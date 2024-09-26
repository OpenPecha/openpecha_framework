from pecha_framework.pipeline import Document, Pipeline, component_registry


def pipe_component(name=None, requires=None):
    """Decorator to register a function as a pipeline component."""

    def decorator(func):
        # Set default name if not provided
        component_name = name or func._name_.lower()

        # Store any required dependencies
        func.requires = requires or []

        # Register the function in the component registry
        component_registry[component_name] = func

        return func

    return decorator
