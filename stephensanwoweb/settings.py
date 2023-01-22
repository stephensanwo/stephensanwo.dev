import yaml
import os
from stephensanwoweb.types.settings import WebSettings
from dotenv import load_dotenv

load_dotenv()

def settings():
    path = os.environ.get("SETTINGS_PATH")
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return WebSettings.parse_obj(config)
