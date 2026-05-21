import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from PureCloudPlatformClientV2.utils import sanitize_for_serialization
import os
import csv
import time
import subprocess
import importlib.util

######################## Authorisation #######################
region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_central_1
PureCloudPlatformClientV2.configuration.host = region.get_api_host()
apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(os.environ['GENESYSCLOUD_OAUTHCLIENT_ID'], os.environ['GENESYSCLOUD_OAUTHCLIENT_SECRET'])                                                                                       
authApi = PureCloudPlatformClientV2.AuthorizationApi(apiclient)

######################## Set Clients ########################
user_api   = PureCloudPlatformClientV2.UsersApi(apiclient)
search_api = PureCloudPlatformClientV2.SearchApi(apiclient)

######################## Search User ########################
def searchuser(user) :
    try:
        body = {"pageSize": 999, "query": [{"fields": ["name"], "type": "EXACT", "value": user}]}
        response = search_api.post_users_search(body)
        json_object = sanitize_for_serialization(response)
        user = json_object['results'][0]['id']
        return user
    except (ApiException, KeyError) as e :
        print(f'Cannot find user {user}')

######################## Update Utilisation ########################
def updateutilization(agent, msg_util, email_util) :
   try:
        body = {
  "utilization": {
    "message": {
      "maximumCapacity": msg_util,
      "interruptableMediaTypes": [
        "email"
      ],
      "includeNonAcd": "false"
    },
    "email": {
      "maximumCapacity": email_util,
      "interruptableMediaTypes": [
        "call",
        "callback",
        "message"
      ],
      "includeNonAcd": "false"
    }
  },
}
        response = user_api.put_routing_user_utilization(user_id=agent, body=body)
        return response
   except ApiException as e:
       print(e)

######################## Run Process ########################
def runscript() :
  try:
    with open('agents.csv', 'r') as f:
        file = csv.DictReader(f)
        for c in file:
            user = c['agent_name']
            msg_util = c['message_limit']
            email_util = c['email_limit']
            agent = searchuser(user)
            if not user : 
               return
            updateutilization(agent, msg_util, email_util)
            wait()
            print(f'User {user} updated')
  except (ApiException, KeyError, ValueError) as e:
    print(f'Error updating {user}. {e}')

######################## Wait Function ########################
def wait() :
     time.sleep(2)
     pass

######################## Initial Start ########################
def start() :
 print(
   r'''                           _     _    _ _   _ _ _           _   _             
     /\                   | |   | |  | | | (_) (_)         | | (_)            
    /  \   __ _  ___ _ __ | |_  | |  | | |_ _| |_ ___  __ _| |_ _  ___  _ __  
   / /\ \ / _` |/ _ \ '_ \| __| | |  | | __| | | / __|/ _` | __| |/ _ \| '_ \ 
  / ____ \ (_| |  __/ | | | |_  | |__| | |_| | | \__ \ (_| | |_| | (_) | | | |
 /_/    \_\__, |\___|_| |_|\__|  \____/ \__|_|_|_|___/\__,_|\__|_|\___/|_| |_|
           __/ |                                                              
          |___/                                                               
   '''
)

 try :
    print('Looking for Genesys Cloud SDK...')    
    wait()
    if importlib.util.find_spec("PureCloudPlatformClientV2") is not None :
        print('Genesys SDK is Intalled')
    else :
        print('''Genesys Cloud Python SDK not installed. Run 'pip install PureCloudPlatformClientV2' to install.''')
        exit()
    wait()
 except FileNotFoundError as e :
    print(e)
    exit()
 try :
    print('Looking for Client Credentials...')
    wait()    
    os.environ['GENESYSCLOUD_OAUTHCLIENT_ID'], os.environ['GENESYSCLOUD_OAUTHCLIENT_SECRET']
    print('Found Client Credentials')
    wait()
 except KeyError as e :
    print('Could not find Client Credentials in Environment Variables')
    exit()
 wait()
 print('Update agents.csv before continuing')
 wait()
 user_input = input('Enter yes to continue: ')
 if user_input == 'yes' :
    runscript()
 else:
    print('Process will now end. Update agents.csv and run app again')
    exit()
if __name__ == "__main__":
    start()

