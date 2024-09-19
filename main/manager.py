"""
This script provides a command-line interface for managing database migrations 
using Flask-Migrate in the Flask backend service.

It allows you to create, apply, and revert database schema changes using the 
'flask db' command.
"""

from main import app, db 
from flask_migrate import Migrate, MigrateCommand  
from flask_script import Manager  

migrate = Migrate(app, db) 

manager = Manager(app) 
manager.add_command('db', MigrateCommand) 

if __name__ == '__main__':
    manager.run() 