import os
import flask
import logging
import boto
import MySQLdb

__doc__ = """
Flaskr
------

AWS Elastic Beanstalk baseline application based on the flaskr micro-blog
tutorial,

http://flask.pocoo.org/docs/tutorial/introduction/

Adapted for Amazon AWS Elastic Beanstalk
by Ryan Galloway <ryan@rsgalloway.com>

http://github.com/rsgalloway/flaskr
"""

DEBUG = True

# app.config stuff
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# use boto to manage aws rds instances, vs. _mysql
USE_BOTO = False

application = app = flask.Flask(__name__)
app.config.from_object(__name__)
app.debug = DEBUG

def connect_db():
    logging.info("Connecting to AWS RDS")
    if USE_BOTO:
        return boto.rds.connect_to_region(
                          "us-west-2",
                          aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key=os.environ['AWS_SECRET_KEY']
                          )
    else:
        return MySQLdb.Connection(host=os.environ['RDS_HOSTNAME'],
                              user=os.environ['RDS_USERNAME'],
                              port=int(os.environ['RDS_PORT']),
                              passwd=os.environ['RDS_PASSWORD'],
                              db=os.environ['RDS_DB_NAME']
                             )

def init_db():
    if USE_BOTO:
        message_table_schema = flask.g.db.create_schema(
            hash_key_name='title',
            hash_key_proto_value='S',
        )
        table = conn.create_table(
            name='entries',
            schema=message_table_schema,
            read_units=10,
            write_units=10
        )
    else:
        flask.g.db.cursor().execute(open("schema.sql").read())

@app.before_request
def before_request():
    flask.g.db = connect_db()
    logging.info('before_request: db=%s' % flask.g.db)

@app.teardown_request
def teardown_request(exception):
    flask.g.db = None

@app.route('/')
def show_entries():
    if USE_BOTO:
        table = flask.g.db.get_table('entries')
        entries = table.scan()
    else:
        curr = flask.g.db.cursor()
        curr.execute('select title, text from entries order by id desc')
        entries = [dict(title=row[0], text=row[1]) for row in curr.fetchall()]
    logging.info('show_entries: N=%s' % entries)
    return flask.render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not flask.session.get('logged_in'):
        flask.abort(401)

    item_data = {
        'text': flask.request.form['text'],
    }

    if USE_BOTO:
        table = flask.g.db.get_table('entries')
        item = table.new_item(
            hash_key=request.form['title'],
            attrs=item_data
        )
        item.put()
    else:
        flask.g.db.query("insert into entries (title, text) values ('%s', '%s')"
                   % (flask.request.form['title'], flask.request.form['text']))
        r = flask.g.db.store_result()

    flask.flash('New entry was successfully posted')
    return flask.redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if flask.request.method == 'POST':
        if flask.request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif flask.request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            flask.session['logged_in'] = True
            flask.flash('You were logged in')
            return flask.redirect(flask.url_for('show_entries'))
    return flask.render_template('login.html', error=error)

@app.route('/logout')
def logout():
    flask.session.pop('logged_in', None)
    flask.flash('You were logged out')
    return flask.redirect(flask.url_for('show_entries'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)

