# AutoJira

auto jira code

# Config

create a config.yaml file

jira_url: "https://gubagoo.atlassian.net"
email: "first.last@gubagoo.com"
api_token: ""
user_account_id: "first.last"
open_ai_api_key: "rdl-api-key"
chat_model: "gpt-4.1"

# set up environment

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# setting up cron

crontab -e
0 17 \* \* 1-5 /home/user/dir/automate_script.sh >> /home/user/dir/automation.log 2>&1

# automating script

project directory will need to change to the home directory you're in
