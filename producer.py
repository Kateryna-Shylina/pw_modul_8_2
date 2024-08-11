import pika
import connect
from models import Contacts
from faker import Faker


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    
    channel.queue_declare(queue='email_queue')
    
    fake = Faker()
    for _ in range(10):  
        contact = Contacts(
            fullname=fake.name(),
            email=fake.email(),
            status=False
        )
        contact.save()

        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))
        print(f"Sent contact ID {contact.id}")

    connection.close()
    

if __name__ == '__main__':
    main()