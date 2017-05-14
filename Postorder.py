# -*- coding: utf-8 -*-


import boto3
import json
import time
from time import strftime


def handler(event, context):
    order_table = boto3.resource('dynamodb').Table('order')
    keys = {'menu_id', 'order_id', 'customer_name', 'customer_email'}
    if all(key in event for key in keys):
      event['order_status'] = 'processing'
      current_time = strftime("%m-%d-%Y@%H:%M:%S", time.localtime())
      order = {}
      order['selection'] = 'empty'
      order['size'] = 'empty'
      order['cost'] = 'empty'
      order['order_time'] = current_time
      

      event['order'] = order

      order_table.put_item(Item=event)
      menu_table = boto3.resource('dynamodb').Table('menu')
      selection = menu_table.get_item(Key={'menu_id': event['menu_id']}).get('Item').get('selection')
      for i in range(0, len(selection)):
        selection[i] = str(i+1) + ". " + selection[i]
      selection_str = ", ".join(selection)
      response = {}
      response['Message'] = 'Hi ' + event.get('customer_name') + ', please choose one of these selection:  ' + selection_str
      return response
    else:
      return "Invalid Menu id"

