# Linux Server Configuration (Notes)

### Root directories:

`/home`:  users directories

`/etc`:   configuration files (db, server, ...)

`/var`:   variable (in size & number) files => typically system & app logs

`/bin`:   executable binaries that are accessible by all users

`/sbin`:  like sbin, but binaries for only root user => system admin & maint.

`/lib`:   libraries that support binaries

`/usr`:   user programs/binaries (which are not required for bootup & system maint.)


===========================

### Miscellaneous
`~/.bash_history`: recent history of every command user type in terminal

Change the group of a FILE:

`[sudo] chgrp GROUP FILE`

Change the owner of a FILE:

`[sudo] chown USER FILE`


Remove packages that are no longer required & can be automatically removed:

`sudo apt-get autoremove`


Each linux dist. serves an easy-to-browse version of packages:

for ubuntu: http://packages.ubuntu.com => use search


**Finger**: a user information lookup program

`sudo apt-get install finger`


`/etc/passwd`:    info about users

`/etc/sudoers`:   who can use `sudo` command (#includedir /etc/sudoers.d)
    keeping customization in "`/etc/sudoers.d`" (common pattern) avoids being reset in case of distribution update overwrites "`/etc/sudoers`"


Don't use "su", use "sudo commands" instead


Disable root user


Change password of currently logged-in user:

`passwd`


Force USER to reset his/her password @ next login (expire password):

`sudo passwd -e USER`


Public key is the key placed on server for key-based authentication

MD5 & SHA256 are hashing algorithms (one-way) not suitable for public key encryption

### Configure SSH (key-based logins):
- Generate key pairs (do it locally to be sure that private key is private): ssh-keygen
- Place the public key in the remote server
- On remote machine: create file (`touch ~/.ssh/authorized_keys`: file contains all public keys that this account is allowed to use for authen., one key per line)
- Copy the content of the *.pub key file generated-locally to this file on remote machine
- On remote machine: change permissions: "`chmod 700 ~/.ssh; chmod 644 ~/.ssh/authorized_keys;`"
- Login to remote machine via ssh: `ssh USER@IP ip PORT -i ~/.ssh/KEYNAME`

### Disable any password logins (forcing key-based authentication):
- On remote machine: edit the ssh configuration file (`sudo nano /etc/ssh/sshd_config`)
-   Change "PasswordAuthentication yes" to "no"
- Restart the ssh service to read the new configuration: (`sudo service ssh restart`)

### Disable "root" login via ssh:
- On remote machine: edit the ssh configuration file (`sudo nano /etc/ssh/sshd_config`) => Change "`PermitRootLogin *`" to "`no`"
- Restart the ssh service to read the new configuration: (`sudo service ssh restart`)

### Disable/lock "root" login at all:
- `sudo passwd -l root" OR "sudo usermod -p '!' root`

### Configure the UFW firewall (Allow only required ports)

Ubuntu's Firewall (ufw) is by default inactive: `sudo ufw status`

*CAUTION*: ssh IS on a connection

*Recommendation*: configure firewall early after server installation

`sudo ufw default deny incoming`:  by default deny all incoming

`sudo ufw default allow outgoing`: by default allow all outgoing

`sudo ufw allow ssh`

`sudo ufw allow 2222/tcp` (custom ssh port in vagrant)

`sudo ufw allow www

`sudo ufw enable`



