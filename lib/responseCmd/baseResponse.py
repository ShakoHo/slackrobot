class BaseResponse(object):
    def __init__(self, slack_client, full_msg_obj, cmd_config, current_content, current_channel, at_bot_str):
        self.slack_client = slack_client
        self.full_msg_obj = full_msg_obj
        self.cmd_config = cmd_config
        self.current_content = current_content
        self.current_channel = current_channel
        self.at_bot_str = at_bot_str

    def response(self):
        pass