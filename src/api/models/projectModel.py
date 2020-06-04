from api.models import db
from datetime import datetime

from api.models.userHasProjectModel import UserHasProject
from api.models.projectLinkModel import ProjectLink

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    languages = db.Column(db.Text)
    development_status = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    release_date = db.Column(db.DateTime)
    users = db.relationship('UserHasProject', back_populates='project')
    links = db.relationship('ProjectLink', backref='project', lazy=True)

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'languages': self.languages,
            'development_status': self.development_status,
            'creation_date': self.creation_date,
            'release_date': self.release_date,
            'users': [ user.user_as_dict() for user in self.users ],
            'links': [ link.as_dict() for link in self.links ]
        }
        return obj_d

    def __repr__(self):
        return '<Project %r>' % self.name
