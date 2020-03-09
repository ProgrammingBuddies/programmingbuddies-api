from api.models import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    experienceLevel = db.Column(db.Integer, nullable=False)
    developmentStatus = db.Column(db.Integer, nullable=False)
    creationDate = db.Column(db.DateTime, nullable=False)
    releaseDate = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Project %r>' % self.title
