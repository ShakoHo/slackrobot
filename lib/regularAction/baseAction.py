class BaseAction(object):
    def __init__(self, slack_client, action_config, default_report_channel):
        self.slack_client = slack_client
        self.action_config = action_config
        self.default_report_channel = default_report_channel

    def run(self, **kwargs):
        pass