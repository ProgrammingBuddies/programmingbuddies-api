"""
The database package
"""
from sys import argv
from datetime import datetime
from api.models.database import db, init_db
from api.models.userModel import UserHasProject, User, UserLink
from api.models.projectModel import Project, ProjectLink

if '--reset-db' in argv:
    init_db(True)
else:
    init_db()

"""
# Test data
import datetime;

user1 = User(name='Foe Joe')
link1 = UserLink(name='GitHub', url='https://github.com')
user1.links.append(link1)

project1 = Project(name='Hello, World!', description='First project.', development_status=2, creation_date=datetime.datetime.now())
link2 = ProjectLink(name='Reddit', url='https://reddit.com')
project1.links.append(link2)

userHasProject = UserHasProject(role=1)
userHasProject.project = project1

user1.projects.append(userHasProject)

db.session.add(user1)
db.session.commit()
"""
