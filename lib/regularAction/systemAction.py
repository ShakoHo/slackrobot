import os
import psutil
import socket
from baseAction import BaseAction
from lib.common.commonUtil import post_message_to_slack


class MonitorDiskSpace(BaseAction):
    def run(self, **kwargs):
        current_percentage = psutil.disk_usage(os.path.abspath(os.sep)).percent
        if current_percentage > self.action_config['alert-percent']:
            current_host_name = socket.gethostname()
            response_text = "Host [%s] current disk space usage is [%s], exceed the alert percentage [%s]" % (current_host_name, str(current_percentage), str(self.action_config['alert-percent']))
            post_message_to_slack(self.slack_client, response_text, self.default_report_channel)

