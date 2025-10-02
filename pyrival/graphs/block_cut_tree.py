from __future__ import annotations

from .node_bcc import find_bcc


class BlockCutTree:
    __slots__ = ("B", "rep", "tree")

    def __init__(self, graph: list[list[int]]):
        N = len(graph)
        cnt = [0] * N
        # Maps each node to its representative in the block-cut tree.
        self.rep = rep = [-1] * N
        bcc = find_bcc(graph)
        self.B = B = len(bcc)
        tree: list[list[int]] = [[] for _ in range(B)]
        for i, comp in enumerate(bcc):
            for v in comp:
                cnt[v] += 1
                if cnt[v] == 1:
                    rep[v] = i
                elif cnt[v] >= 2:
                    if cnt[v] == 2:
                        tree.append([prep := rep[v]])
                        tree[prep].append(B)
                        rep[v] = B
                        B += 1

                    tree[i].append(rv := rep[v])
                    tree[rv].append(i)

        self.tree = tree

    def is_block(self, i: int) -> bool:
        "Returns True if node i in the block-cut tree represents a block (not a cut vertex)."
        return i < self.B
