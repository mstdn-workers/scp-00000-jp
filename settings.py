import os
import utils.file

# Mode
DEBUG_MODE    = os.path.exists(".debug_mode")
MAO_ONLY_MODE = os.path.exists(".mao_only_mode")

# Channels
CHANNEL_GENERAL   = "C54RD0EPK"
CHANNEL_CONTAINER = "C6PBY609X"
CHANNEL_DEBUG     = "G7C8SLGCX"

# Users
USER_SELF = "U7AF58VGQ"
USER_MAO  = "U59KR7QKT"

# Token
API_TOKEN = os.environ.get("SLACK_API_TOKEN", utils.file.read(".token"))

# Option
TIMER_INTERVAL = 5 if DEBUG_MODE else 60 * 60