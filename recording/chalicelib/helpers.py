# coding: utf-8 


import datetime
from typing import Dict

from chalicelib.db_handler import DynamoDB
from chalicelib.utils import (
    generate_key, make_user_id
)

import boto3
from boto3.dynamodb.conditions import Key


def sign_up_or_login(social_id:str, social_type:str):
    db = DynamoDB()

    app_name = 'recording'
    table_name = 'user'

    user_id = make_user_id(social_id, social_type)

    query_item = {
        'name': 'id',
        'value': user_id
    }

    users = db.scan_item(app_name, table_name, query_item)
    if users:
        return users[0]['auth_key']

    auth_key = generate_key(64)
    item = {
        'id': user_id,
        'auth_key': auth_key
    }

    result = db.insert_item(app_name, table_name, item)
    if result:
        return auth_key
    return False


def save_record(file_name:str, user_id: str, body):
    BUCKET = 'record-file-seul'

    tmp_file_name = '/tmp/' + file_name
    with open(tmp_file_name, 'wb') as tmp_file:
        tmp_file.write(body)

    s3_client = boto3.client('s3')
    
    now = datetime.datetime.now()

    file_type = ''
    if '.' in file_name:
        file_type = '.' + file_name.split('.')[-1]
    
    s3_file_name = 'record/{}_{}{}'.format(user_id, now.strftime('%Y-%m-%d_%H-%M-%S'), file_type)
    s3_client.upload_file(tmp_file_name, BUCKET, s3_file_name)
    s3_client.put_object_acl(ACL='public-read', Bucket=BUCKET, Key=s3_file_name)

    url = 'https://s3.ap-northeast-2.amazonaws.com/%s/%s' % (BUCKET, s3_file_name)

    db = DynamoDB()

    s3_key = s3_file_name.split('/')[-1]

    result = db.insert_item(
        'recording',
        'recording', 
        {
            'id': s3_key,
            'user_id': user_id,
            'file_name': file_name,
            'created_at': now.strftime('%Y-%m-%d')
        }
    )
    if result:
        return True
    return False


def delete_recording(record_id:int, user_id:int):

    db = DynamoDB()

    app_name = 'recording'
    table_name = 'recording'

    item = {
        'id': record_id,
        'user_id': user_id
    }

    result = db.delete_item(app_name, table_name, item)
    if result:
        BUCKET = 'record-file-seul'
        s3 = boto3.resource('s3')

        s3_key = 'record/{}'.format(record_id)
        s3.Object(BUCKET, key=s3_key).delete()
        return True
    return False 


def get_records(user):
    db = DynamoDB()
    return db.scan_item(
        'recording',
        'recording',
        {
            'name': 'user_id',
            'value': user['id']
        }
    )
