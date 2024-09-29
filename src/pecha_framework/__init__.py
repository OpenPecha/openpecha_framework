from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field, validator

from pecha_framework.pecha import Pecha

# Global component registry
component_registry = {}


class Pipe:
    requires: List[str] = []

    def __init_subclass__(cls, **kwargs):
        """Automatically register subclasses in the component registry."""
        super().__init_subclass__(**kwargs)
        name = getattr(cls, "name", cls.__name__.lower())
        component_registry[name] = cls
        if not hasattr(cls, "requires"):
            cls.requires = []


class Document(BaseModel):
    text: str = Field(default="")
    annotations: Dict[str, list] = Field(default_factory=dict)
    base_ann_mapping: List = Field(default_factory=list)

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @classmethod
    def from_pecha(cls, pecha: Pecha):
        return cls(pecha=pecha)

    def __repr__(self):
        return f"Document(text={self.text[:50]!r}..., annotations={list(self.annotations.keys())})"

    def get_attr(self, attr: str):
        """Get the attribute of the document."""
        attr_val = eval(f"self.{attr}")
        assert isinstance(attr_val, str), f"Attribute '{attr}' is not a string."

        return attr_val


class Pipeline:
    def __init__(self, components=None, **component_kwargs):
        self.components = []
        if components:
            # check if the components requirements are met.
            self.check_dependencies(components)
            # Add the components to the pipeline
            for name in components:
                self.add_pipe(name, **component_kwargs.get(name, {}))

    def check_dependencies(self, components):
        """
        Check if the component depending on other components are present before in the
        pipeline.
        """
        for idx, component in enumerate(components):
            component_cls = component_registry[component]
            for required_component in component_cls.requires:
                if required_component not in components[:idx]:
                    raise ValueError(
                        f"Component '{component}' requires '{required_component}'"
                    )

    def add_pipe(self, name, **kwargs):
        """Add a component to the pipeline by name."""
        if name not in component_registry:
            raise ValueError(f"Component '{name}' not found in the registry.")

        component_cls = component_registry[name]

        # Check if the component is a function (callable) or a class
        if callable(component_cls) and not isinstance(component_cls, type):
            # If it's a function, we don't need to instantiate it
            component = component_cls
        else:
            # If it's a class, instantiate it with the provided arguments
            component = component_cls(**kwargs)

        self.components.append((name, component))

    def __call__(self, doc):
        """Process the document through the pipeline."""
        for name, component in self.components:
            doc = component(doc)
        return doc

    def pipe_names(self):
        """List the names of the components in the pipeline."""
        return [name for name, _ in self.components]


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
