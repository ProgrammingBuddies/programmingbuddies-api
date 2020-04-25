from api.models import db

class UserHasProject(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    user = db.relationship('User', back_populates='projects')
    project = db.relationship('Project', back_populates='users')
    role = db.Column(db.Integer, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text)
    languages = db.Column(db.Text)
    interests = db.Column(db.Text)
    location = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    projects = db.relationship('UserHasProject', back_populates='user')
    links = db.relationship('UserLink', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

class UserLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<UserLink %r>' % self.name