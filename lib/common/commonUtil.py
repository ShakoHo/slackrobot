import os
import json


def query_api_id_name_mapping(slack_client, input_query_data, mapping_fn, query_method, query_data_list_name,
                              query_data_return_key):
    query_key = input_query_data.keys()[0]
    query_key_value = input_query_data[query_key]
    api_call = slack_client.api_call(query_method)
    return_query_name = "Unknown"
    if mapping_fn:
        if os.path.exists((mapping_fn)):
            with open(mapping_fn) as fh:
                mapping_dict = json.load(fh)
        else:
            mapping_dict = {}
        if query_key_value in mapping_dict:
            return_query_name = mapping_dict[query_key_value]
        else:
            if api_call.get('ok'):
                # retrieve all users so we can find our bot
                users = api_call.get(query_data_list_name)
                for user in users:
                    if query_key in user and user.get(query_key) == query_key_value:
                        return_query_name = user.get(query_data_return_key)
                        mapping_dict[query_key_value] = return_query_name
        with open(mapping_fn, 'w+') as write_fh:
            json.dump(mapping_dict, write_fh)
    else:
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get(query_data_list_name)
            for user in users:
                if query_key in user and user.get(query_key) == query_key_value:
                    return_query_name = user.get(query_data_return_key)
    return return_query_name


def get_user_name(slack_client, input_user_id, mapping_fn=None):
    return query_api_id_name_mapping(slack_client, {'id': input_user_id}, mapping_fn, "users.list", "members", "name")


def get_channel_name(slack_client, input_channel_id, mapping_fn=None):
    return query_api_id_name_mapping(slack_client, {'id': input_channel_id}, mapping_fn, "channels.list", "channels", "name")