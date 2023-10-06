# d3b-flywheel-warehousing

fw_cloud.mri_export
This script can be run anywhere (with appropriate network access, of course) to scrape mri metadata from all v2 and corsica projects on Flywheel and store it in a warehouse database.


fw_cloud.slide_export
This script can be run anywhere (with appropriate network access, of course) to scrape histology metadata from cbtn_histology project on Flywheel and store it in a warehouse database.

fw_cloud.report_export:
This script can be run anywhere (with appropriate network access, of course) to scrape cbtn report metadata from Flywheel and store it in a warehouse database.



Just run:

  1.for fw_cloud.mri_export:

  pip3 install -r requirements.txt
  python3 mri_export.py
 
 2. for fw_cloud.slide_export:
 
 pip3 install -r requirements.txt
 python3 slide_export.py
 
 3. for fw_cloud.report_export:

  pip3 install -r requirements.txt
  python3 report_export.py




Operation currently depends on two environment variables:

| Environment Key | Description |
|-----------------|-------------|
| FLYWHEEL_API_TOKEN | Your API token for Flywheel. It looks like `chop.flywheel.io:<random_alphanum>`.<br> D3b has a gsuite service account for this `flywheel@d3b.center`. |
| D3B_WAREHOUSE_DB_URL | A user/pass authenticated URL<br>like `postgresql://<username>:<password>@<server_uri>/postgres` |
