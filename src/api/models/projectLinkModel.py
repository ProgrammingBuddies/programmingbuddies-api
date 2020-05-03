from api.models import db

class ProjectLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    # todo: decide if this should contain project_id (it is already present in the model)
    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'project_id': self.project_id
        }
        return obj_d

    def __repr__(self):
        return '<ProjectLink %r>' % self.name
