#!/bin/bash
echo Parameters: $@
WWWORIG=www.carolina.com
WWWCONF=www.carolina.com.conf
SUBDIRS=("scripts app cgi-bin htdocs logs data tpl img") ## Add new directories here

PREFIX=$1

if [ -z $PREFIX ]; then
    PREFIX=/var/lib/series
fi

if [ -d $PREFIX ]
then
    echo $PREFIX already there
else
    echo Creating: $PREFIX
    sudo mkdir -m 775 $PREFIX
	sudo chown -R www-data:www-data $PREFIX
fi
for s in $SUBDIRS
do
    if [ ! -d $PREFIX/$s ]; then
        sudo mkdir -m 775 $PREFIX/$s
	sudo chown -R www-data:www-data $PREFIX$s
    fi
done

sudo cp core-1.0.0/scripts/addic7ed.py $PREFIX/scripts
sudo cp core-1.0.0/tpl/firstpage.tpl $PREFIX/tpl
sudo cp core-1.0.0/tpl/serieslist.tpl $PREFIX/tpl
sudo cp core-1.0.0/tpl/seasonslist.tpl $PREFIX/tpl
sudo cp core-1.0.0/tpl/list.tpl $PREFIX/tpl
sudo cp core-1.0.0/tpl/mystyle.css $PREFIX/tpl
sudo cp core-1.0.0/img/favicon.ico $PREFIX/img
sudo cp core-1.0.0/img/vallmo.jpg $PREFIX/img

cd core-1.0.0
sudo ./setup_myseries.py install
cd ..

sudo cp core-1.0.0/wsgi/myseries.wsgi.py $PREFIX/app

sudo chown -R www-data:www-data $PREFIX/app
sudo chown -R www-data:www-data $PREFIX/tpl
sudo chown -R www-data:www-data $PREFIX/img

sudo touch $WWWCONF
sudo chmod 777 $WWWCONF
sudo sed s?baseprefix?$PREFIX?  $WWWORIG > $WWWCONF
sudo cp $WWWCONF /etc/apache2/sites-available/

sudo a2ensite $WWWCONF
sudo apache2ctl restart


