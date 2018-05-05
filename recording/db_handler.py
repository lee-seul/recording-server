# coding: utf-8


import boto3 


class DynamoDB(object):

    def __init__(self, arg):
        self.conn = boto3.resource('dynamodb', region_name='ap-northeast-2')

    def create_table(
            self, table_name, hash_dict, range_dict, attrs,
            read_throughput=5, write_throughput=5):
        
        dynamodb = self.conn
        
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


