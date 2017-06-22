class BaseResponse(object):
    def __init__(self, slack_client, response_config, input_msg):
        self.slack_client = slack_client
        self.response_config = response_config
        self.input_msg = input_msg

    def cmd_response(self, at_bot_str, current_msg_obj, current_msg_content, current_msg_channel):
        pass