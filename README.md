# Pull Request Slack Reminders

Grab pull requests for a repository and alert a channel in Slack if the open requests have gone too long without review.

## Sample Config

```
gh_access_token = 'github_access_token'
slack_token = 'slack_token'

org_repo = 'organization/repo'
channel = 'slack_channel'

# github : slack
user_map = {
    'github_username' : 'slack_username'
}
```