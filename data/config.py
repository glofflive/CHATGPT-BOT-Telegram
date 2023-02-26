from environs import Env

env = Env()

env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
NAME = env.str('NAME')



ADMINS_ID = 5822638695
ADMIN_GROUP = -851307290