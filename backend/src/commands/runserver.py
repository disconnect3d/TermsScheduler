from flask.ext.script import Server, Option

from application.utils import logsql


class Runserver(Server):
    def __init__(self, *args, **kwargs):
        self.logsql = False
        super().__init__(*args, **kwargs)

    def get_options(self):
        return super().get_options() + (
            Option('--logsql',
                   action='store_true',
                   dest='logsql',
                   help='Enables logging of SQL queries (DO NOT use in production code)',
                   default=False),
        )

    def __call__(self, *args, **kwargs):
        self.logsql = kwargs.pop('logsql', False)

        if self.logsql:
            logsql()

        super().__call__(*args, **kwargs)
