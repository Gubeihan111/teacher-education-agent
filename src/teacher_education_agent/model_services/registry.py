"""Model service composition."""
from teacher_education_agent.core.config import get_settings
from .gateway import ModelGateway
def build_model_gateway() -> ModelGateway:
    return ModelGateway(get_settings())
