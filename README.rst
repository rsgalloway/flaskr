Flaskr
======

A baseline Flask application suitable for use on Amazon Elastic Beanstalk.

Things you will need:

- Flask: http://flask.pocoo.org
- AWS 'eb' tool: http://aws.amazon.com/developertools/351/
- AWS API keys: https://aws-portal.amazon.com/gp/aws/securityCredentials
- Git: http://git-scm.com


Quickstart
----------

Setting up the flaskr app ::

    % git clone http://github.com/rsgalloway/flaskr
    % cd flaskr
    % eb init
    % eb start
    % git aws.push
    % eb status --verbose

Initializing the DB

If you are using MySql on AWS via an RDS instance you must add the IP address you want to connect
from to the "DB Security Groups". To do this go to your AWS Managment Console and select RDS.

1. Select "DB Security Groups" on the left panel
2. Select "default"
3. Select "CIDR/IP" from the select box and enter your workstations public IP address, e.g.

   23.234.192.123/32 (dont forget the /32 for a single ip)

4. Click "Add"
5. Wait a few minutes for it to go into effect and then connect your MySql client.


Connecting using mysql client ::

    % mysql --host=foobar.rds.amazon.com --port=3306 --user=<ebroot> -p <ebdb>

Then source the schema file ::

    mysql> source schema.sql;


Additions
---------

The `.ebextensions` folder contains Python-specific settings,
including the WSGI configuration and the environment variables
which are used to supply the AWS Identity Key and Secret Key
needed to use the APIs.  Make sure you update these values
before deploying the system.

