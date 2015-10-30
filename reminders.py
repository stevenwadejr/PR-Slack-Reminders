import requests
import json
import arrow
import re

class Holder(object):
   def set(self, value):
     self.value = value
     return value
   def get(self):
     return self.value

class Reminders(object) :

    def __init__(self, gh_access_token, org_repo):
        self.gh_access_token = gh_access_token
        self.org_repo = org_repo
        self.max_pr_life = 60 * 60 * 24 * 2

    def get_pull_requests(self):
        headers = self.get_default_headers()
        params = {'state': 'open'}
        response = requests.get(
            'https://api.github.com/repos/' + self.org_repo + '/pulls',
            headers=headers,
            params=params
        )

        return response.json()

    def get_comments(self, url):
        return requests.get(
            url,
            headers=self.get_default_headers()
        ).json()

    def get_reminders(self):
        reminders = []
        pull_requests = self.get_pull_requests()
        for pr in pull_requests:
            users_to_remind = Holder()
            if self.is_old_pr(pr) and users_to_remind.set(self.needs_reminding(pr)):
                reminders.append(self.build_reminder(pr, users_to_remind.get()))


        return reminders

    def is_old_pr(self, pr):
        created_at = arrow.get(pr['created_at']).timestamp
        now = arrow.utcnow().timestamp

        return (now - created_at) > self.max_pr_life

    def needs_reminding(self, pr):
        found_users = re.findall(r"@([A-Za-z0-9_-]+)", pr['body'])
        users_who_commented = []

        for comment in self.get_comments(pr['_links']['comments']['href']):
            users_who_commented.extend(x for x in [comment['user']['login']] if x not in users_who_commented)

        return list(set(found_users) - set(users_who_commented))

    def build_reminder(self, pr, who_to_remind):
        return {
            'number': pr['number'],
            'title': pr['title'],
            'users_to_remind': who_to_remind,
            'pr_link': pr['html_url']
        }

    def get_default_headers(self):
        return {
            'Authorization': 'token %s' % self.gh_access_token,
        }