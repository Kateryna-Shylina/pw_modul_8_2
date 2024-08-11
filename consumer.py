import sys
import pika
import connect
from models import Contacts

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    def send_email(contact):
        print(f"Sending email to {contact.email}...")
        
        contact.status = True
        contact.save()
        print(f"Email sent to {contact.email}. Status updated to {contact.status}.")

    def callback(ch, method, properties, body):
        contact_id = body.decode('utf-8')
        contact = Contacts.objects(id=contact_id).first()
        if contact:
            send_email(contact)

    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)