from api.models import db

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
