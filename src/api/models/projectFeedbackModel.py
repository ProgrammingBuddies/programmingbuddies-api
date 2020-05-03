from api.models import db
# from api.models.projectModel import Project
# from api.models.userModel import User

class ProjectFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)
