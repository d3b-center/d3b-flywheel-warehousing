"""
Fetch acquisition files linked to project/subject/session labels from Flywheel
and upload the records to the warehouse DB.
"""

import os

import flywheel
import pandas
import pangres
import psycopg2
from sqlalchemy import create_engine
from yaspin import yaspin

fw_api_token = os.getenv("FLYWHEEL_API_TOKEN")
db_url = os.getenv("D3B_WAREHOUSE_DB_URL")
assert fw_api_token
assert db_url

fw = flywheel.Client(fw_api_token)
db = create_engine(db_url)
table = "flywheel_export"

try:
    last_mod = db.execute(f"select max(file_modified) from {table};").one()[0]
except Exception:
    last_mod = None

# Get metadata quickly with a View. This is very fast. No acquisitions or files
# here, though, because those seem to break the view requester.

view = fw.View(
    columns=["project.label", "subject.label", "session.label", "session.id"]
)
meta_df = pandas.concat(
    (fw.read_view_dataframe(view, p.id) for p in fw.projects.iter()),
    ignore_index=True,
)

# Get acquisition file details with a find iterator. Not super fast, but
# somehow infinitely faster than including them in the View.

msg = "Scouring flywheel for acquisition files"
if last_mod:
    msg += f"modified after: '{last_mod.isoformat()}'"

files = []
n, m = 0, 0
file_cols = ("id", "name", "modality", "created", "modified", "size")
with yaspin(text=msg) as spin:
    # Using an iter_find filter for "modification>..." is not safe here because
    # attached files can be newer than the acquisition's timestamp.
    for ac in fw.acquisitions.iter():
        session = {"session.id": ac.session}
        for fi in ac.files:
            n += 1
            if (last_mod is None) or (fi.modified > last_mod):
                files.append(session | {f"file.{c}": getattr(fi, c) for c in file_cols})
                m += 1
            spin.text = f"{msg}.  Found: {m}/{n}"
    spin.ok("✅ ")

# Send file records to database.

if files:
    with yaspin(text=f"Submitting {len(files)} records to the database...") as spin:
        pangres.upsert(
            engine=db,
            df=pandas.DataFrame(files)
            .merge(meta_df, how="left", on="session.id")
            .set_index(["file.id"], drop=True)  # file.id primary key for upsert
            .drop(columns=["session.id"])  # we don't need this anymore
            .rename(columns=lambda x: x.replace(".", "_")),  # avoid "." in cols
            table_name=table,
            add_new_columns=True,
            if_row_exists="update",
        )
        spin.ok("✅ ")
else:
    print("No files found.")
