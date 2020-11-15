import os
import slackweb

def notifySystem():
  os.system("osascript -e 'display notification \"チケットサイトに入れました！！！\"'")

def notifySlackForHotel():
  slack = slackweb.Slack(url=os.environ['DISNEY_WEBHOOK_URL'])
  slack.notify(text="<@U01CYBK69L7> ホテルの予約サイトに入れました！")

def notifySlackForRest():
  slack = slackweb.Slack(url=os.environ['DISNEY_WEBHOOK_URL'])
  slack.notify(text="<@U01CYBK69L7> レストランの予約サイトに入れました！")