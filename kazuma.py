"""
Usage:
  kazuma.py [--config-file=<str>]
  kazuma.py (-h | --help)

Options:
  -h --help                 Show this screen.
  --config-file=<str>       Load specific config file path [default: kazuma.json]

"""
import re
import os
import sys
import time
import json
import importlib
from docopt import docopt
from slackclient import SlackClient


class SlackBot(object):

    def load_config(self, input_config_fp):
        config_json = None
        if os.path.exists(input_config_fp):
            with open(input_config_fp) as fh:
                config_json = json.load(fh)
        return config_json

    def init_variable(self, input_config):
        api_token_str = input_config.get('api-token', None)
        self.regular_actions_timestamp_recorder = {}
        if api_token_str:
            self.slack_client = SlackClient(api_token_str)
        else:
            print "Missing either api-token or bot-id value in config file!"
            sys.exit(1)

    def __init__(self, config_fp):
        if os.path.exists(config_fp):
            self.config = self.load_config(config_fp)
            if self.config:
                self.init_variable(self.config)
            else:
                print "Can't load configuration json file, exit(1)"
                sys.exit(1)
        else:
            print "Can't find config file path, exit(1)"
            sys.exit(1)

    def parse_input_message(self, input_message, at_bot_str):
        output_list = input_message
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and at_bot_str in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output, output['text'].split(at_bot_str)[1].strip().lower(), output['channel']
        return None, None, None

    def monitor_keywords(self, input_message, monitor_config, channel_mapping_fn, user_mapping_fn):
        module_class = getattr(importlib.import_module(monitor_config['module-path']), monitor_config['module-name'])
        module_obj = module_class(self.slack_client, monitor_config, input_message)
        module_obj.monitor(channel_mapping_fn, user_mapping_fn)

    def response_commands(self, input_message, command_config, at_bot_str):
        current_handle_msg_obj, current_content, current_channel = self.parse_input_message(input_message, at_bot_str)
        if current_content and current_channel:
            current_command = None
            for supported_command_regex_pattern in command_config['command-settings']:
                re_compile_obj = re.compile(supported_command_regex_pattern)
                re_match_obj = re_compile_obj.search(current_content)
                if re_match_obj:
                    current_command = supported_command_regex_pattern
                    break
            if current_command:
                module_path = command_config['command-settings'][current_command]['module-path']
                module_name = command_config['command-settings'][current_command]['module-name']
            else:
                module_path = command_config['default-response-cmd-module-path']
                module_name = command_config['default-response-cmd-module-name']
            module_class = getattr(importlib.import_module(module_path), module_name)
            module_obj = module_class(self.slack_client, command_config, input_message)
            module_obj.cmd_response(at_bot_str, current_handle_msg_obj, current_content, current_channel)

    def rtm_actions_handler(self, input_message):

        self.monitor_keywords(input_message, self.config['monitor-keyword-config'], self.config['default-channel-mapping-fn'], self.config['default-user-mapping-fn'])

        self.response_commands(input_message, self.config['response-command-config'], self.config['at-bot-str'])

        time.sleep(self.config.get('default-read-websocket-delay', 1))

    def regular_actions_handler(self, regular_actions_config):
        for regular_action_module_name in regular_actions_config['action-settings']:
            previous_timestamp = self.regular_actions_timestamp_recorder.get(regular_action_module_name, None)
            alert_interval = regular_actions_config['action-settings'][regular_action_module_name].get('alert-interval', None)
            current_trigger_flag = False
            record_current_timestamp_flag = False
            if previous_timestamp:
                if time.time() - previous_timestamp >= alert_interval:
                    current_trigger_flag = True
                    record_current_timestamp_flag = True
            else:
                if alert_interval is None:
                    current_trigger_flag = True
                    record_current_timestamp_flag = False
                else:
                    current_trigger_flag = True
                    record_current_timestamp_flag = True

            if current_trigger_flag:
                regular_action_module_path = regular_actions_config['action-settings'][regular_action_module_name][
                    'module-path']
                module_class = getattr(importlib.import_module(regular_action_module_path), regular_action_module_name)
                module_obj = module_class(self.slack_client,
                                          regular_actions_config['action-settings'][regular_action_module_name],
                                          regular_actions_config['default-report-channel'])
                module_obj.run()
                if record_current_timestamp_flag:
                    self.regular_actions_timestamp_recorder[regular_action_module_name] = time.time()

    def run(self):
        if self.slack_client.rtm_connect():
            print("Kazuma is online!!!")
            while True:
                current_message = self.slack_client.rtm_read()

                # real time message based action handler
                self.rtm_actions_handler(current_message)

                # regular based action handler
                self.regular_actions_handler(self.config['regular-action-config'])

        else:
            print("Connection failed. Invalid Slack token or bot ID?")


def main():
    arguments = docopt(__doc__)
    slackbot_obj = SlackBot(arguments['--config-file'])
    slackbot_obj.run()

if __name__ == "__main__":
    main()
