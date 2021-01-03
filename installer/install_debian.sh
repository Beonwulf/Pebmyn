#!/bin/bash
has_sudo() {
    local prompt

    prompt=$(sudo -nv 2>&1)
    if [ $? -eq 0 ]; then
    echo "has_sudo__pass_set"
    elif echo $prompt | grep -q '^sudo:'; then
    echo "has_sudo__needs_pass"
    else
    echo "no_sudo"
    fi
}

current_username=$(whoami)

HAS_SUDO=$(has_sudo)

set -eu -o pipefail # fail on error , debug all lines
#echo $HAS_SUDO

if [ "$HAS_SUDO" == 'no_sudo' ]
	then
		echo "you should have sudo priveledge to run this script"
		exit 1
elif [ "$HAS_SUDO" == 'has_sudo__needs_pass' ]
	then
		echo "you should have sudo priveledge to run this script"
		exit 1
elif [ "$HAS_SUDO" == 'has_sudo__pass_set' ]
	then echo "Debian! Ich beginne!"
fi
sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

MY_DOMAIN='your.domain'
USER='pebmyn'
PORT=2402
while getopts ':d:p:u:pw:' OPTION ; do
	case "$OPTION" in
		d)	MY_DOMAIN=$OPTARG; echo "Domain is $MY_DOMAIN";;
		u)	USER=$OPTARG; echo "Username is $USER";;
		p)	PORT=$OPTARG; echo "Port is $PORT";;
		*)	echo "Unknown parameter"
	esac
done


function checker() {
	#which "$1" | grep -o "$1" > /dev/null &&  return 1 || return 0
	apt-mark showinstall | grep -q "^$1$" && return 1 || return 0
}

function ccreatePebmynConf() {
	domain=$1
	port=$2
	user=$3
	echo "Config mit domain: $domain und port: $port user:$user"
}
function createPebmynConf() {
	domain=$1
	port=$2
	user=$3
	sudo cat > /etc/apache2/sites-available/$user.conf << ENDOFFILE
Listen $port
NameVirtualHost *:$port
<VirtualHost *:$port>
        ServerAdmin webmaster@$domain
        ServerAlias $domain
        ServerName www.$domain
        ErrorLog /home/$user/www/logs/error.log
        CustomLog /home/$user/www/logs/access.log combined

        WSGIDaemonProcess $user user=$user group=www-data threads=5
        WSGIProcessGroup $user
        WSGIScriptAlias / /home/$user/www/py/main.wsgi
        Alias /static/ /home/$user/www/py/static

        <Directory /home/$user/www/py>
                Require all granted
        </Directory>
</VirtualHost>
ENDOFFILE
}

####
# check visudo -f ....
# 400
#
function createSudoersPebmyn() {
	if [ -n ${1+x} ]; then
		user=$1
	else
		user=$USER
	fi
	sudo cat > /etc/sudoers.d/pebmyn << ENDOFFILE
#Runas-Alias specification
Runas_Alias WEB = www-data, apache

# User-Alias specification
User_Alias  WEBMASTER1 = $user
User_Alias  APTITUDE = $user
User_Alias  GAMEMASTER = $user
User_Alias  VOICEMASTER = $user

# Comand-Alias specification
Cmnd_Alias  CMD_APACHE2 = /usr/sbin/apache2
Cmnd_Alias  CMD_APACHE_EN = /usr/sbin/a2enconf, /usr/sbin/a2enmod, /usr/sbin/a2ensite
Cmnd_Alias  CMD_APACHE_DIS = /usr/sbin/a2disconf, /usr/sbin/a2dismod, /usr/sbin/a2dissite
Cmnd_Alias  CMD_APT = /usr/bin/apt-get

# User privilege specification
#$user       ALL=(ALL:ALL) ALL
WEBMASTER1  ALL = (WEB) NOPASSWD: CM_APACHE2, CMD_APACHE_EN, CMD_APACHE_DIS
#APTITUDE    ALL = NOPASSWD: CMD_APT
ENDOFFILE
}

function createApache2modSecurityConf() {
	sudo cat > /etc/apache2/conf-available/mod_security.conf << ENDOFFILE
<IfModule mod_security.c>
	# Turn the filtering engine On or Off
	SecFilterEngine On

	# Make sure that URL encoding is valid
	SecFilterCheckURLEncoding On

	# Unicode encoding check
	SecFilterCheckUnicodeEncoding Off

	# Only allow bytes from this range
	SecFilterForceByteRange 0 255

	# Only log suspicious requests
	SecAuditEngine RelevantOnly

	# The name of the audit log file
	SecAuditLog /var/log/apache2/audit_log
	# Debug level set to a minimum
	SecFilterDebugLog /var/log/apache2/modsec_debug_log
	SecFilterDebugLevel 0

	# Should mod_security inspect POST payloads
	SecFilterScanPOST On

	# By default log and deny suspicious requests
	# with HTTP status 500
	SecFilterDefaultAction "deny,log,status:500"

</IfModule>
ENDOFFILE
#sudo a2enconf mod_security
}

#sudo apt-get update


if checker "apache2" == 1 ; then echo "Apache was already Installed"; else echo "Apache Not Installed!"; fi

for modul in "python3" "apache2" "php7.4" "libapache2-mod-php7.4"
	do
		if checker "$modul" == 1 ;
			then echo "$modul was already Installed";
			else 
				echo "$modul Not Installed!";
				#sudo apt install $modul
		fi
done


if checker "libapache2-mod-security2" == 1 ;
	then
		echo "libapache2-mod-security2 was already Installed";
else
	echo "libapache2-mod-security2 Not Installed!";
	sudo apt install libapache2-mod-security2
	sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf
fi

ccreatePebmynConf $MY_DOMAIN $PORT $USER
