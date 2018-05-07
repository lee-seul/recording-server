# coding: utf-8


from chalice import Chalice, Response

from chalicelib.helpers import sign_up_or_login
from chalicelib.utils import make_user_id


app = Chalice(app_name='recording')


@app.route('/login')
def login():
    request = app.current_request
    
    social_id = request.query_params.get('social_id')
    social_type = request.query_params.get('social_type')
    if not social_id or not social_type:
        data = {'error': 'social_id or social_type is null.'}
        return Response(body=data, status_code=400)

    auth_key = sign_up_or_login(social_id, social_type)  
    if not auth_key:
        return Response(status_code=400)

    data = {
        'auth_key': auth_key,
        'user_id': make_user_id(social_id, social_type)
    }

    return Response(body=data, status_code=200)