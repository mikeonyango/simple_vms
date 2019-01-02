import sqlite3
import http.client
import requests
import json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

requests.packages.urllib3.disable_warnings()

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

conn = sqlite3.connect("vouchers.db")

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))
 
# Call the Gmail API
category = service.users().labels().list(userId='me').execute()

# Call the Gmail API, only get 1 of the the recent message ids
# First get the message id for the message
results = service.users().messages().list(userId='me', q ='in:SZMPESA', maxResults=1).execute()
 
# get the message id from the results object
message_id = results['messages'][0]['id']
 
# use the message id to get the actual message, including any attachments
message = service.users().messages().get(userId='me', id=message_id).execute()
 
# print (message)
a = (message['snippet'])
# print(a)
b = a.find("Ksh")
# print (b)
n = a.split("Ksh")[1]
# print (c)
d = n.split(".")[0]
print (d)
e = n.split ("from ")[1]
# print (e)
f= e[:12]
print (f)

#selecting from the list of voucher codes the duration for which the voucher code will be valid after first activation.
def select_voucher():
	amount = d #input("paid amount either 10, 50, 300 or 1000: ") #this is the amount received via API from payment via MPESA.
	amount = int(amount)

	if amount == 10:
		return ("1h")
	elif amount == 50:
		return ("1d")
	elif amount == 300:
		return ("1w")	
	elif amount == 1000:
		return ("1m")
	else:
		return ("try again")
validity = select_voucher()

#now selecting the actual voucher code valid for the duration specified above
query = f"SELECT code FROM voucherslist WHERE duration = '{validity}'"
c=conn.cursor()
c.execute(query)
code = c.fetchone()
#print(code)
x = str(code)
x = x[:-3]
x = x[-11:]

#deleting the selected voucher code so it is not selected for a second time.
query2 = f"DELETE FROM voucherslist WHERE code = '{x}'" 
c.execute(query2)

conn.commit()
conn.commit()
conn.close()

#generating text of SMS message to send to user purchasing voucher
def period():
	if validity == "1h":
		return ("1 hour")
	elif validity == "1d":
		return ("24 hours")
	elif validity == "1w":
		return ("7 days")
	elif validity == "1m":
		return ("1 month")
	else:
		return("not valid")

y = period()

def smstosend():
	if y == "not valid":
		return ("Sorry, your payment amount is incorrect, we'll refund within 24 hours. Please pay the exact amount.")
	else:
		return (f"{x} is your Speedzone voucher code, valid for up to 3 users, for {y} from time of first log in.")

z = smstosend()

con = http.client.HTTPSConnection("bulksmsapiurl")

payload = "{\"from\":\"WIFIPROVIDER\",\"to\":\""+f+"\",\"text\":\""+z+"\"}"

headers = {
    'authorization': "Basic masked==",
    'content-type': "application/json",
    'accept': "application/json"
    }

con.request("POST", "/sms/2/text/single", payload, headers)

res = con.getresponse()
data = res.read()

print(data.decode("utf-8"))
