from python_graphql_client import GraphqlClient
import asyncio
import os
import requests
import time

headers={'Authorization': "5RVds5Cr_tawIiIBb6Itmi6BbVah54xszU62aqA94yQ"}

def print_handle(data):
    print(data["data"]["liveMeasurement"]["timestamp"]+" "+str(data["data"]["liveMeasurement"]["power"]))
    tall = (data["data"]["liveMeasurement"]["power"])
    if tall >= 8000:
        print("OK")
        # schedule async task from sync code
        asyncio.create_task(send_push_notification(data))
        print("msg sent")
        asyncio.create_task(sleep())

client = GraphqlClient(endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions")

query = """
subscription{
  liveMeasurement(homeId:"b2b3cc2a-caa5-4185-94a4-9ebf645195e1"){
    timestamp
    power
    
  }
}
"""

query2 = """
mutation{
  sendPushNotification(input: {
    title: "Advarsel! Høyt forbruk",
    message: "Du bruker 8kw eller mer",
    screenToOpen: CONSUMPTION
  }){
    successful
    pushedToNumberOfDevices
  }
}
"""
async def sleep():
    await asyncio.sleep(300)

async def send_push_notification(data):
    #maybe update your query with the received data here
    await client.execute_async(query=query2,headers={'Authorization': "5RVds5Cr_tawIiIBb6Itmi6BbVah54xszU62aqA94yQ"}) #pass whatever other params you need

async def main():
    await client.subscribe(query=query, headers={'Authorization': "5RVds5Cr_tawIiIBb6Itmi6BbVah54xszU62aqA94yQ"}, handle=print_handle)
    
asyncio.run(main())
