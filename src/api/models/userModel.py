from api.models import db
from api.models.projectModel import Project

projects = db.Table('user_has_project',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text)
    experience_level = db.Column(db.Integer)
    interests = db.Column(db.Text)
    location = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    projects = db.relationship('Project', secondary=projects, backref=db.backref('members', lazy='dynamic'))
    links = db.relationship('UserLink', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

class UserLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<UserLink %r>' % self.name
