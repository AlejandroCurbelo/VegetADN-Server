from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

from flask_cors import CORS
CORS(app)

from flask_login import LoginManager
login = LoginManager(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
db.reflect()
from sqlalchemy import MetaData
db.make_declarative_base(db.Model, MetaData(bind=db.get_engine()))

from app.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint)

from flask_restful import Api
routes = Api(app)
from .api import *
routes.add_resource(Biodatabase, '/biodatabase', '/biodatabase/<name>')
routes.add_resource(Bioentry, '/bioentry', '/bioentry/<int:id>', '/bioentry/<string:accession>')
routes.add_resource(Taxon, '/taxon', '/taxon/<int:id>', '/taxon/<string:name>')
routes.add_resource(FilesIO, '/upload/<biodb>', '/download')
routes.add_resource(Search, '/search')

print('\t¡¡ SET UP !!\n')

if __name__ == '__main__':
    from models import User

    db.create_all()
    print('''>> Creating the two user accounts.
        >> Insert the data for the administrator.''')
    from getpass import getpass
    username = input('Username: ')
    while True:
        password = getpass()
        check_password = getpass('Repeat the same password: ')
        if password == check_password:
            break
        print('The password does not match. Try again.')
    db.session.add(User(username, password, True))
    print('>> Insert the data for the basic user.')
    username = input('Username: ')
    while True:
        password = getpass()
        check_password = getpass('Repeat the same password: ')
        if password == check_password:
            break
        print('The password does not match. Try again.')
    db.session.add(User(username, password))
    db.session.commit()
