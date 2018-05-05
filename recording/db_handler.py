# coding: utf-8


from typing import Dict, List

from .utils import make_table_name, make_update_expr

import boto3 
from boto3.dynamodb.conditions import Key


class DynamoDB(object):

    def __init__(self, arg):
        self.conn = boto3.resource('dynamodb', region_name='ap-northeast-2')

    def create_table(
            self, app_name:str, table_name:str, hash_dict:Dict, range_dict:Dict, attrs:List,
            read_throughput:int=5, write_throughput:int=5):
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
        attrs += [hash_dict, range_dict]

        table = dynamodb.create_table(
                TableName=table_name,
                AttrebuteDefinitions=attr,
                KeySchema=[
                    {
                        'AttributeName': hash_dict['AttributeName'],
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': range_dict['AttributeName'],
                        'KeyType': 'RANGE'
                    }
                ],
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

    def query_item(
        self, app_name:str, table_name:str, sort_key: Dict, partition_key:Dict,
        index_name=None, total_items=None, start_key=None, table=None
    ):

    if not table:
        dynamodb = self.conn 
        table_name = make_table_name(app_name, table_name)
        table = dynmodb.Table(table_name)
    
    sk = sort_key['name']
    skv = sort_key['value']
    pk = partition_key['name']
    pkv = partition_key['value']
    if not start_key:
        if index_name:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=Key(sk).eq(skv) &
                Key(pk).eq(pkv)
            )
        else:
            response = table.query(
                KeyConditionExpression=Key(sk).eq(skv) &
                Key(pk).eq(pkv)
            )
    else:
        if index_name:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=Key(sk).eq(skv) &
                Key(pk).eq(pkv),
                ExclusiveStartKey=start_key
            )
        else:
            response = table.query(
                KeyConditionExpression=Key(sk).eq(skv) &
                Key(pk).eq(pkv),
                ExclusiveStartKey=start_key
            )
            
    if not total_items:
        total_items = response['Items']
    else:
        total_items.extend(response['Items'])

    if response.get('LastEvaluatedKey'):
        start_key = response['LastEvaluatedKey']
        return_items = self.query_item(
            table_name=table_name, sort_key=sort_key,
            partition_key=partition_key, total_items=total_items,
            start_key=start_key, table=table
        )
        return return_items
    return total_item
