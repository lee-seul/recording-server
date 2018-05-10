# coding: utf-8


from chalicelib.db_handler import DynamoDB


APP_NAME = 'recording'


def create_user_table():
    db = DynamoDB()
    
    table_name = 'user'    
    hash_dict = {
        'AttributeName': 'id',
        'AttributeType': 'S'
    }

    range_dict = {
        'AttributeName': 'auth_key',
        'AttributeType': 'S'
    }

    attrs = []
    table = db.create_table(APP_NAME, table_name, hash_dict, attrs, range_dict=range_dict)

    print(table)


def create_recording_table():
    db = DynamoDB()
    table_name = 'recording' 

    hash_dict = {
        'AttributeName': 'id',
        'AttributeType': 'S',
    }

    range_dict = {
        'AttributeName': 'user_id',
        'AttributeType': 'S'
    }

    # KeySchema에 없는 내용을 AtrributeDefinitions에 넣을 경우 Index를 만들어줘야함
    """
    attrs = [
        {
            'AttributeName': 'created_at',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'record_url',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
    ]
    """

    attrs = []
    table = db.create_table(APP_NAME, table_name, hash_dict, attrs, range_dict=range_dict)
    
    print(table)


if __name__ == '__main__':
    create_user_table()
    create_recording_table()
