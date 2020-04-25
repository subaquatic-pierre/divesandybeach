#! /bin/bach

cd ~/divesandybeach
eval 'ssh-agent -s'
sudo ssh-add ~/.ssh/github_id_rsa
git pull origin master
sudo supervisorctl reload