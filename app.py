import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from PureCloudPlatformClientV2.utils import sanitize_for_serialization
import os
import csv
import time
import logging
import importlib.util

######################## Logging ########################
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

######################## Authorisation #######################
region = PureCloudPlatformClientV2.PureCloudRegionHosts.eu_central_1
PureCloudPlatformClientV2.configuration.host = region.get_api_host()


def get_api_client():
    return PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(
        os.environ['GENESYSCLOUD_OAUTHCLIENT_ID'], os.environ['GENESYSCLOUD_OAUTHCLIENT_SECRET']
    )


######################## Search User ########################
def searchuser(search_api, user):
    try:
        body = {"pageSize": 999, "query": [{"fields": ["name"], "type": "EXACT", "value": user}]}
        response = search_api.post_users_search(body)
        json_object = sanitize_for_serialization(response)
        results = json_object.get('results', [])
        if not results:
            logger.warning(f'No matching user found for "{user}"')
            return None
        if len(results) > 1:
            logger.warning(
                f'Multiple users found for "{user}" ({len(results)} matches); using the first result'
            )
        return results[0]['id']
    except (ApiException, KeyError) as e:
        logger.error(f'Cannot find user "{user}": {e}')
        return None


######################## Update Utilisation ########################
def updateutilization(user_api, agent, msg_util, email_util, retries=3):
    body = {
        "utilization": {
            "message": {
                "maximumCapacity": msg_util,
                "interruptableMediaTypes": ["email"],
                "includeNonAcd": False,
            },
            "email": {
                "maximumCapacity": email_util,
                "interruptableMediaTypes": ["call", "callback", "message"],
                "includeNonAcd": False,
            },
        },
    }

    delay = 2
    for attempt in range(1, retries + 1):
        try:
            return user_api.put_routing_user_utilization(user_id=agent, body=body)
        except ApiException as e:
            if e.status == 429 and attempt < retries:
                logger.warning(f'Rate limited updating agent {agent}, retrying in {delay}s...')
                time.sleep(delay)
                delay *= 2
                continue
            logger.error(f'Failed to update utilization for agent {agent}: {e}')
            return None


######################## Parse & Validate Row ########################
def parse_row(row):
    """Validate a single CSV row, returning (agent_name, msg_util, email_util) or None if invalid."""
    agent_name = (row.get('agent_name') or '').strip()
    if not agent_name:
        logger.error(f'Skipping row with missing agent_name: {row}')
        return None

    try:
        msg_util = int(row['message_limit'])
        email_util = int(row['email_limit'])
    except (KeyError, TypeError, ValueError):
        logger.error(f'Skipping "{agent_name}": message_limit/email_limit must be integers ({row})')
        return None

    if msg_util < 0 or email_util < 0:
        logger.error(f'Skipping "{agent_name}": limits must be non-negative ({row})')
        return None

    return agent_name, msg_util, email_util


######################## Run Process ########################
def run():
    api_client = get_api_client()
    search_api = PureCloudPlatformClientV2.SearchApi(api_client)
    user_api = PureCloudPlatformClientV2.UsersApi(api_client)

    try:
        with open('agents.csv', 'r') as f:
            rows = list(csv.DictReader(f))
    except (FileNotFoundError, OSError) as e:
        logger.error(f'Could not read agents.csv: {e}')
        return

    if not rows:
        logger.warning('agents.csv contains no data rows')
        return

    for row in rows:
        parsed = parse_row(row)
        if parsed is None:
            continue

        agent_name, msg_util, email_util = parsed
        agent_id = searchuser(search_api, agent_name)
        if not agent_id:
            continue

        result = updateutilization(user_api, agent_id, msg_util, email_util)
        if result is not None:
            logger.info(f'User {agent_name} updated')
        wait()


######################## Wait Function ########################
def wait():
    time.sleep(2)


########################  Start ########################
def start():
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

    print('Looking for Genesys Cloud Library...')
    wait()
    if importlib.util.find_spec("PureCloudPlatformClientV2") is not None:
        print('Genesys Cloud Library is Installed')
    else:
        print('''Genesys Cloud Library not installed. Run 'pip install -r requirements.txt' to install.''')
        return
    wait()

    if 'GENESYSCLOUD_OAUTHCLIENT_ID' not in os.environ or 'GENESYSCLOUD_OAUTHCLIENT_SECRET' not in os.environ:
        print('Could not find Client Credentials in Environment Variables')
        return
    print('Found Client Credentials')
    wait()

    print('Update agents.csv before continuing')
    wait()
    user_input = input('Enter yes to continue: ')
    if user_input.strip().lower() == 'yes':
        try:
            run()
        except ApiException as e:
            logger.error(f'Unexpected API error: {e}')
    else:
        print('Process will now end. Update agents.csv and run app again')


if __name__ == "__main__":
    start()
