from api.models import db, User, Project, UserHasProject, ProjectLink, ProjectFeedback

class ProjectController:
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
    def create_link(self, user_id, **kwargs):
        if "project_id" not in kwargs:
            return None, "Failed to create project link. Request body must specify link's 'project_id'.", 400

        try:
            if "link" in kwargs and "project_id" in kwargs and "name" in kwargs["link"] and "url" in kwargs["link"] and len(kwargs) == 2:
                if kwargs["link"]["name"] is None or kwargs["link"]["url"] is None or kwargs["project_id"] is None:
                    return None, "Arguments can't be empty", 400

                link = ProjectLink(project_id=kwargs["project_id"], **kwargs["link"])
                self.session.add(link)
                self.session.commit()

                return link, "OK", 201
            else:
                return None, "Forbidden attributes used in request. Only 'project_id' and 'link' object containing 'name' and 'url' allowed.", 400
        except:
            self.session.rollback()
            return None, "Failed to create project link.", 400

    def update_link(self, user_id, **kwargs):
        if "project_id" in kwargs and "link" in kwargs and "id" in kwargs["link"] and len(kwargs) == 2:
            if kwargs["project_id"] is None or kwargs["link"]["id"] is None:
                return None, "Arguments can't be empty", 400

            link = ProjectLink.query.filter_by(project_id=kwargs["project_id"], id=kwargs["link"]["id"]).first()

            if link == None:
                return None, "Failed to update project link. Project link not found.", 404

            for key, value in kwargs["link"].items():
                if not hasattr(link, key):
                    return None, f"Failed to update project link. Forbidden attribute '{key}'.", 400

            for key, value in kwargs["link"].items():
                setattr(link, key, value)

            db.session.commit()

            return link, "OK", 200
        else:
            return None, "Forbidden attributes used in request. Only 'project_id' and 'link' object containing 'id', 'name' and 'url' allowed.", 400

    def delete_link(self, user_id, **kwargs):
        if "project_id" in kwargs and "link" in kwargs and "id" in kwargs["link"] and len(kwargs) == 2 and len(kwargs["link"]) == 1:
            if kwargs["project_id"] is None or kwargs["link"]["id"] is None:
                return None, "Arguments can't be empty", 400

            link = ProjectLink.query.filter_by(project_id=kwargs["project_id"], id=kwargs["link"]["id"]).first()

            if link == None:
                return None, "Failed to delete project link. Project link not found.", 404

            db.session.delete(link)
            db.session.commit()

            return link, "OK", 200
        else:
            return None, "Forbidden attributes used in request. Only 'project_id' and 'link' object containing 'id' allowed.", 400

    # Project Feedback
    def create_feedback(self, author_id, **kwargs):
        if 'project_id' not in kwargs:
            return None, "Failed to create feedback. Request body must specify feedback's project_id.", 400

        try:
            if "project_id" in kwargs and "rating" in kwargs and "description" in kwargs and len(kwargs) == 3:
                if kwargs["project_id"] is None or kwargs["rating"] is None or kwargs["description"] is None:
                    return None, "Arguments can't be empty", 400

                feedback = ProjectFeedback(author_id=author_id, **kwargs)
                self.session.add(feedback)
                self.session.commit()

                return feedback, "OK", 201
            else:
                return None, "Forbidden attributes used in request. Only 'project_id', 'rating' and 'description' allowed.", 400
        except:
            self.session.rollback()
            return None, "Failed to create project feedback.", 400

    def delete_feedback(self, author_id, feedback_id):
        feedback = ProjectFeedback.query.filter_by(id=feedback_id).first()

        if feedback == None:
            return None, "Failed to delete project feedback. Project feedback not found.", 404

        if feedback.author_id != author_id:
            return None, "Failed to delete project feedback. Cannot delete project feedback that you did not create.", 400

        db.session.delete(feedback)
        db.session.commit()

        return feedback, "OK", 200

projectController = ProjectController()
