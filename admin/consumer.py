"""
This module defines a RabbitMQ consumer for the Django admin service.

It listens to the 'admin' queue for messages related to product likes 
and updates the corresponding product's 'likes' count in the database.
"""

import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    """
    Callback function to handle messages received from the 'main' queue.

    Args:
        ch: The channel object.
        method: The method object.
        properties: The properties object.
        body: The message body (bytes).
    """
    print('Received in admin')
    product_id = json.loads(body)
    print(product_id)
    product = Product.objects.get(id=product_id)
    product.likes += 1
    product.save()
    print('Product likes increased!')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()