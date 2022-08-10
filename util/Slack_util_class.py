#from util import AK_log
import os, time, json

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
# pip install slack_sdk
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# pip install tqdm
from tqdm import trange

class Slack_instance:
    homedir = os.path.expanduser('~')
    def __init__(self, log, args=None, bot_token="nosync_userinput.json"):
        self.log = log
        log.debug('Slack Instance - Started')
        if args:
            self.args = args
            self.dryrun = not args.Execute
        
            with open(args.filename, 'r') as f:
                self.user_prop = json.load(f)
        else:
            self.dryrun = False
            self.user_prop={"SLACK_BOT_TOKEN":bot_token}
        
        #GetSlack
        #self.slack = AK_slack.AKSlack(self.user_prop["SLACK_BOT_TOKEN"])
        self.client = WebClient(token=self.user_prop["SLACK_BOT_TOKEN"])
        
        return

    # Destructor
    def __del__(self):
        self.log.info('Slack Instance - Exit')
        return
    
    def do_actions(self): 
        if self.args.CleanChannel:
            self.delete_channel_messages(self.args.CleanChannel)
        
        return 0

    def channel_id(self, channel_name):
        """Returns channel id for the specified channel name

        Args:
            channel_name (str): Name of the slack channel

        Returns:
            str: Channel ID
        """
        channel_list = {
            "python":"CQA4X9HRR",
            "17784012912":"C0210FZAWFR",
            "daily":"C01LU7SPU8P",
            "general":"C72Q20UF3",
            "personal":"C01GFLQHU2C"
        }
        return channel_list[channel_name]

    def delete_channel_messages(self,channel):
        """Deletes all the messages in a channel. If dry-run, shows the number of messages that will be deleted on actual execution

        Args:
            channel (str): Channel Name

        Returns:
            int: Error code. 0 for OK, >0 indicates errors in execution.
        """
        err = 0
        messages = 0        #count for num of messages found
        deleted = 0         #count for deleted messages
        latest = 0          #latest ts
        client = self.client
        log = self.log
        channel_id = self.channel_id(channel)

        log.info("[CLEAN CHANNEL]Started.")

        #Get messages
        #https://api.slack.com/methods/conversations.history/code
        conversation_history = []
        
        try:
            while True:
                # Call the conversations.history method using the WebClient
                # conversations.history returns the first 100 messages by default
                # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
                result = client.conversations_history(channel=channel_id,latest=latest,limit=1000)

                conversation_history.extend(result["messages"])
                messages += len(result["messages"])
                if conversation_history == []:
                    log.info("[CLEAN CHANNEL]There are no conversations found in the channel.")
                    log.info("[CLEAN CHANNEL]Finished.")
                    return err
                latest = float(conversation_history[-1]["ts"]) + 0.000001

                if not result['has_more']:
                    break

                #Slack ratelimits this requests to 50 per min.
                time.sleep(1.1)

        except SlackApiError as e:
            log.error("[CLEAN CHANNEL]Error creating conversation: {}".format(e))
            err += 1
        
        if not self.dry:
            log.info(f"[CLEAN CHANNEL]{str(messages)} messages found. Attempting to clean all.")

            for i in trange(conversation_history):
                try:
                    message_id = conversation_history[i]["ts"]
                    # Call the chat.chatDelete method using the built-in WebClient
                    result = client.chat_delete(channel=channel_id,ts=message_id)
                    deleted += 1
                except SlackApiError as e:
                    log.error(f"[CLEAN CHANNEL]Error deleting message: {e}")
                    err += 1
                
            log.info(f'[CLEAN CHANNEL]Deleted {str(deleted)} messages.')
        
        else:
            log.info(f"[CLEAN CHANNEL]{str(messages)} messages found. No attempt will be made to clean due to the absence of -e flag.")
            
        log.info("[CLEAN CHANNEL]Finished.")
        return err

    def init_block(self):
        self.block = []
        return
    
    def msg(self, message, channel="python"):
        """Sends Slack message

        Args:
            message (str): Message to be sent
            channel (str, optional): Slack channel to send the message to. Defaults to "#python".
        """
        log = self.log
        err = 0

        try:
            response = self.client.chat_postMessage(
                channel=self.channel_id(channel),
                text=message
            )
            
            log.info(f'OK - Slack message sent: {message}')
            
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            log.error(f'NG - Slack message not sent: {str(e)}')
            #assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
            err = 1
            
        return err
    
        
    def add_text(self, text, image_url=None,image_alt_text=""):
        """Adds markdown element to block message

        Args:
            text (str): Text to display
            image_url (str, optional): Image to display. Defaults to None.
            image_alt_text (str, optional): Alt string for image. Defaults to "".
        """ 
        
        if not image_url:
            self.block.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }
            )
        else:
            self.block.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": image_url,
                        "alt_text": image_alt_text
                    }
                }
            )
            
        return
    
    def add_divider(self):
        """Adds divider to the block message
        """
        self.block.append(
            {
                "type": "divider"
            }
        )
        return
    
    
    def post_block(self, channel):
        """Posts the currently constructed block to slack chat

        Args:
            channel (str): Channel name
        """
        log = self.log
        err = 0
        try:
            response = self.client.chat_postMessage(channel=self.channel_id(channel),blocks=self.block)
            log.info(f'OK - Slack Block sent')
            
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            log.error(f'NG - Slack message not sent: {str(e)}')
            err = 1
        return err