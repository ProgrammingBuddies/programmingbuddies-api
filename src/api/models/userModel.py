from api.models import db

from api.models.userHasProjectModel import UserHasProject
from api.models.userLinkModel import UserLink
from api.models.projectFeedbackModel import ProjectFeedback

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.Integer)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text)
    languages = db.Column(db.Text)
    interests = db.Column(db.Text)
    location = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    projects = db.relationship('UserHasProject', back_populates='user')
    links = db.relationship('UserLink', backref='user', lazy=True)
    project_feedbacks = db.relationship('ProjectFeedback', backref='project_feed_author')
    user_feedbacks = db.relationship('UserFeedback', foreign_keys="UserFeedback.author_id", backref='user_feed_author')
    received_feedbacks = db.relationship('UserFeedback', foreign_keys="UserFeedback.user_id", backref='destination')

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'github_id': self.github_id,
            'name': self.name,
            'bio': self.bio,
            'languages': self.languages,
            'interests': self.interests,
            'location': self.location,
            'occupation': self.occupation,
            'projects': [ project.project_as_dict() for project in self.projects ],
            'links': [ link.as_dict() for link in self.links ],
            'feedbacks': [ feedback.as_dict() for feedback in self.received_feedbacks ]
        }
        return obj_d

    def __repr__(self):
        return '<User %r>' % self.name
