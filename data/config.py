from environs import Env

env = Env()

env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
NAME = env.str('NAME')



ADMINS_ID = 2049738013
ADMIN_GROUP = -1001508571081
