##### 500 server error followed by a 502 bad gateway after server restart
* update and upgrade ubuntu
* **error**: `unix:///var/run/supervisor.sock no such file`
* restart supervisord `sudo service supervisor restart`
* **solution**: `/etc/supervisor/conf.d/celery.conf` was not configured correctly. Settings of the main configuration file were probably overwritten