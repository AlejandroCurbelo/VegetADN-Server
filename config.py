import os
basedir = os.path.abspath(os.path.dirname(__file__))

# from Bio import Entrez
# Entrez.email = 'vegetADN@vegetadn.es'

DEBUG = False
TESTING = False
with open(f'{basedir}/password', 'r') as file:
    PASSWORD = file.read().splitlines()[0]
SQLALCHEMY_DATABASE_URI = f'postgresql://vegetadn:{PASSWORD}@localhost:5432/vegetadn'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
SECRET_KEY = '\xfc\xfe\xad\xe1u\xd3=\xfd?\x00\xb6\xfeQ\x176\x17C\xd6\xfa\xf2\xfbK\x1f\xa0\xd6lx~\xcev.\xb4'

if __name__ == '__main__':
    from app import app, db
    from app.models import User

    db.create_all()
    print('>> Creating the two user accounts that will access to the aplication.\n',
        '>> Insert the data for the administrator (full-access).')
    from getpass import getpass
    username = input('Username: ')
    while True:
        password = getpass()
        check_password = getpass('Repeat the same password: ')
        if password == check_password:
            break
        print('The password does not match. Try again.')
    db.session.add(User(username, password, True))
    print('>> Insert the data for the basic user (read and download only).')
    username = input('Username: ')
    while True:
        password = getpass()
        check_password = getpass('Repeat the same password: ')
        if password == check_password:
            break
        print('The password does not match. Try again.')
    db.session.add(User(username, password))
    db.session.commit()
