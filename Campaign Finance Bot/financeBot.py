import json
import requests
import os
slackUrl = os.environ["SLACK_URL"]
response = requests.get('http://54.213.83.132/hackoregon/http/all_new_transactions/5/')
data = response.json()

greeting={"text": "Here's the top 5 transactions for the last few days."}
requests.post(slackUrl, json.dumps(greeting), headers={'content-type': 'application/json'})

for value in data:
	date = value['tran_date']
	transType = value['sub_type']
	amount = '${:,}'.format(value['amount'])
	payee = value['contributor_payee']
	filer = value['filer']
	purpose = value['purp_desc']
	if transType == 'Cash Contribution':
		color = '#36a64f'
		message = "%s gave %s to %s on %s" % (filer, amount, payee, date)
	elif transType == 'Cash Expenditure':
		color = '#B21627'
		message = "%s expensed %s on %s on %s" % (filer, amount, payee, date)
	else:
		color = '#414243'
		message = "A %s of %s from %s to %s on %s" % (transType, amount, filer, payee, date)
	payload = {
		# "fallback": "Here's the top 10 transactions for the last few days.",
		# "text": "Here's the top 10 transactions for the last few days.",
		# "pretext": "Here's the top 10 transactions for the last few days.",
		"color": color,
		"fields": [
			{
				"title": transType,
				"value": message
				# "short": false
			}
		]
	}
	req = requests.post(slackUrl, json.dumps(payload), headers={'content-type': 'application/json'})
