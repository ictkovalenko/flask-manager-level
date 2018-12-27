import os
from flask_migrate import MigrateCommand, Migrate
from flask_script import Shell, Manager, Server
from app import create_app, db
from app.models import Roles, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(db=db,
                Roles=Roles,
                User=User)


manager.add_command("runserver", Server(host='127.0.0.1', port=8000))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def fakefill():
    import fake
    fake.clear_database()
    fake.create_superuser()
    fake.fake_users()


@manager.command
def cleardb():
    import fake
    fake.clear_database()
    fake.create_superuser()


if __name__ == '__main__':
    manager.run()


