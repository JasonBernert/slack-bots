import json
import requests
import os

# Set up incoming webhooks on Slack to get a URL for your team: https://api.slack.com/incoming-webhooks
slackUrl = os.environ["SLACK_URL"]

# Declare the API endpoint for requests
response = requests.get('http://54.213.83.132/hackoregon/http/all_new_transactions/5/')
data = response.json()

# The initial message is first posted as a simple text defined by greeting
greeting={"text": "Here's the top 5 transactions for the last few days."}
requests.post(slackUrl, json.dumps(greeting), headers={'content-type': 'application/json'})

# Loop through our data declaring and formating values for the message
for value in data:
	date = value['tran_date']
	transType = value['sub_type']
	amount = '${:,}'.format(value['amount'])
	payee = value['contributor_payee']
	filer = value['filer']
	purpose = value['purp_desc']
	# Look for the type of transaction to label and color code the Slack message attachment
	if transType == 'Cash Contribution':
		color = '#36a64f'
		message = "%s gave %s to %s on %s" % (filer, amount, payee, date)
	elif transType == 'Cash Expenditure':
		color = '#B21627'
		message = "%s expensed %s on %s on %s" % (filer, amount, payee, date)
	else:
		color = '#414243'
		message = "A %s of %s from %s to %s on %s" % (transType, amount, filer, payee, date)
	# Each transaction is posted as at message attachment: https://api.slack.com/docs/attachments
	payload = {
		"color": color,
		"fields": [
			{
				"title": transType,
				"value": message
			}
		]
	}
	req = requests.post(slackUrl, json.dumps(payload), headers={'content-type': 'application/json'})
