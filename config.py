from envparse import env

env.read_envfile(".env")

# BOT
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
LOGFILE = env.str("LOGFILE")
SKIP_UPDATES = env.bool("SKIP_UPDATES")
OWNER = env.int("OWNER")

# DATABASE
DB_FILE = env.str("DB_FILE")