from project import db
from project.models import BlogPost

# create the database and the db tables
db.create_all()

# insert
db.session.add(BlogPost("Good", "I\'m good."))
db.session.add(BlogPost("Well", "I\'m well."))
db.session.add(BlogPost("Flask", "discoverflask.com"))
db.session.add(BlogPost("postgres", "we set a local postgres instance"))
# commit the changes
db.session.commit()

# pip install psycopg2 to add sqlite data to heroku postgersql then heroku run python db_create.py
