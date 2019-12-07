from flask_restful import Resource
from flask import abort, request

class Search(Resource):
    methods = ['GET', 'PUT']

    def get(self):
        print(f'\n### GET(search) request:\n{request}')
        self.__check_args()
        self.__set_args()
        return self.__get_paged_search(), 200


    def put(self):
        print(f'\n### PUT(search) request:\n{request}')
        print(request.args)
        print(request.form)
        print(request.values)
        print(request.files)
        print(request.json)
        return 200
        if ('type' in request.json):
            if request.json['type'] == 'biodatabase':
                query = 'REFRESH MATERIALIZED VIEW biodatabase_search;'
            elif request.json['type'] == 'bioentry':
                query = 'REFRESH MATERIALIZED VIEW bioentry_search;'
            elif request.json['type'] == 'taxon':
                query = 'REFRESH MATERIALIZED VIEW taxon_search;'
            msg = f'The full-text search for {request.json["type"]} is ready.'
        else:
            query = '''REFRESH MATERIALIZED VIEW biodatabase_search;
                REFRESH MATERIALIZED VIEW bioentry_search;
                REFRESH MATERIALIZED VIEW taxon_search;'''
            msg = 'The full-text search is ready.'
        from app import db
        db.session.execute(query)
        db.session.commit()
        db.session.close()
        return {'message': msg}, 200


    def __check_args(self):
        print(request.args)
        if ('type' not in request.args) or ('search' not in request.args) \
            or ('page' not in request.args) or ('page_size' not in request.args):
            abort(400, description=f'Params are missing.')
        if request.args['type'] not in ('biodatabase', 'bioentry', 'taxon'):
            abort(409, description=f'Search of type {type} is not available.')
        if not (request.args['page'].isdigit() and request.args['page_size'].isdigit()):
            abort(409, description='The page information is incorrect.')


    def __set_args(self):
        self.type = request.args['type']
        self.search = ' & '.join(request.args['search'].strip().split())
        self.page = request.args['page']
        self.page_size = request.args['page_size']


    def __get_paged_search(self):
        query = self.__get_query()
        query = query.paginate(int(self.page), int(self.page_size), False)
        result = []
        for b in query.items:
            result.append(b.serialize())
        return {'result': result, 'pages' : query.pages, 'total' : query.total}


    def __get_query(self):
        if self.search=='':
            return self.__get_all()
        else:
            if self.type=='biodatabase':
                return self.__search_biodatabase()
            if self.type=='bioentry':
                return self.__search_bioentry()
            if self.type=='taxon':
                return self.__search_taxon()


    def __get_all(self):
        if self.type == 'biodatabase':
            from app.models import Biodatabase as Bioelement
        if self.type == 'bioentry':
            from app.models import Bioentry as Bioelement
        if self.type == 'taxon':
            from app.models import TaxonName
            return TaxonName.query.filter(TaxonName.name_class == 'scientific name')
        return Bioelement.query


    def __search_biodatabase(self):
        from app import db
        from app.models import Biodatabase, BiodatabaseSearch
        return Biodatabase.query \
            .join(BiodatabaseSearch, Biodatabase.biodatabase_id == BiodatabaseSearch.biodatabase_id) \
            .filter(BiodatabaseSearch.document.match(self.search, postgresql_regconfig='english'))


    def __search_bioentry(self):
        from app import db
        from app.models import Bioentry, BioentrySearch
        return Bioentry.query \
            .join(BioentrySearch, Bioentry.bioentry_id == BioentrySearch.bioentry_id) \
            .filter(BioentrySearch.document.match(self.search, postgresql_regconfig='english'))


    def __search_taxon(self):
        from app import db
        from app.models import TaxonName, TaxonSearch
        return TaxonName.query \
            .filter(TaxonName.name_class == 'scientific name') \
            .join(TaxonSearch, TaxonName.taxon_id == TaxonSearch.taxon_id) \
            .filter(TaxonSearch.document.match(self.search, postgresql_regconfig='english'))
