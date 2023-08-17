import os
import json
from django.conf import settings

# path to config file outsite django server
home = os.path.expanduser("~")


class Config:
    def __init__(self, config: object) -> None:
        self.DEBUG = config.get("DEBUG")
        self.SECRET_KEY = config.get("SECRET_KEY")
        self.DB_ENGINE = config.get("DB_ENGINE")
        self.DB_HOST = config.get("DB_HOST")
        self.DB_NAME = config.get("DB_NAME")
        self.DB_USER = config.get("DB_USER")
        self.DB_PASSWORD = config.get("DB_PASSWORD")
        self.EMAIL_HOST = config.get("EMAIL_HOST")
        self.EMAIL_HOST_USER = config.get("EMAIL_HOST_USER")
        self.EMAIL_HOST_PASSWORD = config.get("EMAIL_HOST_PASSWORD")
        self.SOCIALACCOUNT_PROVIDERS = config.get("SOCIALACCOUNT_PROVIDERS")
        self.AWS_ACCESS_KEY_ID = config.get("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = config.get("AWS_SECRET_ACCESS_KEY")
        self.RECAPTCHA_PUBLIC_KEY = config.get("RECAPTCHA_PUBLIC_KEY")
        self.RECAPTCHA_PRIVATE_KEY = config.get("RECAPTCHA_PRIVATE_KEY")
        self.AWS_STORAGE_BUCKET_NAME = config.get("AWS_STORAGE_BUCKET_NAME")


def open_config(base_dir: str) -> object:
    local_settings = os.path.join(base_dir, "config.json")
    if os.path.exists(local_settings):
        with open(local_settings) as f:
            return json.load(f)
    else:
        with open(home + "/etc/divesandybeach/config.json") as f:
            return json.load(f)


def load_config(base_dir: str) -> Config:
    config_json = open_config(base_dir)
    return Config(config_json)
