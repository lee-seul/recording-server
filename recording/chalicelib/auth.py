# coding: utf-8


from chalicelib.db_handler import DynamoDB


def check_authorization(request):
    user_id, auth_key = request.headers['Authorization']

    db = DynamoDB()

    query_item = {
        'id': user_id,
        'auth_key': auth_key
    }

    user = db.get_item('recording', 'user', query_item)
    if not user:
        return None
    return user

    