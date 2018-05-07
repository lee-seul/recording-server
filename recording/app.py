# coding: utf-8


from chalice import Chalice, Response

from chalicelib.auth import check_authorization
from chalicelib.helpers import sign_up_or_login
from chalicelib.utils import make_user_id


app = Chalice(app_name='recording')
app.debug = True

@app.route('/login', methods=['GET'])
def login():
    request = app.current_request
    
    social_id = request.query_params.get('social_id')
    social_type = request.query_params.get('social_type')
    if not social_id or not social_type:
        data = {'error': 'social_id or social_type is null.'}
        return Response(body=data, status_code=400)

    auth_key = sign_up_or_login(social_id, social_type)  
    if not auth_key:
        data = {'error': 'error'}
        return Response(body=data, status_code=400)

    data = {
        'auth_key': auth_key,
        'user_id': make_user_id(social_id, social_type)
    }

    return Response(body=data, status_code=200)


@app.route('/record', methods=['POST'])
def record_save():
    request = app.current_request

    user = check_authorization(request)
    if user is None:
        data = {'error': 'Unauthorization'}
        return Response(body=data, status_code=401)


@app.route('/record/{record_id}', methods=['DELETE'])
def record_delete(record_id):
    request = app.current_request


@app.route('record/list', methods=['GET'])
def record_list():
    request = app.current_request