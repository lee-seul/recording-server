# coding: utf-8


from typing import Dict, List

import boto3 


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

        table_name = '{}_{}'.format(app_name, table_name)        
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

    def insert_item(self, table_name:str, item:Dict):
        dynamodb = self.conn 

        table = dynamodb.Table(table_name)

        response = table.put_item(Item=item)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        return False

    def get_item(self, table_name, query_item):        
        dynamodb = self.conn
        table = dynamodb.Table(table_name)

        response = table.get_item(key=query_item)
        item = response['Item']
        return item

        