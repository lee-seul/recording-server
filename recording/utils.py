# coding: utf-8


from typing import Dict


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
