# FSND-Project-Linux-Server-Configuration
* IP address: `52.59.170.191`
* SSH port: `2200`
* URL of the hosted web application: http://52.59.170.191/
>> Note: to login to the app, add `52.59.170.191 fsnd.dev` to `/etc/hosts` file & use URL: http://fsnd.dev/
* Software installed:
  - apache2
  - libapache2-mod-wsgi
  - python-flask
  - python-flask-sqlalchemy
  - python-sqlalchemy
  - python-oauth2client
  - python-oauthlib
  - python-httplib2
  - python-requests
* Configuration changes made:
  - Firewall: allow only ports: 2200, 80, 123
  - Configure apache `VirtualHost *:80` for: `WSGIScriptAlias / /var/www/html/apache.wsgi`
  - Users: add user `grader` & delete user `ubuntu`. Add `grader` to `sudoers`
  - Generate ssh key pair to: `/home/grader/.ssh/id_rsa`
  - Add the generated ssh key to `authorized_keys` of user: `grader`
  - Update & upgrade all packages
* Resources used to complete this project: Ubuntu terminal & built-in ssh
