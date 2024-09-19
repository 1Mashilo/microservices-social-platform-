# RabbitMQ Consumer Configuration for Flask Backend

# Import necessary libraries
import pika
import json
from flask import Flask
from main import db, Product
from main import app 

# Configure RabbitMQ connection
params = pika.URLParameters('amqp://guest:guest@localhost:5672/')
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare the RabbitMQ queue
channel.queue_declare(queue='main')

# Define the callback function for handling received messages
def callback(ch, method, properties, body):
    print('Received in main (Flask backend):', body.decode())

    # Parse the received message data
    data = json.loads(body)

    # Handle the message based on its content type
    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        if product:
            product.title = data['title']
            product.image = data['image']
            db.session.commit()

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data['id'])
        if product:
            db.session.delete(product)
            db.session.commit()

# Set up the consumer to listen for messages on the "main" queue
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages from "admin" (Django backend). To exit, press CTRL+C')
channel.start_consuming()
