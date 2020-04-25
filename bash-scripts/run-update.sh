#! /bin/bash

ssh-add ~/.ssh/ubuntu_ssh_key.pem
ssh ubuntu@3.15.1.157 'bash -s' < 'update-site.sh'