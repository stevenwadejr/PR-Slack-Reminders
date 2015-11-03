#!/usr/bin/python

from slacker import Slacker
from reminders import Reminders
import config

def make_mentions(users):
    mentions = ''
    for user in users :
        if user in config.user_map and config.user_map[user] not in config.user_blacklist :
            mentions += '@' + config.user_map[user] + ' '
    return mentions

# Start the app 
reminders = Reminders(config.gh_access_token, config.org_repo)
slack = Slacker(config.slack_token)

for reminder in reminders.get_reminders():
    slack.chat.post_message(
        '#' + config.channel.replace('#', ''),
        '<%s|[PR #%d - %s]> needs attention %s' % (
            reminder['pr_link'], 
            reminder['number'], 
            reminder['title'], 
            make_mentions(reminder['users_to_remind'])
        ),
        link_names=1
    )