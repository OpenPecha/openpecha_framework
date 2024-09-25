from typing import List

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


class Document:
    def __init__(self, text=""):
        self.text = text
        self.annotations = {}

    def __repr__(self):
        return f"Document(text={self.text[:50]!r}..., annotations={list(self.annotations.keys())})"


class Pipeline:
    def __init__(self, components=None, **component_kwargs):
        self.components = []
        if components:
            for name in components:
                self.add_pipe(name, **component_kwargs.get(name, {}))

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
