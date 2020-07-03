from api.models import db, User, Project, UserHasProject, ProjectLink, ProjectFeedback

class ProjectController:
    # TODO: remove this (also from userController)?
    session = db.session

    # Project
    def create_project(self, user_id, **kwargs):
        try:
            user = User.query.filter_by(id=user_id).first()

            if user == None:
                return None, "User not found", 404

            project = Project(**kwargs)

            userHasProject = UserHasProject(role=1)
            userHasProject.project = project
            userHasProject.user = user

            self.session.add(userHasProject)
            self.session.commit()

            return project, "OK", 201
        except:
            self.session.rollback()
            return None, "Project creation failed", 400

    def update_project(self, user_id, **kwargs):
        if 'user_id' in kwargs:
            return None, "Failed to update project. Request body can not specify user's id.", 400

        if 'id' not in kwargs:
            return None, "Failed to update project. Request body must specify project's id.", 400

        user = User.query.filter_by(id=user_id).first()

        if user == None:
            return None, "User not found", 404

        project = Project.query.filter_by(id=kwargs["id"]).first()

        if project == None:
            return None, "Project not found", 404

        # Note that we are updating the id too, but to the same id because we used it to query the user with it
        for key, value in kwargs.items():
            if not hasattr(project, key):
                return None, f"Forbidden attribute '{key}'", 400

        for key, value in kwargs.items():
            setattr(project, key, value)

        db.session.commit()

        return project, "OK", 200

    def get_project(self, **kwargs):
        project = Project.query.filter_by(**kwargs).first()

        if project:
            return project, "OK", 200
        else:
            return None, "Project not found", 404

    def get_all_projects(self, **kwargs):
        all_projects = Project.query.all()

        return all_projects, "OK", 200

    def delete_project(self, user_id, **kwargs):
        if len(kwargs) != 1:
            return None, "Failed to delete project. Request body must contain only project's id.", 400

        if 'id' not in kwargs:
            return None, "Failed to delete project. Request body must specify project's id.", 400

        project_id = kwargs["id"]

        userHasProject = UserHasProject.query.filter_by(user_id=user_id, project_id=project_id).first()
        # TODO: verify that the user owns the project (or has neccessary rights)
        if not userHasProject:
            return None, "Failed to delete project. Current user does not belong to specified project, or the project does not exist.", 404

        # Remove all project's links
        for link in ProjectLink.query.filter_by(project_id=project_id).all():
            db.session.delete(link)

        # Remove project from all users
        for project in UserHasProject.query.filter_by(project_id=project_id).all():
            db.session.delete(project)

        project = Project.query.filter_by(id=project_id).first()

        if project == None:
            # TODO: db.session.rollback?
            return None, "Project not found", 404

        db.session.delete(project)
        db.session.commit()

        return project, "OK", 200

    # Project Link
    def create_link(self, project_id, **kwargs):
        try:
            link = ProjectLink(project_id=project_id, **kwargs)
            self.session.add(link)
            self.session.commit()

            return link
        except:
            self.session.rollback()
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
            self.session.rollback()
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
