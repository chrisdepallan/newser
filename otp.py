import requests
import random

# Replace with your Fast2SMS API credentials
API_KEY = 'your_api_key'
SENDER_ID = 'FSTSMS'
OTP_TEMPLATE_ID = 'your_template_id'

def send_otp(phone_number):
    otp = random.randint(100000, 999999)
    url = f"https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "authorization": API_KEY,
        "sender_id": SENDER_ID,
        "message": f"Your OTP is {otp}. It is valid for 5 minutes.",
        "variables_values": otp,
        "route": "otp",
        "numbers": phone_number
    }

    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(f"Sent OTP {otp} to {phone_number}")
    return otp

if __name__ == "__main__":
    phone_number = input("Enter the phone number (without country code): ")
    send_otp(phone_number)
