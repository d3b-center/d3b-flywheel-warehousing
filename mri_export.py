"""
Fetch acquisition files linked to project/subject/session labels from Flywheel
and upload the records to the warehouse DB.
"""
import os
import re
import json
import flywheel
import pandas
from sqlalchemy import create_engine

fw_api_token = os.getenv("FLYWHEEL_API_TOKEN")
db_url = os.getenv("D3B_WAREHOUSE_DB_URL")
assert fw_api_token and db_url

print("Starting scour")

fw = flywheel.Client(fw_api_token)
db = create_engine(db_url)
table = "flywheel_mri_export"

# Get file metadata quickly with Views. This is relatively fast.

view = fw.View(
    container="acquisition",
    filename="*",
    match="all",
    columns=[
        "file.id",
        "file.name",
        "file.size",
        "file.type",
        "file.modality",
        "file.info.MagneticFieldStrength",
        "file.info.BodyPartExamined",
        "file.classification.Intent",
        "file.classification.Features",
        "file.classification.Measurement",
        "file.info.dim1",
        "file.info.dim2",
        "file.info.SpacingBetweenSlices",
        "file.info.Manufacturer",
        "file.info.ManufacturersModelName",
        "file.info.SoftwareVersions",
        "file.created",
        "file.modified",
    ],
    include_ids=True,
    include_labels=True,
    process_files=False,
    sort=False,
)


all_data = []
# for project in fw.projects.iter():
for project in fw.projects.iter():
    pid = project.id
    name = project.label
    grp = project.group
    if ((grp == 'd3b') and ('_v2' in name)) or (grp == 'corsica'):
      print(f"Fetching view for project {name} ({pid})...")
      d = json.load(fw.read_view_data(view, pid, decode=False, format="json-flat"))
      all_data.extend(d)

# Send file records to database.

if all_data:
    rex = re.compile(r"(?<!_)(?=[A-Z])")
    df = (
        pandas.DataFrame(all_data)
        .rename(columns=lambda x: x.replace(".", "_"))  # avoid "." in colnames
        .rename(columns=lambda x: rex.sub("_", x).lower())  # camelcase to snake
    )

    df['session_age_days']  = df['session_label'].str.split('d_').str[0].astype(int) # days

    df['acquisition_number'] = df['acquisition_label'].str.split(' - ').str[0].astype(int)
    acq_counts = df['acquisition_id'].value_counts()
    df['session_n_total_acquisitions'] = df['acquisition_id'].map(acq_counts)

    print(f"Submitting {len(df)} records to the '{table}' table in {repr(db.url)}...")
    df.to_sql(
        table, db, schema = "fw_cloud", index=False, if_exists="replace", chunksize=10000, method="multi"
    )
    with db.connect() as conn:
        conn.execute(f"GRANT SELECT ON {table} TO public")
else:
    print("No files found.")
