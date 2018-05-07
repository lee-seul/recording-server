# coding: utf-8


from chalice import Chalice, Response

from helpers import sign_up_or_login


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

    data = {
        'auth_key': auth_key,
        'user_id': '{}_{}'.format(social_type, social_id)
    }

    return Response(body=data, status_code=200)