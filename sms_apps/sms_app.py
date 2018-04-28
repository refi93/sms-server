from datetime import datetime

import db
from models import MessageToSend

class SmsApp:
    def should_handle(self, sms):
        pass

    def get_response(self, sms):
    	pass

    def handle(self, sms):
        response = self.get_response(sms)
        
        db.session.add(MessageToSend(
        	phone_to=sms.phone_from,
        	msg_body=response
        ))
        sms.processed_at = datetime.utcnow()

        db.session.commit()