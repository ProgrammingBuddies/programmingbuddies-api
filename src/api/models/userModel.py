from api.models import db

class UserHasProject(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    user = db.relationship('User', back_populates='projects')
    project = db.relationship('Project', back_populates='users')
    role = db.Column(db.Integer, nullable=False)

    # todo: figure out where to put the role property

    def user_as_dict(self):
        return { 'user_id': self.user_id, 'role': self.role }

    def project_as_dict(self):
        return { 'project_id': self.project_id, 'role': self.role }

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

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'languages': self.languages,
            'interests': self.interests,
            'location': self.location,
            'occupation': self.occupation,
            'projects': [ project.project_as_dict() for project in self.projects ],
            'links': [ link.as_dict() for link in self.links ]
        }
        return obj_d

    def __repr__(self):
        return '<User %r>' % self.name

class UserLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'user_id': self.user_id
        }
        return obj_d

    def __repr__(self):
        return '<UserLink %r>' % self.name