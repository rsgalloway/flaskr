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

::

% git clone http://github.com/rsgalloway/flaskr
% cd flaskr
% eb init
% eb start
% git aws.push
% eb status --verbose


Changes
-------

The original database was Sqlite3.  This was removed and modified
to use RDS, either using boto or MySQL-python The first-time setup 
should be done by opening the /initdb URL.


Additions
---------

The `.ebextensions` folder contains Python-specific settings,
including the WSGI configuration and the environment variables
which are used to supply the AWS Identity Key and Secret Key
needed to use the APIs.  Make sure you update these values
before deploying the system.

