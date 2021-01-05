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

HAS_SUDO=$(has_sudo)

if [ "$HAS_SUDO" == 'no_sudo' ]
	then
		echo "you should have sudo priveledge to run this script"
		exit 1
elif [ "$HAS_SUDO" == 'has_sudo__needs_pass' ]
	then
		echo "you should have sudo priveledge to run this script"
		exit 1
elif [ "$HAS_SUDO" == 'has_sudo__pass_set' ]
	then echo "PEBMYN! ich beginne!"
fi

VHOST_PATH="/etc/apache2/sites-available"
LISTEN='*'
PORT=80
USER=''
CNAME='www'
DOMAIN=''
SSL='NO'
DOCROOT='htdocs'
while getopts ':c:d:l:u:p:s:' OPTION ; do
	case "$OPTION" in
		c)	CNAME=$OPTARG; echo "Cname is $CNAME";;
		d)	DOMAIN=$OPTARG; echo "Domain is $DOMAIN";;
		l)	LISTEN=$OPTARG; echo "listen is $LISTEN";;
		u)	USER=$OPTARG; echo "Username is $USER";;
		p)	PORT=$OPTARG; echo "Port is $PORT";;
		r)	DOCROOT=$OPTARG; echo "docroot is $DOCROOT";;
		s)	SSL=$OPTARG; echo "SSL is $SSL";;
		*)	echo "Unknown parameter"
	esac
done

ALIAS="$CNAME.$DOMAIN"
FILE_VHOST="$VHOST_PATH/$CNAME.$DOMAIN.conf"
WWW="/home/$USER/www"
WWWD="$WWW/domains"
MYDIR="/home/$USER/www/domains/$DOMAIN/$DOCROOT"
LOGDIR="/home/$USER/www/log/"
[ ! -d "$WWW" ] && mkdir -p "$WWW"
[ ! -d "$WWWD" ] && mkdir -p "$WWWD"
[ ! -d "$MYDIR" ] && mkdir -p "$MYDIR"
[ ! -d "$LOGDIR" ] && mkdir -p "$LOGDIR"


read -d '' VHOST_CONTENT <<EOF
<VirtualHost $LISTEN:$PORT>
	ServerName $DOMAIN
	ServerAlias $ALIAS
	DocumentRoot $MYDIR
	ErrorLog $LOGDIR$ALIAS.error.log
	CustomLog $LOGDIR$ALIAS.access.log combined
	<Directory $MYDIR>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Order allow,deny
		Allow from all
		Require all granted
	</Directory>
</VirtualHost>
EOF



if [ "$SSL" == 'yes' ] 
	then
		SSLDIR="/home/$USER/www/ssl"
		[ ! -d "$SSLDIR" ] && mkdir -p "$SSLDIR"
		SSLCRT="$SSLDIR/$DOMAIN.crt"
		SSLKEY="$SSLDIR/$DOMAIN.key"
		openssl req -x509 -new -extensions v3_ca -newkey rsa:4096 -keyout $SSLKEY -out $SSLCRT -days 365 -nodes \
				-subj "/CN=$DOMAIN/O=./C=DE"
		if ! echo -e $SSLKEY; then
			echo "Certificate key wasn't created !"
		else
			echo "Certificate key created !"
		fi
		echo "create ssl vhost"
		read -d '' VHOST_CONTENT_SSL <<EOF
#### ssl $ALIAS
<VirtualHost $listen:443>
	SSLEngine on
	SSLCertificateFile $SSLCRT
	SSLCertificateKeyFile $SSLKEY
	ServerName $DOMAIN
	ServerAlias $ALIAS
	DocumentRoot $MYDIR
	<Directory $MYDIR>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Order allow,deny
		Allow from all
		Satisfy Any
	</Directory>
</VirtualHost>
EOF
		cat > $VHOST_PATH <<EOF
$VHOST_CONTENT
$VHOST_CONTENT_SSL
EOF
else 
	sudo cat > $FILE_VHOST << ENDOFFILE
$VHOST_CONTENT
ENDOFFILE
fi


chown -R $USER:$USER $WWWD
chmod -R '775' $WWWD

exit 1
