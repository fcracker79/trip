import typing

from trip import domain


def get_closure(node: domain.VersionNode) -> typing.Set[domain.VersionNode]:
    result = set()
    _get_closure(node, result)
    return result


def _get_closure(node: domain.VersionNode, result: typing.Set[domain.VersionNode]) -> None:
    result.add(node)
    for child in node.dependencies:
        _get_closure(child, result)
