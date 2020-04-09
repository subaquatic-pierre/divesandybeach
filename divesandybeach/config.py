import os
import json
# path to config file outsite django server
home = os.path.expanduser('~')
with open(home + '/etc/divesandybeach/config.json') as f:
    config = json.load(f)


class Config():

    DEBUG = config.get("DEBUG")
    SECRET_KEY = config.get("SECRET_KEY")
    DB_ENGINE = config.get("DB_ENGINE")
    DB_HOST = config.get("DB_HOST")
    DB_NAME = config.get("DB_NAME")
    DB_USER = config.get("DB_USER")
    DB_PASSWORD = config.get("DB_PASSWORD")
    EMAIL_HOST = config.get("EMAIL_HOST")
    EMAIL_HOST_USER = config.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config.get("EMAIL_HOST_PASSWORD")
    SOCIALACCOUNT_PROVIDERS = config.get("SOCIALACCOUNT_PROVIDERS")
    AWS_ACCESS_KEY_ID = config.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config.get("AWS_SECRET_ACCESS_KEY")
    RECAPTCHA_PUBLIC_KEY = config.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = config.get("RECAPTCHA_PRIVATE_KEY")
    AWS_STORAGE_BUCKET_NAME = config.get("AWS_STORAGE_BUCKET_NAME")
