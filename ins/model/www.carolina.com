#
#  carolina.com (/etc/apache2/sites-available/www.carolina.com)
#
<VirtualHost *:80>
        ServerAdmin webmaster@carolina.com
        ServerName  www.carolina.com
        ServerAlias carolina.com
	
	#DocumentRoot baseprefix/app/
	#<Directory baseprefix/app/>
	#	Options Indexes FollowSymLinks MultiViews
	#	AllowOverride None
	#	Order allow,deny
	#	allow from all
	#</Directory>


	WSGIDaemonProcess  myseries user=www-data group=www-data processes=1 threads=5
	WSGIScriptAlias / baseprefix/app/myseries.wsgi.py
	

	<Directory /var/lib/series/app>
		WSGIProcessGroup myseries
		WSGIApplicationGroup %{GLOBAL}
		Order deny,allow
		Allow from all
	</Directory>

        # Logfiles
        ErrorLog  baseprefix/logs/error.log
        CustomLog baseprefix/logs/access.log combined
</VirtualHost>
