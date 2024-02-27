import os

import boto3
from formula_thoughts_web.abstractions import EventHandler, Serializer
from formula_thoughts_web.events import SQSEventPublisher
from formula_thoughts_web.ioc import Container

from backend.src.events.handlers import UpsertGroupEventHandler


sqs = boto3.client('sqs')


def register_event_dependencies(container: Container):
    serializer = container.resolve(service=Serializer)
    (container.register(service=EventHandler, implementation=UpsertGroupEventHandler)
     # TODO: figure out how to get implementations from service container
     .register_factory(service=SQSEventPublisher, factory=lambda: SQSEventPublisher(sqs_client=sqs,
                                                                                    queue_name=os.environ['QUEUE_NAME'],
                                                                                    serializer=serializer)))
