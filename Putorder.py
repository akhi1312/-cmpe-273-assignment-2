# -*- coding: utf-8 -*-


import boto3
import json


def handler(event, context):
  keys = {'input'}
  #Make sure the API is correct
  if all(key in event for key in keys):
    response = {}
    order_table = boto3.resource('dynamodb', region_name='us-west-2').Table('order')
    menu_table = boto3.resource('dynamodb', region_name='us-west-2').Table('menu')

    item = order_table.get_item(Key={'order_id': event['order_id']}).get('Item')
    if item == None:
      response['Message'] = 'Order does not exist'
      return response
    #fetch order details
    order = item.get('order')
    
    menu_id = item.get('menu_id')
    #Check wether order selection is emply or not 
    if order.get('selection') == 'empty':
      #updating table with selection
      selection = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('selection')[int(event.get('input'))-1]
      order['selection'] = selection
      sizes = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('size')
      for i in range(0, len(sizes)):
        sizes[i] = str(i+1) +". " + sizes[i]
      sizes_str = ", ".join(sizes)
      response['Message'] = 'Which size do you want? ' + sizes_str
    elif order.get('size') == 'empty':
      #update the table with the size
      size = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('size')[int(event.get('input'))-1]
      order['size'] = size
      cost = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('price')[int(event.get('input'))-1]
      order['cost'] = cost
      response['Message'] = 'Your order costs $' + cost + '. We will email you when the order is ready. Thank you!'
    else:
      response['Message'] = 'Your order has already been placed. We will email you when the order is ready. Thank you!'
      return response

    order_table.update_item(
      Key={'order_id': event['order_id']},
      UpdateExpression="SET #order = :ss",
      ExpressionAttributeNames={'#order': 'order'},
      ExpressionAttributeValues={':ss': order}
    )
    return response
    
  else:
    return "Invalid selections"
