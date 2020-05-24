# ah-delivery-notifier

This Python script helps you get notified for available delivery spots for Albert Heijn Home Delivery (AH Bezorgservice).

### Why did I need this?
It was almost impossible to find free spots in AH Home Delivery due to Corona times. I just wanted something to let me know when there is a free spot in my preferred dates. Then I built this script so that I can run it via a scheduler so that it can let me know when there is availability.

## 1. Install the requirements

`pip install -r requirements.txt`



## 2. Create a config.ini file
An example config.ini file for gmail smtp:
```
[smtp]
server = smtp.gmail.com
port = 587
username = your-gmail-address@gmail.com
password = your-gmail-password
```


## 3. How to run

Command Line Arguments:
* An email address
* Your postcode in 1000XX format
* From Date: A preferred start date in ISO format (inclusive)
* End Date: A preferred end date in ISO format (inclusive)

`python ah_delivery_notifier\ah_delivery_notifier.py your-email@gmail.com 1000XX 2020-05-24 2020-05-27`

When there are available spots between preferred dates, you will receive an email including date, time and delivery costs. Then you can go to ah.nl and claim your spot **ASAP!**.