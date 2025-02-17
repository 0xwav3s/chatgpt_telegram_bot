import yaml
import dotenv
from pathlib import Path
import urllib.request
from json import load
import requests
from requests.auth import HTTPDigestAuth

config_dir = Path(__file__).parent.parent.resolve() / "config"

# load yaml config
with open(config_dir / "config.yml", 'r') as f:
    config_yaml = yaml.safe_load(f)

# load .env config
config_env = dotenv.dotenv_values(config_dir / "config.env")

# config parameters
telegram_token = config_yaml["telegram_token"]
openai_api_key = config_yaml["openai_api_key"][1]
allowed_telegram_usernames = config_yaml["allowed_telegram_usernames"]
new_dialog_timeout = config_yaml["new_dialog_timeout"]
# mongodb_uri = {config_env['MONGODB_URI']}
mongodb_uri_local = {config_env['MONGODB_URI_LOCAL']}



atlas_group_id = config_yaml["atlas_group_id"]
atlas_api_key_public = config_yaml["atlas_api_key_public"]
atlas_api_key_private = config_yaml["atlas_api_key_private"]


IP_addres = requests.get("https://api.ipify.org?format=json").json()["ip"]

print("IP: "+ IP_addres)
resp = requests.post(
    "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
    auth=HTTPDigestAuth(atlas_api_key_public, atlas_api_key_private),
    json=[{'ipAddress': IP_addres, 'comment': 'From PythonAnywhere'}]  # the comment is optional
)
if resp.status_code in (200, 201):
    print("MongoDB Atlas accessList request successful", flush=True)
else:
    print(
        "MongoDB Atlas accessList request problem: status code was {status_code}, content was {content}".format(
            status_code=resp.status_code, content=resp.content
        ),
        flush=True
    )

