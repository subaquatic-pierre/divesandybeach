#! /bin/bash

ssh-add ~/.ssh/aws-main-us-east-2.pem
ssh ubuntu@18.216.193.42 ./update-site.sh