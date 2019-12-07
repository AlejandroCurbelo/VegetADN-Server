from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

from flask_cors import CORS
CORS(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
db.reflect()
from sqlalchemy import MetaData
db.make_declarative_base(db.Model, MetaData(bind=db.get_engine()))
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(binds=db.get_binds(app))

from flask_restful import Api
routes = Api(app)
from .api import *
routes.add_resource(Biodatabase, '/biodatabase', '/biodatabase/<int:id>', '/biodatabase/<string:id_name>')
routes.add_resource(Bioentry, '/bioentry', '/bioentry/<int:id>', '/bioentry/<string:accession>')
routes.add_resource(Taxon, '/taxon', '/taxon/<int:id>', '/taxon/<string:name>')
routes.add_resource(FilesIO, '/upload/<biodb>', '/download')
routes.add_resource(Search, '/search')

print('\t¡¡¡¡¡¡¡¡¡ Configurando !!!!!!!!!')
