from __future__ import annotations
from typing import Any, Callable, List, Optional

import flowfunc.config as base
from flowfunc.models import Port
from .models import Node


def node_config(**kwargs: Any):
    """Decorator to attach custom configuration to node functions."""

    def decorator(func: Callable) -> Callable:
        setattr(func, "_node_custom_config", kwargs)
        return func

    return decorator


class Config(base.Config):
    """Extended Config supporting custom node attributes."""

    @classmethod
    def from_function_list(
        cls,
        function_list: List[Callable],
        extra_nodes: Optional[List[Node]] = None,
        extra_ports: Optional[List[Port]] = None,
    ) -> "Config":
        nodes: List[Node] = []
        for func in function_list:
            base_node = base.process_node(func)
            node_data = base_node.model_dump()
            node_data.update(getattr(func, "_node_custom_config", {}))
            node = Node(**node_data, method=base_node.method)
            nodes.append(node)

        extra_nodes = extra_nodes or []
        extra_ports = extra_ports or []
        ports = list(set(extra_ports + base.ports_from_nodes(nodes)))
        nodes = nodes + extra_nodes
        return cls(nodes, ports)
