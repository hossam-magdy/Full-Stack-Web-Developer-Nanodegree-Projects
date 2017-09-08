# LOGIN
ssh ubuntu@IP -p 22 -i KEYFILE_FROM_AMAZON

# SSH PORT=2200 & DISABLE SSH FOR "root"
sudo nano /etc/ssh/sshd_config # Change "Port 22" to "Port 2200" AND "PermitRootLogin prohibit-password/*" to "PermitRootLogin no"
sudo service sshd restart

# FIREWALL
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200 # for SSH
sudo ufw allow 80   # for HTTP
sudo ufw allow 123  # for NTP
sudo ufw enable
sudo ufw status

# ADD USER: grader
sudo adduser grader

# SUDOER
sudo cp /etc/sudoers.d/90-cloud-init-users /etc/sudoers.d/grader
sudo nano /etc/sudoers.d/grader # "grader ALL=(ALL) NOPASSWD:ALL"

# NEW RSA/SSH keypair
mkdir /home/grader/.ssh
sudo ssh-keygen # save_key_path=/home/grader/.ssh/id_rsa
sudo cat /home/grader/.ssh/id_rsa # & COPY the rsa key to a local file (KEYFILE)
sudo cp /home/grader/.ssh/id_rsa.pub /home/grader/.ssh/authorized_keys
logout
#Locally: chmod 700 KEYFILE
ssh grader@IP -p 2200 -i KEYFILE

# DELETE DEFAULT USER
sudo deluser ubuntu

# PACKAGES UPDATE & UPGRADE
sudo apt-get update
sudo apt-get upgrade

# CONFIGURE APACHE2 & MOD_WSGI
sudo apt-get install apache2 libapache2-mod-wsgi
sudo nano /etc/apache2/sites-enabled/000-default.conf
#Add line at end of VirtualHost: WSGIScriptAlias / /var/www/html/apache.wsgi
#apache.wsgi content: from PYTHON_FILE import app as application
sudo apache2ctl restart

# WEB_APP: INSTALL DEPENDENCIES & CLONE REPO TO: /var/www/html
sudo apt-get install git python-flask python-flask-sqlalchemy python-sqlalchemy python-oauth2client python-oauthlib python-httplib2 python-requests
cd /var/www
sudo mv html html.old
sudo git clone REPO_PATH html
cd /var/www/html
sudo apache2ctl restart
