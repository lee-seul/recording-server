# coding: utf-8


import string
import random
from typing import Dict, List


KEY_SOURCE = string.ascii_letters + string.digits


def make_table_name(app_name:str, table_name:str):
    return '{}_{}'.format(app_name, table_name)


def make_update_expr(update_data:List):
    expr = 'SET'
    last = len(update_data) - 1
    
    expr_attr_values = {}
    for idx, data in enumerate(update_data):
        expr += ' {} = :val{}'.format(data['attribute'], idx+1)
        if not idx == last:
            expr += ','
        key = 'val' + str(idx+1)
        expr_attr_values[key] = data['value']

    return expr, expr_attr_values 


def generate_key(n:int):
    return ''.join(random.choice(KEY_SOURCE) for _ in range(n))


def make_user_id(social_id:str, social_type:str):
    return '{}_{}'.format(social_type, social_id)

