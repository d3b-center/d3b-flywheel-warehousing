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
from yaspin import yaspin

fw_api_token = os.getenv("FLYWHEEL_API_TOKEN")
db_url = os.getenv("D3B_WAREHOUSE_DB_URL")
assert fw_api_token and db_url

fw = flywheel.Client(fw_api_token)
db = create_engine(db_url)
table = "flywheel_export"

# Get file metadata quickly with Views. This is relatively fast.

view = fw.View(
    container="acquisition",
    filename="*",
    match="all",
    columns=[
        "file.name",
        "file.size",
        "file.modality",
        "file.info.MagneticFieldStrength",
        "file.classification.Intent",
        "file.classification.Features",
        "file.classification.Measurement",
        "file.created",
        "file.modified",
    ],
    include_ids=True,
    include_labels=True,
    process_files=False,
    sort=False,
)


all_data = []
for project in fw.projects.iter():
    pid = project.id
    name = project.label
    with yaspin(text=f"Fetching view for project {name} ({pid})...") as spin:
        d = json.load(fw.read_view_data(view, pid, decode=False, format="json-flat"))
        all_data.extend(d)
        spin.text = f"Found {len(d)} files for project {name} ({pid})."
        spin.ok("✅")

# Send file records to database.

if all_data:
    rex = re.compile(r"(?<!_)(?=[A-Z])")
    df = (
        pandas.DataFrame(all_data)
        .rename(columns=lambda x: x.replace(".", "_"))  # avoid "." in colnames
        .rename(columns=lambda x: rex.sub("_", x).lower())  # camelcase to snake
    )
    with yaspin(
        text=f"Submitting {len(df)} records to the '{table}' table in {repr(db.url)}..."
    ) as spin:
        df.to_sql(
            table, db, index=False, if_exists="replace", chunksize=10000, method="multi"
        )
        with db.connect() as conn:
            conn.execute(f"GRANT SELECT ON {table} TO public")
        spin.ok("✅")
else:
    print("No files found.")
