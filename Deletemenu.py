# -*- coding: utf-8 -*-

import boto3
import json


def handler(event, context):
    table = boto3.resource('dynamodb', region_name='us-west-2').Table('menu')
    table.delete_item(Key={'menu_id': event['menu_id']})
    return "200 OK"

