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
	then echo "Capuah ich beginne!"
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

function createSudoersPebmyn() {
	sudo cat > /etc/sudoers.d/pebmyn << ENDOFFILE
ENDOFFILE
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
