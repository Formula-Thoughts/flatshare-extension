import os

from src.data.ioc import register_data_dependencies
from src.domain.ioc import register_domain_dependencies
from src.events.ioc import register_event_dependencies
from src.web.ioc import register_web_dependencies
from formula_thoughts_web.ioc import register_web, Container, LambdaRunner


def lambda_handler(event, context):
    print(os.environ["QUEUE_NAME"])
    container = Container()
    register_web(services=container, default_error_handling_strategy="leave to be determined")
    register_domain_dependencies(container=container)
    register_web_dependencies(container=container)
    register_event_dependencies(container=container)
    register_data_dependencies(container=container)
    return container.resolve(service=LambdaRunner).run(event=event, context=context)
