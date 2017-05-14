# -*- coding: utf-8 -*-


import boto3


def handler(event, context):
    table = boto3.resource('dynamodb', region_name='us-west-2').Table('menu')
    item = table.get_item(Key={'menu_id': event['menu_id']}).get('Item')
    return item
