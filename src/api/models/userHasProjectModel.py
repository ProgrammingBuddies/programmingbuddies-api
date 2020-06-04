from api.models import db

class UserHasProject(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    user = db.relationship('User', back_populates='projects')
    project = db.relationship('Project', back_populates='users')
    role = db.Column(db.Integer, nullable=False)

    def user_as_dict(self):
        return { 'user_id': self.user_id, 'role': self.role }

    def project_as_dict(self):
        return { 'project_id': self.project_id, 'role': self.role }
