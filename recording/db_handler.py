# coding: utf-8


import boto3 


class DynamoDB(object):

    def __init__(self, arg):
        self.conn = boto3.resource('dynamodb', region_name='ap-northeast-2')

    def create_table(
            self, table_name, hash_name, 
            read_throughput=5, write_throughput=5):
        
        dynamodb = self.conn
        
        #table = dynamodb.create_table(
        #        TableName=table_name,
        #        Key
