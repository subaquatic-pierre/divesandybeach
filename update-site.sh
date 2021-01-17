#! /bin/bash

ssh-add ~/.ssh/aws-ecs-ohio.pem
ssh ubuntu@18.223.170.156 ./update-site.sh