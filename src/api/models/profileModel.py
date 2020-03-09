from api.models import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(80), nullable=False)
    experienceLevel = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Profile %r>' % self.title
