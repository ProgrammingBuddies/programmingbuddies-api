from api.models import db, Project

class ProjectController:
    session = db.session()
    def create_project(self, **kwargs):
        project = Project(**kwargs)
        self.session.add(project)
        self.session.commit()

    def get_project(self, **kwargs):
        project = Project.query.filter_by(**kwargs).first()
        return project

projectController = ProjectController()
