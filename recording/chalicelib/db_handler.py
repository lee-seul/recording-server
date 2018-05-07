# coding: utf-8


from typing import Dict, List

from chalicelib.utils import make_table_name, make_update_expr

import boto3 
from boto3.dynamodb.conditions import Key


class DynamoDB(object):

    def __init__(self):
        self.conn = boto3.resource('dynamodb', region_name='ap-northeast-2')

    def create_table(
            self, app_name:str, table_name:str, hash_dict:Dict, attrs:List,
            range_dict:Dict=None, read_throughput:int=1, write_throughput:int=1):
        """
            attrs = [
                {
                    "AttributeName": String,
                    "AttributeType": "S(문자), N(숫자), B(바이너리)"
                },
            ]
        """
        dynamodb = self.conn

        table_name = make_table_name(app_name, table_name)     
        attrs += [hash_dict]
        key_schema = [
            {
                'AttributeName': hash_dict['AttributeName'],
                'KeyType': 'HASH'
            }
        ]

        if range_dict is not None:
            attrs += [range_dict]
            key_schema += [
                {
                    'AttributeName': range_dict['AttributeName'],
                    'KeyType': 'RANGE'
                }
            ]
        table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attrs,
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_throughput,
                    'WriteCapacityUnits': write_throughput
                } 
            )
        return table

    def insert_item(self, app_name:str, table_name:str, item:Dict):
        dynamodb = self.conn 

        table_name = make_table_name(app_name, table_name)     
        table = dynamodb.Table(table_name)

        response = table.put_item(Item=item)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        return False

    def get_item(self, app_name:str, table_name:str, query_item:Dict):        
        dynamodb = self.conn

        table_name = make_table_name(app_name, table_name)     
        table = dynamodb.Table(table_name)

        response = table.get_item(Key=query_item)

        if not 'Item' in response:
            return None
            
        item = response['Item']
        return item

    def update_item(self, app_name:str, table_name:str, key_dict:Dict, update_data:List):
        dynamodb = self.conn

        table_name = make_table_name(app_name, table_name)
        table = dynamodb.Table(table_name)

        update_expr, expr_attr_values = make_update_expr(update_data)

        response = table.update_item(
            Key=key_dict,
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_attr_values
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        return False 

    def delete_item(self, app_name:str, table_name:str, item_key:Dict):
        dynamodb = self.conn 

        table_name = make_table_name(app_name, table_name)
        table = dynamodb.Table(table_name)

        response = table.delete_item(Key=item_key)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        return False 

    def query_item(self, app_name:str, table_name:str, partition_key:Dict, sort_key:Dict=None):
        dynamodb = self.conn

        table_name = make_table_name(app_name, table_name)
        table = dynamodb.Table(table_name)

        pk = partition_key['name']
        pkv = partition_key['value']

        if range_key is None:
            response = table.query(
                KeyConditionExpression=Key(pk).eq(pkv)
            )
        else:
            sk = sort_key['name']
            skv = sort_key['value']
            response = table.query(
                KeyConditionExpression=Key(sk).eq(skv) &
                Key(pk).eq(pkv)
            )            
        
        items = response['Items']

        return items