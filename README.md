# DiveSandyBeach.com

Home of divesandybeach.com website.

Uses Django as base for content management.

## Dev Usage

1. Create virtual end

```sh
python3 -m venv venv
```

2. Install deps

```sh
source venv/bin/acitvate
pip3 install -r requirements.txt
```

3. Run server

```sh
python3 manage.py runserver
```

## Notes:

1. Requires config json file located at `$HOME/etc/divesandybeach/config.json` with following format

```json
{
  "DEBUG": "",
  "SECRET_KEY": "",
  "DB_ENGINE": "",
  "DB_HOST": "",
  "DB_NAME": "",
  "DB_USER": "",
  "DB_PASSWORD": "",
  "EMAIL_HOST": "",
  "EMAIL_HOST_USER": "",
  "RECAPTCHA_PUBLIC_KEY": "",
  "RECAPTCHA_PRIVATE_KEY": "",
  "EMAIL_HOST_PASSWORD": "",
  "AWS_ACCESS_KEY_ID": "",
  "AWS_SECRET_ACCESS_KEY": "",
  "AWS_STORAGE_BUCKET_NAME": "",
  "SOCIALACCOUNT_PROVIDERS": {
    "google": {
      "APP": {
        "client_id": "",
        "secret": "",
        "key": ""
      }
    },
    "facebook": {
      "APP": {
        "client_id": "",
        "secret": "",
        "key": ""
      }
    }
  }
}
```
