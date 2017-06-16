import os
import sys
import tee
import time
import json
import urllib2
from datetime import date, timedelta
from slackclient import SlackClient


class SlackBot(object):

    DEFAULT_slack_config_fn = "config.json"
    DEFAULT_READ_WEBSOCKET_DELAY = 1
    DEFAULT_SUPPORT_COMMAND_DICT = {'explosion': 'explosion_command',
                                    'status': 'status_command',
                                    'blame': 'blame_command'}

    def __init__(self):
        config = self.load_config()
        if config:
            self.slack_client = SlackClient(config['api-token'])
            self.at_bot_str = "<@" + config['bot-id'] + ">"
        else:
            print "Can't find config.json file"
            sys.exit(1)

    def send_url_data(self, url_str):
        DEFAULT_URL_HEADER = {'User-Agent': "Megumin slack robot url query"}
        request_obj = urllib2.Request(url_str, headers=DEFAULT_URL_HEADER)
        try:
            response_obj = urllib2.urlopen(request_obj)
        except Exception as e:
            print "Send post data failed, error message [%s]" % e.message
            return None
        if response_obj.getcode() == 200:
            return response_obj
        else:
            print "response status code is [%d]" % response_obj.getcode()
            return None

    def load_config(self):
        config_json = None
        if os.path.exists(self.DEFAULT_slack_config_fn):
            with open(self.DEFAULT_slack_config_fn) as fh:
                config_json = json.load(fh)
        return config_json

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.at_bot_str in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(self.at_bot_str)[1].strip().lower(), \
                           output['channel']
        return None, None

    def blame_command(self, input_command_str):
        c_list = input_command_str.split(" ")
        if len(c_list) == 2:
            return "Blame %s!" % c_list[1]
        else:
            return "Stop blaming everyone!! Everything is your fault!!!(>_>) "

    def explosion_command(self, input_command_str):
        return "http://www.anime-evo.net/wp-content/uploads/2016/03/Konosuba_10_18.jpg"

    def status_command(self, input_command_str):
        yesterday_date = date.today() - timedelta(1)
        yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')
        query_keyword = input_command_str.split(" ")[1]
        query_cmd = "python query_data_from_perfherder.py --keyword=%s --begin-date=%s" % (query_keyword, yesterday_date_str)
        print "status_command: %s" % query_cmd
        returncode, output = tee.system2(query_cmd)
        if returncode == 0:
            if len(output) > 1:
                try:
                    return_str = ""
                    print output
                    print_json = json.loads("".join(output))
                    for date_str in print_json:
                        for b_type in print_json[date_str]:
                            for platform_str in print_json[date_str][b_type]:
                                return_str += '{:30s} {:15s} {:20s} {:30s}\n'.format(date_str, b_type, platform_str, print_json[date_str][b_type][platform_str])
                    return return_str
                except:
                    return ".. Ah, Houston, we've had a problem."
            else:
                return ".. Ah, Houston, we've had a problem."
        else:
            return ".. Ah, Houston, we've had a problem."


    def handle_command(self, command, channel):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        current_command = None
        for supported_command in self.DEFAULT_SUPPORT_COMMAND_DICT:
            if command.startswith(supported_command):
                current_command = supported_command
                break
        if current_command:
            response_text = self.__getattribute__(self.DEFAULT_SUPPORT_COMMAND_DICT[current_command])(command)
        else:
            response_text = "I'm sorry, my responses are limited. You must ask the right question."
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response_text, as_user=True)

    def run(self):
        if self.slack_client.rtm_connect():
            print("Slack robot connected and running!")
            while True:
                command, channel = self.parse_slack_output(self.slack_client.rtm_read())
                if command and channel:
                    self.handle_command(command, channel)
                time.sleep(self.DEFAULT_READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")

if __name__ == "__main__":
    slackbot_obj = SlackBot()
    slackbot_obj.run()