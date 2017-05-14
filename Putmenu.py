# -*- coding: utf-8 -*-


import boto3

def handler(event, context):
        table = boto3.resource("dynamodb").Table("menu")
        menu_id = {"menu_id": event["menu_id"]}
        key = event["update"].keys()[0]
# Updating Menu Items 
        value = event["update"][key]
        table.update_item(Key=menu_id, UpdateExpression="SET #key = :val",ExpressionAttributeNames={"#key":key}, ExpressionAttributeValues={ ":val" :value})
        return "200 OK"
   