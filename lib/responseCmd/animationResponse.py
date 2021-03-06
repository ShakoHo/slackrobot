import time
from baseResponse import BaseResponse
from lib.common.commonUtil import get_user_name
from lib.common.commonUtil import post_message_to_slack


class ResponseSnipeCmd(BaseResponse):
    def cmd_response(self, at_bot_str, current_msg_obj, current_msg_content, current_msg_channel):
        response_text = "https://68.media.tumblr.com/586e70e8281c0e00a34803217dfd4b50/tumblr_orabpvA6Fs1wp8qnmo1_500.gif?" + str(time.time())
        post_message_to_slack(self.slack_client, response_text, current_msg_channel)


class ResponseBlameCmd(BaseResponse):
    def cmd_response(self, at_bot_str, current_msg_obj, current_msg_content, current_msg_channel):
        c_list = current_msg_content.strip().split(" ")
        if len(c_list) > 1:
            response_text = "blame %s" % c_list[1].strip()
        else:
            response_text = "blame %s" % get_user_name(self.slack_client, current_msg_obj['user'])
        post_message_to_slack(self.slack_client, response_text, current_msg_channel)


class ResponseDefaultCmd(BaseResponse):
    def cmd_response(self, at_bot_str, current_msg_obj, current_msg_content, current_msg_channel):
        response_text = "Hai! Kazuma desu!!!"
        post_message_to_slack(self.slack_client, response_text, current_msg_channel)
