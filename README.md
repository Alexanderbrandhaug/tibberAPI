## tibberAPI

Connects to tibber-graphQL API and subscribes to live-data from Tibber pulse. 
Send push-notifications to your tibber-application on your cellphone when reaching a self-set Kw-threshold (effect). Then waits for n-amount of time before re-sending another message, given you're still above the said threshold. 


requirements: 
* Python interpretrer
* pip install graphqlclient
* pip install asyncio
* pip install python-time
* Tibber pulse & Tibber phone app

 
 *API keys generated from developer.tibber.com // Access token, and homeID (can be found in the API explorer when testing subscribing to live data).*








