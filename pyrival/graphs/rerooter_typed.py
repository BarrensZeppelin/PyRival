from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Generic, Protocol, TypeVar

    Agg = TypeVar("Agg")
    Val = TypeVar("Val", contravariant=True)

    class CombineFn(Protocol, Generic[Agg, Val]):
        def __call__(self, a: Agg, b: Val, node: int, eind: int) -> Agg: ...


def rerooter(
    graph: list[list[int]],
    default: list[Agg],
    combine: CombineFn,
    finalize: Callable[[Agg, int, int], Val] = lambda nodeDP, node, eind: nodeDP,
) -> tuple[list[Val], list[list[Val]], list[list[Val]]]:
    n = len(graph)
    rootDP: list[Val] = [0] * n  # pyright: ignore[reportAssignmentType]
    forwardDP: list[list[Val]] = [[]] * n
    reverseDP = forwardDP[:]

    def exclusive(A: list[Val], zero: Agg, node: int):
        n = len(A)
        exclusiveA = [zero] * n

        for bit in range(n.bit_length())[::-1]:
            for i in range(n)[::-1]:
                exclusiveA[i] = exclusiveA[i // 2]
            for i in range(n & (-1 if bit else -2)):
                ind = (i >> bit) ^ 1
                exclusiveA[ind] = combine(exclusiveA[ind], A[i], node, i)
        return exclusiveA

    DP = rootDP[:]
    bfs = [0]
    P = [0] * n
    for node in bfs:
        for nei in graph[node]:
            if P[node] != nei:
                P[nei] = node
                bfs.append(nei)

    for node in reversed(bfs):
        nodeDP = default[node]
        for eind, nei in enumerate(graph[node]):
            if P[node] != nei:
                nodeDP = combine(nodeDP, DP[nei], node, eind)
        DP[node] = finalize(nodeDP, node, graph[node].index(P[node]) if node else -1)

    for node in bfs:
        DP[P[node]] = DP[node]
        forwardDP[node] = [DP[nei] for nei in graph[node]]
        rerootDP = exclusive(forwardDP[node], default[node], node)
        reverseDP[node] = [
            finalize(nodeDP, node, eind) for eind, nodeDP in enumerate(rerootDP)
        ]
        rootDP[node] = finalize(
            (
                combine(rerootDP[0], forwardDP[node][0], node, 0)
                if n > 1
                else default[node]
            ),
            node,
            -1,
        )
        for nei, dp in zip(graph[node], reverseDP[node], strict=True):
            DP[nei] = dp
    return rootDP, forwardDP, reverseDP
