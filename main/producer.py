"""
This module provides a function to publish messages to a RabbitMQ queue.

It establishes a connection to a RabbitMQ server and defines a 'publish' 
function to send messages with specified metadata (method) and content (body) 
to the 'admin' queue.
"""

import pika
import json
import producer

params = pika.URLParameters('amqp://guest:guest@python-app-rabbitmq-1:5672/')

connection = pika.BlockingConnection(params)  
channel = connection.channel() 

def publish(method, body):
    """
    Publishes a message to the 'admin' queue.

    Args:
        method (str): The type of message or action being performed (e.g., 'product_created', 'product_updated').
        body (dict): The data associated with the message, typically a dictionary that will be JSON-encoded.
    """
    properties = pika.BasicProperties(method) 
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)