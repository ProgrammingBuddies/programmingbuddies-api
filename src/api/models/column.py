from api.models import db


class Column(db.Column):
    readonly = False

    def __init__(self, *args, readonly=False, **kwargs):
        self.readonly = readonly
        super(Column, self).__init__(*args, **kwargs)
