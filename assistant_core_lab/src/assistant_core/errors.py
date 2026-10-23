class AssistantError(Exception):
    """Base class for all assistant errors."""
    pass

class ConfigError(AssistantError):
    """Configuration is missing or invalid."""
    pass

class DataError(AssistantError):
    """A knowledge file is missing or malformed."""
    pass

class InvalidRequest(AssistantError):
    """The user's request cannot be processed as given."""
    pass

class ProviderError(AssistantError):
    """The AI provider failed (timeout, outage, bad response)."""
    pass
