############################ To run the app via apache2: mod_wsgi
#sudo apt-get install apache2 libapache2-mod-wsgi
#sudo nano /etc/apache2/sites-enabled/000-default.conf
#Add line at end of VirtualHost: WSGIScriptAlias / PATH_TO_THIS_FILE
#sudo apache2ctl restart
############################

import sys, os
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from project import app as application


