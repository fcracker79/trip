import typing

from trip import domain


def find_circuits(*nodes: typing.Set[domain.VersionNode]):
    result = []
    for node in nodes:
        _already_seen = {}
        _nodes_stack = []
        _find_circuits(node, _already_seen, _nodes_stack, result)
    return result


def _find_circuits(
        node: domain.VersionNode,
        already_seen: dict,
        nodes_stack: typing.List[domain.VersionNode],
        result: typing.List[typing.List[domain.VersionNode]]) \
        -> None:
    nodes_stack.append(node)
    if already_seen.get(node, False):
        result.append(nodes_stack.copy())
        nodes_stack.pop()
        return

    already_seen[node] = True
    for child in node.dependencies:
        _find_circuits(child, already_seen, nodes_stack, result)
    nodes_stack.pop()
    already_seen[node] = False
