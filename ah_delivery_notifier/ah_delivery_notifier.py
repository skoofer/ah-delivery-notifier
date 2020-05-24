import smtplib
import requests
from datetime import datetime
import pytz
import configparser
from sys import argv


def smtp_config():
    smtp_config_obj = configparser.ConfigParser()
    smtp_config_obj.read('config.ini')
    return smtp_config_obj['smtp']


def send_email(email_data):
    config = smtp_config()
    username = config['username']
    password = config['password']
    server = smtplib.SMTP(config['server'], config['port'])
    server.ehlo()
    server.starttls()
    server.login(username, password)
    body = '\r\n'.join(['To: %s' % email_data['to'],
                        'From: %s' % username,
                        'Subject: %s' % email_data['subject'],
                        '', (email_data['body'])])

    server.sendmail(username, [(email_data['to'])], body)
    server.quit()


def get_ah_data(post_code):
    r = requests.get(f'https://www.ah.nl/service/rest/kies-moment/bezorgen/{post_code}')
    result = r.json()
    return result


def ah_data_converter(ah_data_dto):
    available_slots = []

    delivery_dates = ah_data_dto['_embedded']['lanes'][3]['_embedded']['items'][0]['_embedded']['deliveryDates']

    for delivery_date in delivery_dates:
        available_times = [{
            'from': delivery_time_slot['from'],
            'to': delivery_time_slot['to'],
            'value': delivery_time_slot['value']
        } for delivery_time_slot in delivery_date['deliveryTimeSlots']
            if delivery_time_slot['state'] == 'selectable']

        if len(available_times) > 0:
            available_slots.append(
                {
                    'date': delivery_date['date'],
                    'available_slots': available_times
                })

    return available_slots


def filter_available_dates(available_dates, date_start, date_end):
    return [available_date for available_date in available_dates
            if date_start <= available_date['date'] <= date_end]


def generate_email_data(filtered_ah_data, email_address, post_code):
    availabilities = [
        f"{available_date['date']}: between {available_slot['from']} and {available_slot['to']} for {available_slot['value']} EUR\n"
        for available_date in filtered_ah_data
        for available_slot in available_date['available_slots']]

    return {
        'to': email_address,
        'subject': f'New available Spots for {post_code} for AH Bezorgservice!',
        'body': f'''Hi,

There are new openings for you on AH Bezorgservice:
{''.join(availabilities)}
Good luck!'''
    }


def notify_available_slots(email_address, post_code, date_start, date_end):
    ah_dto = get_ah_data(post_code)

    available_dates = ah_data_converter(ah_dto)

    filtered_dates = filter_available_dates(available_dates, date_start, date_end)

    timestamp = datetime.now(tz=pytz.timezone("Europe/Amsterdam"))
    if len(filtered_dates) > 0:
        email_data = generate_email_data(filtered_dates, email_address, post_code)
        send_email(email_data)
        print(filtered_dates)
        print(f'[{timestamp}]: Email sent for {post_code} :)')
    else:
        print(f'[{timestamp}]: No availabilities for {post_code} :(')


if __name__ == '__main__':
    email_address_arg = argv[1]
    post_code_arg = argv[2]
    date_start_arg = argv[3]
    date_end_arg = argv[4]
    notify_available_slots(email_address_arg, post_code_arg, date_start_arg, date_end_arg)
