# coding: utf-8


from db_handler import DynamoDB


APP_NAME = 'recording'


def create_user_table():
    db = DynamoDB()
    
    table_name = 'user'    
    hash_dict = {
        'AttributeName': 'id',
        'AttributeType': 'S'
    }
    attrs = [
        {
            'AttributeName': 'auth_key',
            'AttributeType': 'S'
        }
    ]

    table = db.create_table(APP_NAME, table_name, hash_dict, attrs)
    print(table)


def create_recording_table():
    db = DynamoDB()
    table_name = 'recording' 

    hash_dict = {
        'AttributeName': 'user_id',
        'AttributeType': 'S'
    }
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

    table = db.create_table(APP_NAME, table_name, hash_dict, attrs)
    print(table)


if __name__ == '__main__':
    create_user_table()
    create_recording_table()