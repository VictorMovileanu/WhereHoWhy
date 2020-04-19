sudo apt-get update


### PostgreSQL
sudo apt-get -y install postgresql postgresql-contrib
sudo -u postgres createuser wherehowhy
sudo -u postgres createdb wherehowhy --owner wherehowhy
sudo -u postgres psql -c "ALTER USER wherehowhy WITH PASSWORD '<strong password>'"
sudo -u postgres psql -c "ALTER USER wherehowhy CREATEDB;" # allow user wherehowhy to create test databases


### PIP
sudo apt-get -y install python3-pip libpq-dev
pip3 install -r /home/vagrant/WhereHoWhy/requirements.txt
update-alternatives --install /usr/bin/python python /usr/bin/python3 10


### Celery
# Installation instructions:
# - https://www.vultr.com/docs/how-to-install-rabbitmq-on-ubuntu-16-04-47
# - https://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html
sudo apt-get -y install rabbitmq-server
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"


### npm
# installing and running npm in a vagrant requires npm enterprise
# install and run build scripts locally
# >> curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
# >> sudo apt-get install -y nodejs

### setup server
sudo apt-get -y install nginx
sudo apt-get -y install supervisor
sudo systemctl enable supervisor
sudo systemctl start supervisor
adduser wherehowhy
gpasswd -a wherehowhy sudo