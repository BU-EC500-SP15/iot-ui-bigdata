#IoT Resource Tree Representation for Massive Data Sets
<b>Introduction:</b>

The goal of this project is to provide a webapp to visualize 1 million+ data points collected from OpenDaylight (ODL). Visual aids must give the user a sense for extracting meaning from these mass quantities of data in an intuitive way. Our solution will contain management functions for adding, editing or deleting nodes from the tree. We also want minimize the client/server side response time to provide a fluid user experience. This documentation should serve as a means of describing our system as well as configuring it for use. 

##System Overview:

![UML Diagram](https://raw.githubusercontent.com/BU-EC500-SP15/iot-ui-bigdata/master/Docs/IOT_UML.png)

<b>Legend</b>

Yellow = EC2 Instance

Green = Server-side Execution

Red = Web Browser

Blue = Client-side User Functionality in browser


<b>Description</b>


Open DayLight is a Software Defined Networking Controller platform used for big data collection and distribution. We are running this as a server on our EC2 instance.


You interact with this ODL server through CRUD operations sent through HTTP. 


We utilized the Python Library Requests to recursively walk through our tree and retrieve all of the attributes for each node. 


Next we parsed all of the data we retrieved from each node into a cumulative JSON format


We use the shape of the tree and the number of nodes to calculate the position for each node in the visual to minimize overlap when rendering.


Finally we re-encode our JSON into the format required by sigma.js, our visualization library.


However, walking the tree and generating the corresponding sigma.js JSON can take quite a long time as trees get very large. This is much too long for a user to wait when loading up the visualization in the web browser. To combat this, rather  than generating the JSON on demand, we pre-compile it, and merely serve up the static JSON file to the client’s web browser. This ensure we have super smooth and low latency render.


We have a Cron job on the server that generates a new JSON file every 10 minute. This gives us near “real-time” visualization client-side without incurring a time-penalty.


![Visualization Example](https://raw.githubusercontent.com/BU-EC500-SP15/iot-ui-bigdata/master/Docs/Visualization.png)


Clicking on a resource such as an AE, Container, or contentInstance pulls up a side-panel containing all of the attributes of that node. Among these, include the resource’s name, ID, type, size, number of children, as well as links to its parent and child nodes. 


For nodes with an extremely large number of data points (called contentInstances), it may be difficult to find the most recent collected data. To make this easier, we’ve added a button called “latest” which will conveniently grab and display this latest data.


From this panel you can also edit the tree. You can edit or delete the existing node, or even create new ones. These CRUD calls to ODL are done via AJAX.


You can easily filter or search the visualization if you know the name of a specific resource, resource type, or attribute.


In order to be more real-time we’ve added the option to refresh the tree. The user can choose to either refresh the whole tree, thereby incurring a potentially large time penalty, OR choose to merely update the current node along with a user-specified level depth to render. This results in a MUCH quicker render while still giving the user the real-time data they want. We feel this is a very good trade-off between functionality and usability.


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
