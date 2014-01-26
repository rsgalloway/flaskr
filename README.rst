Flaskr
======

A baseline Flask application suitable for use on Amazon Elastic Beanstalk.

Based on the flaskr tutorial:

http://flask.pocoo.org/docs/tutorial/introduction/

Things you will need:

- Flask: http://flask.pocoo.org
- AWS 'eb' tool: http://aws.amazon.com/developertools/351/
- AWS API keys: https://console.aws.amazon.com/iam/home?#users
- Git: http://git-scm.com


Quickstart
----------

**Setting up the flaskr app** ::

    % git clone http://github.com/rsgalloway/flaskr
    % cd flaskr
    % eb init
    % eb start
    % git aws.push
    % eb status --verbose

**Initializing the app**

If everything worked as expected, then you should be able to init the db by requesting
the '/init' route at your new flaskr environment URL, for example ::

    http://flaskr-env.elasticbeanstalk.com/init

This sets up the 'entries' table in the RDS database. You can also follow the more manual steps
outlined below.

If you are using MySql on AWS via an RDS instance you must add the IP address you want to connect
from to the "DB Security Groups". To do this go to your AWS Managment Console and select RDS.

- Select "DB Security Groups" on the left panel
- Select "default"
- Select "CIDR/IP" from the select box and enter your workstations public IP address, e.g.

   23.234.192.123/32 (dont forget the /32 for a single ip)

- Click "Add"
- Wait a few minutes for it to go into effect and then connect your MySql client.


**Connecting using mysql client** ::

    % mysql --host=foobar.rds.amazon.com --port=3306 --user=<ebroot> -p <ebdb>

Then source the schema file ::

    mysql> source schema.sql;

