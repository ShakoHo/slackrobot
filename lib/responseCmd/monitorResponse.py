import re
from baseResponse import BaseResponse
from lib.common.commonUtil import get_channel_name
from lib.common.commonUtil import get_user_name


class MonitorKeyword(BaseResponse):
    def monitor(self, channel_mapping_fn, user_mapping_fn):
        if self.input_msg and len(self.input_msg) > 0:
            for msg_data in self.input_msg:
                for keyword in self.response_config['default-keyword-list']:
                    if msg_data and 'text' in msg_data and msg_data['user'] not in self.response_config['default-userid-whilelist']:
                        re_compile_obj = re.compile(keyword)
                        re_match_obj = re_compile_obj.search(msg_data['text'])
                        if re_match_obj:
                            post_message = "[%s] %s say: %s" % (get_channel_name(self.slack_client, msg_data['channel'], channel_mapping_fn), get_user_name(self.slack_client, msg_data['user'], user_mapping_fn), msg_data['text'])
                            self.slack_client.api_call("chat.postMessage", channel=self.response_config['default-report-channel'], text=post_message, as_user=True)