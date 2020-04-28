"""
The database package
"""
from sys import argv
from datetime import datetime
from api.models.database import db, init_db
from api.models.userModel import UserHasProject, User, UserLink, UserFeedback
from api.models.projectModel import Project, ProjectLink, ProjectFeedback

if '--reset-db' in argv:
    init_db(True)
else:
    init_db()

"""
# Test data
import datetime;

user1 = User(name='Foe Joe')
user2 = User(name='Tommy Frich')
user3 = User(name='Limm Carter')
link1 = UserLink(name='GitHub', url='https://github.com')
user1.links.append(link1)

project1 = Project(name='Hello, World!', repository="https://github.com/ProgrammingBuddies/programmingbuddies-api", description='First project.', development_status=2, creation_date=datetime.datetime.now())
link2 = ProjectLink(name='Reddit', url='https://reddit.com')
project1.links.append(link2)

userHasProject = UserHasProject(role=1)
userHasProject.project = project1

user1.projects.append(userHasProject)

feedback1 = ProjectFeedback(rating=3, description="Cool project!", author=user1)
feedback2 = ProjectFeedback(rating=1, description="Not so cool!", author=user2)

project1.feedbacks.append(feedback1)
project1.feedbacks.append(feedback2)

feedback3 = UserFeedback(author=user1, user=user2, rating=5, description="Good guy!")
feedback4 = UserFeedback(author=user3, user=user2, rating=1, description="Poor guy!")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

users = User.query.all()
print(users[0].author, users[0].user, users[0].project_feedbacks)
print(users[1].author, users[1].user, users[1].project_feedbacks)
print(users[2].author, users[2].user, users[2].project_feedbacks)
"""
