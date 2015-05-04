#IoT Resource Tree Representation for Massive Data Sets
Introduction:

The goal of the project is to provide a webapp to view 1 million+ data points collected from the OpenDaylight. Visual aids must give the user a sense for extracting meaning from these mass quantities of data in an intuitive way. Our solution will also contain management functions for adding, editing or deleting nodes from the tree. We also want minimize the client/server side response time to provide a fluid user experience. This documentation should serve as a means of describing our system as well as configuring it for use. 

##System Overview:

![UML Diagram](https://raw.github.com/nkunkel/BU-EC500-SP15/iot-ui-bigdata/master/Docs/IOT_UML.png)

##Prerequisite
<b>1. Install Python2</b> (https://www.python.org/downloads/)

<b>2. Install Apache2</b> (http://apache.org/dyn/closer.cgi)

<b>3. Clone iot-ui-bigdata repo:</b>

    git clone https://github.com/CCI-MOC/haas

##Apache Configuration
<b>1. Enable cgid</b>

This will enable CGI processing in Apache so that it can execute python script on server side.

    sudo a2enmod cgi

<b>2. Modify Apache httpd or conf file</b>

In Ubuntu system, Apache conf file location is:

    /etc/apache2/apache.conf

Then add into it:

    <Directory /var/www/html/network/cgi-bin>
        Options ExecCGI
        SetHandler cgi-script
    </Directory>

    <Directory /var/www/html/network>
        Options +ExecCGI
        AddHandler cgi-script .py
    </Directory>

After done this, restart apache server:

    sudo service apache2 restart

<b>3. Put everything into apache web server folder</b>

    cp -r iot-ui-bigdata/network /var/www/html/

##Using visualization tool

<b>Access tool</b>

 After successfully configure Apache, using this address to access

    http://localhost/network/index.html?config=config_ukgov.json

And you are ready to go!

<b>Tool on EC2</b>

There is another replica of this tool on our EC2 instance, feel free to try it out.

    http://54.68.184.172/network/index.html?config=config_ukgov.json#
