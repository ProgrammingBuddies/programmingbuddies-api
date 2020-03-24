from api.models import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    experience_level = db.Column(db.Integer)
    development_status = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    release_date = db.Column(db.DateTime)
    links = db.relationship('ProjectLink', backref='project', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

class ProjectLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name