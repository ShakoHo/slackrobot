# Slack Robot

Cover several robots which can help us monitor or do some automation things

## Usage

### Sample  
* Trigger Kazuma: `python kazuma.py`

### Usage
```
  kazuma.py [--config-file=<str>]
  kazuma.py (-h | --help)
```

### Options:

```
  -h --help                 Show this screen.
  --config-file=<str>       Load specific config file path [default: kazuma.json]  
```
 
#### Config file template
```
{
  "bot-id": "",
  "at-bot-str": "",
  "api-token": "",
  "default-read-websocket-delay": 1,
  "default-user-mapping-fn": "usermapping.json",
  "default-channel-mapping-fn": "channelmapping.json",
  "monitor-keyword-config":{
    "default-keyword-list": [""],
    "default-userid-whilelist": [""],
    "default-report-channel": ""
  },
  "response-command-config":{
    "command-settings":
    {
      "^snipe":
      {
        "module_path": "lib.responseCmd.animationResponse",
        "module_name": "ResponseSnipeCmd"
      },
      "[bB][lL][aA][mM][eE]":
      {
        "module_path": "lib.responseCmd.animationResponse",
        "module_name": "ResponseBlameCmd"
      }
    },
    "default-response-cmd-module-path": "lib.responseCmd.animationResponse",
    "default-response-cmd-module-name": "ResponseDefaultCmd"
  }
}
```

