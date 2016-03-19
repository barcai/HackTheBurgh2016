#! /usr/bin/env python
from flask.ext.script import Manager, Server

from budgetbanger import create_app
from budgetbanger.models import User, Money
from budgetbanger import models



app = create_app('dev')
manager = Manager(app)


# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)

@manager.shell
def make_shell_context():
    return dict(app=app, models=models)

@manager.command
def create_table():
    db.create_all()

@manager.command
def create_and_insert():

    db.create_all()

    admin = User(user_name = "admin", email = "admin@admin.com", password = "admin",  is_admin=True)

    db.session.add(admin)

    db.session.commit()
    print('Inserted mock data')


if __name__ == '__main__':
    manager.run()