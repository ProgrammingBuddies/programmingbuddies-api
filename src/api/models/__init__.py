"""
The database package
"""
from sys import argv
from datetime import datetime
from api.models.database import db, init_db
from api.models.userModel import User
from api.models.projectModel import Project

if '--reset-db' in argv:
    init_db(True)
else:
    init_db()

"""
# Test data
from api.models.userModel import UserLink
from api.models.projectModel import ProjectLink

user1 = User()
user1.name = 'Foe Joe'

link1 = UserLink()
link1.name = 'GitHub'
user1.links.append(link1)

project1 = Project()
project1.name = 'Hello, World!'

link2 = ProjectLink()
link2.name = 'Discord'
project1.links.append(link2)

user1.projects.append(project1)

db.session.add(user1)
db.session.commit()
"""
