class Component:
    """Minimal base component used for custom nodes."""

    def __init__(self, component_id: str | None = None):
        self.id = component_id
