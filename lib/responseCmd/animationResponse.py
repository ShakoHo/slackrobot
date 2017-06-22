import time
from baseResponse import BaseResponse
from lib.common.commonUtil import get_user_name


class ResponseSnipeCmd(BaseResponse):
    def response(self):
        response_text = "https://68.media.tumblr.com/586e70e8281c0e00a34803217dfd4b50/tumblr_orabpvA6Fs1wp8qnmo1_500.gif?" + str(
            time.time())
        self.slack_client.api_call("chat.postMessage", channel=self.current_channel, text=response_text, as_user=True)


class ResponseBlameCmd(BaseResponse):
    def response(self):
        c_list = self.current_content.strip().split(" ")
        if len(c_list) > 1:
            response_text = "blame %s" % c_list[1].strip()
        else:
            response_text = "blame %s" % get_user_name(self.slack_client, self.full_msg_obj['user'])
        self.slack_client.api_call("chat.postMessage", channel=self.current_channel, text=response_text, as_user=True)


class ResponseDefaultCmd(BaseResponse):
    def response(self):
        response_text = "Hai! Kazuma desu!!!"
        self.slack_client.api_call("chat.postMessage", channel=self.current_channel, text=response_text, as_user=True)
