import os.path
from pathlib import Path

from split_settings.tools import include, optional 

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# # Namespacking out own custom env var
# ENV_SETTINGS_PREFIX = "CORESETTINGS_"

# LOCAL_SETTINGS_PATH = os.getenv(f'{ENV_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

# if not LOCAL_SETTINGS_PATH:
#     LOCAL_SETTINGS_PATH = "local/settings.dev.py"

# if not os.path.isabs(LOCAL_SETTINGS_PATH):
#     LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include("base.py", "local.py")
