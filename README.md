# d3b-flywheel-warehousing

This script can be run anywhere (with appropriate network access, of course) to scrape image metadata from Flywheel and store it in a warehouse database.

Just run:

```bash
pip3 install -r requirements.txt
python3 scour_flywheel.py
```

Operation currently depends on two environment variables:

| Environment Key | Description |
|-----------------|-------------|
| FLYWHEEL_API_TOKEN | Your API token for Flywheel. It looks like `chop.flywheel.io:<random_alphanum>`.<br> D3b has a gsuite service account for this `flywheel@d3b.center`. |
| D3B_WAREHOUSE_DB_URL | A user/pass authenticated URL<br>like `postgresql://<username>:<password>@<server_uri>/postgres` |
