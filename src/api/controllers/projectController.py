from api.models import db, Project, UserHasProject, ProjectLink

class ProjectController:
    session = db.session()
    def create_project(self, **kwargs):
        project = Project(**kwargs)
        self.session.add(project)
        self.session.commit()

        return project

    def update_project(self, id, **kwargs):
        project = Project.query.filter_by(id=id).first()

        if project == None:
            return project

        for key, value in kwargs.items():
            setattr(project, key, value)

        db.session.commit()

        return project

    def get_project(self, **kwargs):
        project = Project.query.filter_by(**kwargs).first()
        
        return project
    
    def get_all_projects(self, **kwargs):
        all_projects = Project.query.all()

        return all_projects

    def delete_project(self, id):
        # Remove all project's links
        for link in ProjectLink.query.filter_by(project_id=id).all():
            db.session.delete(link)
        
        # Remove project from all users
        for project in UserHasProject.query.filter_by(project_id=id).all():
            db.session.delete(project)
        
        project = Project.query.filter_by(id=id).first()
        
        if project == None:
            return project
        
        db.session.delete(project)
        db.session.commit()
        
        return project

projectController = ProjectController()