"""
This module defines a RabbitMQ consumer for the Flask backend service. 

It listens to the 'main' queue for messages related to product actions 
(create, update, delete) and performs corresponding database operations 
to keep the Flask backend's product data in sync with the Django admin service.
"""

import pika
import json

from main import Product, db

params = pika.URLParameters('amqp://guest:guest@python-app-rabbitmq-1:5672/')
connection = pika.BlockingConnection(params) 
channel = connection.channel()  

channel.queue_declare(queue='main')  


def callback(ch, method, properties, body):
    """
    Callback function to handle messages received from the 'main' queue.

    Args:
        ch: The channel object.
        method: The method object.
        properties: The properties object containing message metadata.
        body: The message body (bytes).
    """
    print('Received in main')
    data = json.loads(body)  
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data) 
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming() 
channel.close() 