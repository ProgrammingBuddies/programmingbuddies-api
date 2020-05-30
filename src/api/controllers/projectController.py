from api.models import db, Project, UserHasProject, ProjectLink, ProjectFeedback

class ProjectController:
    session = db.session()

    # Project
    def create_project(self, **kwargs):
        try:
            project = Project(**kwargs)
            self.session.add(project)
            self.session.commit()

            return project
        except:
            return None

    def update_project(self, id, **kwargs):
        project = Project.query.filter_by(id=id).first()

        if project == None:
            return None

        for key, value in kwargs.items():
            if not hasattr(project, key):
                return None

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

    # Project Link
    def create_link(self, project_id, **kwargs):
        try:
            link = ProjectLink(project_id=project_id, **kwargs)
            self.session.add(link)
            self.session.commit()

            return link
        except:
            return None

    def update_link(self, project_id, link_id, **kwargs):
        link = ProjectLink.query.filter_by(project_id=project_id, id=link_id).first()

        if link == None:
            return None

        for key, value in kwargs.items():
            if not hasattr(link, key):
                return None

        for key, value in kwargs.items():
            setattr(link, key, value)

        db.session.commit()

        return link

    def get_all_links(self, project_id):
        all_links = ProjectLink.query.filter_by(project_id=project_id).all()

        return all_links

    def delete_link(self, project_id, link_id):
        link = ProjectLink.query.filter_by(project_id=project_id, id=link_id).first()

        if link == None:
            return None

        db.session.delete(link)
        db.session.commit()

        return link

    # Project Feedback
    def create_feedback(self, project_id, **kwargs):
        try:
            feedback = ProjectFeedback(project_id=project_id, **kwargs)
            self.session.add(feedback)
            self.session.commit()

            return feedback
        except:
            return None

    def get_all_feedbacks(self, project_id):
        all_feedbacks = ProjectFeedback.query.filter_by(project_id=project_id).all()

        return all_feedbacks

    def delete_feedback(self, project_id, feedback_id):
        feedback = ProjectFeedback.query.filter_by(project_id=project_id, id=feedback_id).first()

        if feedback == None:
            return None

        db.session.delete(feedback)
        db.session.commit()

        return feedback

projectController = ProjectController()
