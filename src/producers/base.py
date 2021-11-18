from src.config import DefaultConfig
from src.exceptions.handler import handle_exception
from src.extensions import producer
from src.utils.format import dumps


@handle_exception()
def send_message_to_topic(topic: str, data: dict):
    """

        Format message:

        topic: string
        data:
            {
                "action": PUT, POST, DELETE
                "value": object
            }
            - PUT = Update something
            - POST = Request or submit something
            - DELETE = Remove or delete something
    """

    if isinstance(data, dict):
        if not isinstance(data.get('from_services'), list):
            data['from_services'] = []
        data['from_services'].append(DefaultConfig.PROJECT)
    value = dumps(data)
    future = producer.send(topic, value.encode('utf-8'))
    result = future.get(timeout=60)
    print('result producer', result)
