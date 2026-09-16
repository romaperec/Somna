from taskiq_nats import PullBasedJetStreamBroker

from app.core.config import settings

broker = PullBasedJetStreamBroker(f"nats://{settings.nats.host}:{settings.nats.port}", queue=f"{settings.app.name}_tasks")
