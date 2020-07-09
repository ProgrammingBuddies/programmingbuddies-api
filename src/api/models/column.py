from api.models import db


class Column(db.Column):
    readonly = False
    const = False

    def __init__(self, *args, readonly=False, const=False, **kwargs):
        if const:
            self.readonly = self.const = True
        elif readonly:
            self.readonly = True

        super(Column, self).__init__(*args, **kwargs)
