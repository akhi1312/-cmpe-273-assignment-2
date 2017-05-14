# -*- coding: utf-8 -*-

import boto3
import json


def handler(event, context):
    table = boto3.resource('dynamodb', region_name='us-west-2').Table('menu')

    sequence = '["selection", "size"]'
    item = {
               'menu_id':event['menu_id'],
               'store_name':event['store_name'],
               'selection':event['selection'],
               'size':event['size'],
               'price':event['price'],
               'store_hours':event['store_hours'],
               'sequence' : json.loads(sequence)
       }
 
    table.put_item(Item=item)
    print item
    return " 200 OK "
