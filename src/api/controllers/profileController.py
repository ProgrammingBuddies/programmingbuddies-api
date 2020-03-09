from api.models import db, Profile

class ProfileController:
    session = db.session()
    def create_profile(self, **kwargs):
        profile = Profile(**kwargs)
        self.session.add(profile)
        self.session.commit()

    def get_profile(self, **kwargs):
        profile = Profile.query.filter_by(**kwargs).first()
        return profile

profileController = ProfileController()
