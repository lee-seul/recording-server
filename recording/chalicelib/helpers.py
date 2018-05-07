# coding: utf-8 


from chalicelib.db_handler import DynamoDB
from chalicelib.utils import generate_key, make_user_id


def sign_up_or_login(social_id:str, social_type:str):
    user_id = make_user_id(social_id, social_type)
    auth_key = generate_key(64)

    db = DynamoDB()

    app_name = 'recording'
    table_name = 'user'

    item = {
        'user_id': user_id,
        'auth_key': auth_key
    }

    result = db.insert_item(app_name, table_name, item)
    if result:
        return auth_key
    return False