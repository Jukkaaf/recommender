from pyramid.view import view_config
from functions.test import testfunction

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'recommender'}

@view_config(route_name='test', renderer='templates/test.jinja2')
def test(request):
    result = testfunction()
    return {'test': 'testi teksti',
            'result': result
            }
