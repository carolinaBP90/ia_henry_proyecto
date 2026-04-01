from collections import defaultdict


class QueueBroker:
    def __init__(self) -> None:
        self._queues: dict[str, list[dict]] = defaultdict(list)

    def publish(self, queue_name: str, message: dict) -> None:
        self._queues[queue_name].append(message)

    def consume_all(self, queue_name: str) -> list[dict]:
        items = list(self._queues[queue_name])
        self._queues[queue_name].clear()
        return items


broker = QueueBroker()
