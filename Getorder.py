# -*- coding: utf-8 -*-


import boto3
import json

def handler(event, context):
  keys = {'order_id'}
  #Make sure the API is correct
  if all(key in event for key in keys):
      order_table = boto3.resource('dynamodb', region_name='us-west-2').Table('order')
      item = order_table.get_item(Key={'order_id': event['order_id']}).get('Item')
      return item
  else:
    return "Invalid Order Id"
