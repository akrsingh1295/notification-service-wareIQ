from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from twilio.rest import Client
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

class NotificationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True, help='Notification type (sms)')
        parser.add_argument('message', type=str, required=True, help='Notification message')
        args = parser.parse_args()

        notification_type = args['type']
        message = args['message']

        if notification_type == 'sms':
            # Use Twilio to send SMS
            send_sms(message)
            return 'SMS Notification sent successfully', 200
        else:
            return 'Invalid notification type', 400

def send_sms(message):
    
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
    
    # Replace these values with your Twilio phone numbers
    from_phone_number = '+18152670083'
    to_phone_number = '+918005307382'
    
    twilio_client.messages.create(body=message, from_=from_phone_number, to=to_phone_number)

api.add_resource(NotificationResource, '/send_notification')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    notification_type = data['type']
    message = data['message']
    
    # Make an HTTP request to the notifications microservice
    response = requests.post('http://localhost:5000/send_notification', json={'type': notification_type, 'message': message})
    
    if response.status_code == 200:
        return 'Notification sent successfully', 200
    else:
        return 'Failed to send notification', 500

if __name__ == '__main__':
    app.run(debug=True)
