from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


# python manage.py db init - creates migrations folder

# python manage.py db migrate - creates a migrations scripts

# python manage.py db upgrade

# Always include migrations folder in version control to maintan the history of db changes

# Migrate the upgrade Always

# Before any rollbacks/downgrades, backup db always

# python manage.py db downgrade -1  --  takes you back one revision

# use python manage.py db history for specific revision ids

# update directly on migrate scrips or start new script with changes
