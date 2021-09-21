"""
Fetch acquisition files linked to project/subject/session labels from Flywheel
and upload the records to the warehouse DB.
"""
import os

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

# Get metadata quickly with a View. This is very fast. No acquisitions or files
# here, though, because those seem to break the view requester.

with yaspin(text="Fetching flywheel View data.") as spin:
    view = fw.View(
        columns=["project.label", "subject.label", "session.label", "session.id"],
        include_ids=False
    )
    # FIXME: I've replaced read_view_dataframe for now because the current
    # implementation (as of 16.0.0rc1) raises a FutureWarning from pandas
    # because it passes "records" as a positional argument instead of the
    # orient keyword argument. Please periodically check the implementation of
    # read_view_dataframe to see if flywheel.io has fixed this. - Avi
    meta_df = pandas.concat(
        (
            pandas.read_json(
                fw.read_view_data(view, p.id, decode=False, format="json-flat"),
                orient="records"
            ) for p in fw.projects.iter()
        ),
        ignore_index=True
    )
    # meta_df = pandas.concat(
    #     (fw.read_view_dataframe(view, p.id) for p in fw.projects.iter()),
    #     ignore_index=True,
    # )
    spin.ok("✅")

# Get acquisition file details with a find iterator. Not super fast, but
# somehow infinitely faster than including them in the View.

files = []
n = 0
file_cols = ("id", "name", "modality", "created", "modified", "size")
msg = "Scouring flywheel for acquisition files."
with yaspin(text=msg) as spin:
    # Using an iter_find filter for "modification>..." is not safe here because
    # attached files can be newer than the acquisition's timestamp.
    for ac in fw.acquisitions.iter():
        session = {"session.id": ac.session}
        for fi in ac.files:
            n += 1
            files.append(session | {f"file.{c}": getattr(fi, c) for c in file_cols})
            spin.text = f"{msg}  Found: {n}"
    spin.ok("✅")

# Send file records to database.

if files:
    with yaspin(text=f"Submitting {len(files)} records to the database...") as spin:
        df = (
            pandas.DataFrame(files)
            .merge(meta_df, how="left", on="session.id")
            .drop(columns=["session.id"])  # we don't need this anymore
            .rename(columns=lambda x: x.replace(".", "_"))  # avoid "." in cols
        )
        df.to_sql(
            table, db, index=False, if_exists="replace", chunksize=10000, method="multi"
        )
        spin.ok("✅")
else:
    print("No files found.")
