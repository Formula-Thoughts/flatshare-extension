from formula_thoughts_web.ioc import register_web, Container, LambdaRunner

from backend.src.data.ioc import register_data_dependencies
from backend.src.domain.ioc import register_domain_dependencies
from backend.src.events.ioc import register_event_dependencies
from backend.src.web.ioc import register_web_dependencies


def lambda_handler(event: dict, context: dict) -> dict:
    container = Container()
    register_web(services=container, default_error_handling_strategy="leave to be determined")
    register_domain_dependencies(container=container)
    register_web_dependencies(container=container)
    register_event_dependencies(container=container)
    register_data_dependencies(container=container)
    return container.resolve(service=LambdaRunner).run(event=event, context=context)