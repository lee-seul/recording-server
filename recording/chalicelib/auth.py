# coding: utf-8


from chalice import Response

from chalicelib.db_handler import DynamoDB


def check_authorization(request):
    if not 'Authorization' in request.headers:
        return False
    
    user_id, auth_key = request.headers['Authorization'].split()

    db = DynamoDB()

    query_item = {
        'id': user_id,
        'auth_key': auth_key
    }

    user = db.get_item('recording', 'user', query_item)
    return user


def not_authorization_response(response_type):
    headers = {'Content-Type': 'application/json'}
    
    body = {'error': 'Not Authorization'}
    status_code = 401
    if response_type is False:
        status_code = 400
        body['error'] = 'Authorization Header is required.'
    
    return Response(
        body=body,
        status_code=status_code,
        headers=headers
    )