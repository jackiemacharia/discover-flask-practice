from app import db
from models import User

# Insert data
db.session.add(User("jackie", "jackie@example.com", "neverwilltell"))
db.session.add(User("admin", "ad@min.com", "admin"))

db.session.commit()
