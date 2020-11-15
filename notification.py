import os
import slackweb

def notifySystem():
  os.system("osascript -e 'display notification \"チケットサイトに入れました！！！\"'")

def notifySlackForHotel():
  slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
  slack.notify(text="<@U01CYBK69L7> ホテルの予約サイトに入れました！")

def notifySlackForRest():
  slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
  slack.notify(text="<@U01CYBK69L7> レストランの予約サイトに入れました！")