from typing import Type, Dict
from .base import WeatherProvider
from .mock import MockProvider

# Registry of available weather providers
_registry: Dict[str, Type[WeatherProvider]] = {
    "mock": MockProvider
}


def register_provider(name: str, provider: Type[WeatherProvider]) -> None:
    if not issubclass(provider, WeatherProvider):
        raise TypeError(f"{provider} must inherit from WeatherProvider")
    # Add the provider to the registry
    _registry[name] = provider


def get_provider(name: str) -> Type[WeatherProvider]:
    # Retrieve a provider by name, with helpful error if not found
    if name not in _registry:
        available = ", ".join(_registry.keys())
        raise ValueError(f"Unknown provider '{name}'. Available: {available}")
    return _registry[name]