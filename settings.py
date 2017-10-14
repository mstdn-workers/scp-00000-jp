import os
import utils.file

# Channels
CHANNEL_GENERAL   = "C54RD0EPK"
CHANNEL_CONTAINER = "C6PBY609X"
CHANNEL_DEBUG     = "G7C8SLGCX"

# Bot Users
USER_SELF = "U7AF58VGQ"

# Token
API_TOKEN = os.environ.get("SLACK_API_TOKEN", utils.file.read(".token"))


# Mode
DEBUG_MODE = os.path.exists(".debug_mode")