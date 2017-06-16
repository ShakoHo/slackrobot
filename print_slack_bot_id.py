import json
from slackclient import SlackClient


BOT_NAME = 'megumin'

with open('config.json') as fh:
    json_obj = json.load(fh)
slack_client = SlackClient(json_obj['api-token'])

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                with open('config.json', 'w+') as write_fh:
                    json_obj['bot-id'] = user.get('id')
                    json.dump(json_obj, write_fh)


    else:
        print("could not find bot user with the name " + BOT_NAME)

