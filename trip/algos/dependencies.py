import typing

from trip import domain


def get_dependencies(deps: typing.Dict[str, typing.List[domain.VersionNode]]) -> typing.List[typing.List[domain.VersionNode]]:
    deps_info = []
    versions_by_name = {}
    for version_name, cur_deps in deps.items():
        for n in cur_deps:
            _get_versions_by_name(n, versions_by_name)

        deps_info.append({
            'version_name': version_name,
            'versions': _get_versions(cur_deps),
            'counter': 0
        })

    result = []
    while not _finished(deps_info):
        final_version = None
        for x in deps_info:
            final_version = _merge(final_version, x['versions'][x['counter']])
            if not final_version:
                break
        _incr(deps_info)
        if final_version:
            result.append(final_version)

    return result


def _merge(v1: typing.List[domain.VersionNode], v2: typing.List[domain.VersionNode]) -> typing.List[domain.VersionNode]:
    if not v1:
        return v2
    if not v2:
        return v1

    v1_by_name = {x.version_name: x for x in v1}
    v2_by_name = {x.version_name: x for x in v2}

    for k1 in v1_by_name.keys():
        if k1 in v2_by_name and v1_by_name[k1] != v2_by_name[k1]:
            return []

    return v1 + [x for x in v2 if x.version_name not in v1_by_name]


def _incr(deps_info: typing.List[typing.Dict], index: int=0) -> None:
    if index == 0 and _finished(deps_info):
        raise ValueError
    x = deps_info[index]
    if x['counter'] == len(x['versions']) - 1:
        x['counter'] = 0
        _incr(deps_info, index + 1)
    else:
        x['counter'] += 1


def _finished(deps_info: typing.List[typing.Dict]) -> bool:
    return all(x['counter'] == len(x['versions']) - 1 for x in deps_info)


def _get_versions_by_name(node: domain.VersionNode, result: typing.Dict[str, typing.Set[domain.VersionNode]]) \
        -> None:
    result.get(node.version_name, set()).add(node)
    for child in node.dependencies:
        _get_versions_by_name(child, result)


def _get_versions(nodes: typing.List[domain.VersionNode]) -> typing.List[typing.List[domain.VersionNode]]:
    result = []
    for node in nodes:
        cur_result = _get_versions_for_node(node, [], [])
        if cur_result:
            result += cur_result
    return result


def _get_versions_for_node(
        node: domain.VersionNode,
        result: typing.List[typing.List[domain.VersionNode]],
        call_stack: typing.List[domain.VersionNode]) -> typing.List[typing.List[domain.VersionNode]]:
    call_stack.append(node)
    if node.dependencies:
        for child in node.dependencies:
            _get_versions_for_node(child, result, call_stack)
    else:
        result.append(call_stack.copy())
    call_stack.pop()
    return result
