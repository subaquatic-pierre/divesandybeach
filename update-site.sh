#! /bin/bash

ssh-add ~/.ssh/aws-ecs-ohio.pem
ssh ubuntu@18.216.193.42 ./update-site.sh