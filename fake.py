from app import db
from app.models import User, Roles


def clear_database():
    User.query.delete()
    db.session.commit()
    print('DB flushed')


def create_superuser():
    a = User()
    a.login = 'admin'
    a.name_first = 'root'
    a.name_last = 'root'
    a.email = 'root@gmail.com'
    a.role = Roles.ADMIN
    db.session.add(a)
    db.session.commit()
    print('SU added')


def fake_users():
    counter = 0
    for x in range(5):
        u = User()
        u.login = 'user{}'.format(x)
        u.name_first = 'FIRST NAME {}'.format(x)
        u.name_last = 'LAST NAME {}'.format(x)
        u.email = 'user{}@gmail.com'.format(x)
        u.city = 'City {}'.format(x)
        u.company = 'Company {}'.format(x)
        u.contacts = '(044) 495-11-95'
        u.role = Roles.USER
        db.session.add(u)
        counter += 1
    db.session.commit()
    print('fake users added successfully: {}'.format(counter))
