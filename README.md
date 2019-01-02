# simple_vms
A simple system to manage Unifi vouchers, receive payment via whatever means and send voucher to client via SMS.

This code helps to manage acess to a WiFi network via a Unifi Controller. More information on the Unifi Wi Fi system can be found here: https://www.ubnt.com/products/#unifi  

Many times, integrating to a payment API can be a challenge for administrators. I propose a workaround here. For any payment received towards use of the network, an SMS notification is usually sent by the payment provider, whether Paypal, Visa, MPESA etc to the recipient. This SMS is received on a mobile phone, and with an SMS autoforward application, this SMS can be forwarded to your email address every time a payment is received. I prefer to use the [AutoForwardSMS](https://autoforwardsms.com/) app, available on Android Play Store. To avoid flooding your inbox, I propose to set up a new folder on your email account, and forward the relevant SMSs to that folder, then use the Gmail API to check for new messages on that folder. I use Gmail here. In the AutoforwardSMS app, it is possible to filter the messages so that only relevant messages are forwarded to your email.

Once the SMS is forwarded to your e-mail, you run this python script to extract from the email message the amount paid and the mobile number of the customer.

Every week (or daily depending on how frequent the vouchers are purchased), I extract from the Unifi controller the vouchers list for each payment duration and write this table to an SQLite database. The voucher management script takes the payment info, and using that selects from the SQLite database one voucher code with duration validity corresponding to the payment. To avoid using the same voucher multiple times, the script automatically deletes that voucher code from the SQLite table.

This information is then sent by SMS to the customer. For this, I used Infobip API, though any bulk SMS provide should easily provide this functionality.
