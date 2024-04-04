import requests

url="https://pt.airbnb.com/api/v2/listings?user_id=12730028"

headers= {

    "X-Airbnb-API-Key":"d306zoyjsyarp7ifhu67rjxn52tv0t20"

}

response=requests.get(url,headers=headers)

lista= []

if response.status_code==200:
    data=response.json()
   
# Retrieve all ids of listing properties 
for x in data['listings']:
    lista.append(x['listing_id_str'])

print(lista)