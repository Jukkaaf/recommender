from pyramid.view import view_config
from functions.test import testfunction
from functions.collaborative import collaborativeFiltering
import MySQLdb as mysli

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'recommender'}

@view_config(route_name='test', renderer='templates/test.jinja2')
def test(request):
    result = testfunction()
    return {'test': 'testi teksti',
            'result': result
            }

@view_config(route_name='collab', renderer='templates/collab.jinja2')
def collab(request):
    return {'action': request.matchdict.get('action')}

@view_config(route_name='collab_action', match_param='action=filter', renderer='templates/collab.jinja2')
def collab_filter(request):
    params = request.POST

    settings = request.registry.settings
    db = mysli.connect(settings['mysql.host'], settings['mysql.user'], settings['mysql.password'], settings['mysql.database'])

    result = collaborativeFiltering(params["User-ID"].encode("utf-8"), params["ISBN"].encode("utf-8"), db)
    return {'result': result,
            'params': params,
            'action': request.matchdict.get('action'),
}