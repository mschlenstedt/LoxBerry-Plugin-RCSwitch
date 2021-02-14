#!/bin/bash

# Shell script which is executed *BEFORE* installation is started
# (*BEFORE* preinstall and *BEFORE* preupdate). Use with caution and remember,
# that all systems may be different!
#
# Exit code must be 0 if executed successfull.
# Exit code 1 gives a warning but continues installation.
# Exit code 2 cancels installation.
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Will be executed as user "root".
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# You can use all vars from /etc/environment in this script.
#
# We add 5 additional arguments when executing this script:
# command <TEMPFOLDER> <NAME> <FOLDER> <VERSION> <BASEFOLDER>
#
# For logging, print to STDOUT. You can use the following tags for showing
# different colorized information during plugin installation:
#
# <OK> This was ok!"
# <INFO> This is just for your information."
# <WARNING> This is a warning!"
# <ERROR> This is an error!"
# <FAIL> This is a fail!"

# To use important variables from command line use the following code:
COMMAND=$0    # Zero argument is shell command
PTEMPDIR=$1   # First argument is temp folder during install
PSHNAME=$2    # Second argument is Plugin-Name for scipts etc.
PDIR=$3       # Third argument is Plugin installation folder
PVERSION=$4   # Forth argument is Plugin version
#LBHOMEDIR=$5 # Comes from /etc/environment now. Fifth argument is
              # Base folder of LoxBerry
PTEMPPATH=$6  # Sixth argument is full temp path during install (see also $1)

# Combine them with /etc/environment
PCGI=$LBPCGI/$PDIR
PHTML=$LBPHTML/$PDIR
PTEMPL=$LBPTEMPL/$PDIR
PDATA=$LBPDATA/$PDIR
PLOG=$LBPLOG/$PDIR # Note! This is stored on a Ramdisk now!
PCONFIG=$LBPCONFIG/$PDIR
PSBIN=$LBPSBIN/$PDIR
PBIN=$LBPBIN/$PDIR

# Installing pilight
if [ ! -x /usr/local/sbin/pilight-daemon ]; then
	APT_LISTCHANGES_FRONTEND=none
	DEBIAN_FRONTEND=noninteractive
	echo "Installing pilight - please be patient..."
	dpkg --configure -a
	cd /tmp
	wget http://apt.pilight.org/pool/stable/main/l/libmbedx509-0/libmbedx509-0_2.6.0-1_armhf.deb
	wget http://apt.pilight.org/pool/stable/main/l/libmbedtls10/libmbedtls10_2.6.0-1_armhf.deb
	wget http://apt.pilight.org/pool/stable/main/l/libmbedcrypto0/libmbedcrypto0_2.6.0-1_armhf.deb
	dpkg -i libmbed*.deb
	rm libmbed*.deb
	echo "deb http://apt.pilight.org/ stable main" > /etc/apt/sources.list.d/pilight.list
	wget -O - http://apt.pilight.org/pilight.key | apt-key add -
	apt-get -y --allow-unauthenticated --fix-broken --reinstall --allow-downgrades --allow-remove-essential --allow-change-held-packages --purge autoremove
	apt-get -y --allow-unauthenticated --allow-downgrades --allow-remove-essential --allow-change-held-packages update
	apt-get --no-install-recommends -y --allow-unauthenticated --fix-broken --reinstall --allow-downgrades --allow-remove-essential --allow-change-held-packages install pilight
	service pilight stop
	systemctl disable pilight
fi

# Installing WiringPi on LoxBerry 2.0
if [ ! -x /usr/bin/gpio ]; then
	APT_LISTCHANGES_FRONTEND=none
	DEBIAN_FRONTEND=noninteractive
	echo "Installing WiringPi - please be patient..."
	dpkg --configure -a
	cd /tmp
	wget https://project-downloads.drogon.net/wiringpi-latest.deb
	dpkg -i wiringpi-latest.deb
	rm wiringpi-latest.deb
fi

exit 0
