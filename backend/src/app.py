import os

from formula_thoughts_web.ioc import register_web, Container, LambdaRunner

from src.data.ioc import register_data_dependencies
from src.domain.ioc import register_domain_dependencies
from src.web.ioc import register_web_dependencies


def lambda_handler(event, context):
    container = Container()
    bootstrap(container=container)
    run(event=event, context=context, container=container)


def bootstrap(container):
    register_web(services=container, default_error_handling_strategy="leave to be determined")
    register_domain_dependencies(container=container)
    register_web_dependencies(container=container)
    register_data_dependencies(container=container)


def run(event, context, container):
    return container.resolve(service=LambdaRunner).run(event=event, context=context)