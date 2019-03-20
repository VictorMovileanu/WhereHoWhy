# Installation

## Deployment
```bash
git pull
./manage.py migrate
./manage.py collectstatic
sudo supervisorctl restart wherehowhy
```

## Environment
```bash
git clone https://github.com/ViggieSmalls/WhereHoWhy
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./mange.py migrate
```

## Server setup
```bash
sudo apt-get update
sudo apt-get -y upgrade

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6

sudo apt-get -y install postgresql postgresql-contrib

sudo apt-get -y install nginx

sudo apt-get -y install supervisor

sudo systemctl enable supervisor
sudo systemctl start supervisor

sudo apt-get -y install python3-distutils

wget https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
sudo pip3.6 install virtualenv

adduser wherehowhy
gpasswd -a wherehowhy sudo

sudo su - postgres
createuser wherehowhy
createdb wherehowhy --owner wherehowhy

psql -c "ALTER USER u_boards WITH PASSWORD '<strong password>'"
```