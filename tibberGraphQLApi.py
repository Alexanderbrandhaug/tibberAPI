from python_graphql_client import GraphqlClient
import asyncio
import time


last_notification_timestamp = 0
NOTIFICATION_INTERVAL = 5 * 60  # 5min - hvor frekvent du ønsker å bli varslet. 

def print_handle(data):
    global last_notification_timestamp
    print(
        data["data"]["liveMeasurement"]["timestamp"]
        + " "
        + str(data["data"]["liveMeasurement"]["power"])
    )
    tall = data["data"]["liveMeasurement"]["power"]
    current_time = time.time()
    if (
        tall >= 1000 #antall watt du ønsker notifikasjon ved
        and current_time - NOTIFICATION_INTERVAL > last_notification_timestamp
    ):
        print("OK")
        # schedule async task from sync code
        asyncio.create_task(send_push_notification(data))
        last_notification_timestamp = current_time
        
        

client = GraphqlClient(endpoint="wss://api.tibber.com/v1-beta/gql/subscriptions")

query = """
subscription{
  liveMeasurement(homeId:"hent egen nøkkel ved å gå til developer.tibber.com"){
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

async def send_push_notification(data):
    #maybe update your query with the received data here
    await client.execute_async(query=query2,headers={'Authorization': "generer egen nøkkel via developer.tibber.com"})
    

async def main():
    await client.subscribe(query=query, headers={'Authorization': "samme nøkkel som ovenfor"}, handle=print_handle)
    
asyncio.run(main())
