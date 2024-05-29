import sqlite3
import click
from flask import current_app, g

def get_db():
    """
    Get a database connection. If there is none yet for the current application context,
    create one.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    If this request connected to the database, close the connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
    Initialize the database with the schema provided in 'schema.sql'.
    """
    db = get_db()
    try:  
      with current_app.open_resource('schema.sql') as f:
          db.executescript(f.read().decode('utf8'))
    except sqlite3.OperationalError as e:
      print(f"An error occurred: {e}")
      raise
      

@click.command('init-db')
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """
    Register database functions with the Flask app. This is called by the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
