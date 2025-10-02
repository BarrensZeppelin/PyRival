Hi Codeforces!

Have you ever had this issue before?

![ ](https://cdn.discordapp.com/attachments/572613134020247562/1191774699110285392/image.png?ex=65a6a9ae&is=659434ae&hm=aeb62b0d97a84c226709b88bc3db7647f4509eef7c3a757a798ffe37e7e91c2b&)

If yes, then you have come to the right place! This is a blog about my super easy to use template for (reroot) DP on trees. I really believe that this template is kind of revolutionary for solving reroot DP problems. I've implemented it both in [Python](https://codeforces.com/contest/1324/submission/240129139) and in [C++](https://codeforces.com/contest/1324/submission/240131453) (the template supports `Python2`, `Python3` and `>= C++14`). Using this template, you will be able to easily solve > 2000 rated reroot problems in a couple of minutes, with a couple of lines of code.

A big thanks goes out to everyone that has helped me by giving feedback on blog and/or discussing reroot with me, [user:nor,2024-01-03], [user:meooow,2024-01-03], [user:qmk,2024-01-03], [user:demoralizer,2024-01-03], [user:jeroenodb,2024-01-03], [user:ffao,2024-01-03]. And especially a huge thanks goes to [user:nor,2024-01-03] for helping out making the C++ version of the template.

## 1. Introduction / Motivation

As an example, consider this problem: [problem:1324F]. The single thing that makes this problem difficult is that you need **for every node** $u$ find the maximum white subtree containing $u$. Had this problem only asked to find the answer for a specific node $u$, then a simple dfs solution would have worked.

<spoiler summary="Simple dfs solution">
```py
def dfs(node, parent=-1):
  nodeDP = 0
  for nei in graph[node]:
    if nei != parent:
      nodeDP = nodeDP + max(dfs(nei, node), 0)
  return nodeDP + 2 * color[node] - 1
print(dfs(u))
```
</spoiler>

But [problem:1324F] requires you to find the answer for every node. This forces you to use a technique called _rerooting_. Long story short, it is a mess to code. Maybe you could argue that for this specific problem it isn't all that bad. But it is definitely not as easy to code as the dfs solution above.

What if I told you that it is possible to take the logic from the dfs function above, put it inside of a "black box", and get the answer for all $u$ in $O(n \log n)$ time? Well it is, and that is what this blog is all about =)

In order to extract the logic from the simple dfs solution, let us first create a generic template for DP on trees and implement the simple dfs solution using its interface. _Note that the following code contain the exact same logic as the simple dfs solution above. It solves the problem for a specific node $u$._

<spoiler summary="Simple dfs solution (using treeDP template)">
```py
def treeDP(root, graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
  DP = [0] * len(graph)
  def dfs(node, parent=-1):
    nodeDP = default[node]
    for eind, nei in enumerate(graph[node]):
      if nei != parent:
        neiDP = dfs(nei, node)
        nodeDP = combine(nodeDP, neiDP, node, eind)
    parent_eind = -1 if parent == -1 else graph[node].index(parent)
    DP[node] = finalize(nodeDP, node, parent_eind)
    return DP[node]

  dfs(root)
  return DP

default = [0] * n

def combine(nodeDP, neiDP, node, eind):
  return nodeDP + max(neiDP, 0)

def finalize(nodeDP, node, eind):
  return nodeDP + 2 * color[node] - 1

print(treeDP(u, graph, default, combine, finalize)[u])
```
</spoiler>

Now, all that remains to solve the full problem is to switch out the `treeDP` function with the ultimate reroot template. The template returns the output of `treeDP` **for every node** $u$, in $O(n \log n)$ time! It is just that easy. [submission:240150867]

<spoiler summary="Solution to problem F using the ultimate reroot template">
```py
default = [0] * n

def combine(nodeDP, neiDP, node, eind):
  return nodeDP + max(neiDP, 0)

def finalize(nodeDP, node, eind):
  return nodeDP + 2 * color[node] - 1

rootDP, _, _ = rerooter(graph, default, combine, finalize)
print(*rootDP)
```
</spoiler>

The takeaway from this is example is that the reroot template makes it almost trivial to solve complicated reroot problems. For example, suppose we modify [problem:1324F] such that both nodes and edges have colors. Normally this modification would be complicated and would require an entire overhaul of the solution. However, with the ultimate reroot template, the solution is simply:

<spoiler summary="Solution to problem F if both edges and nodes are colored">
```py
default = [0] * n

def combine(nodeDP, neiDP, node, eind):
  return nodeDP + max(neiDP + 2 * edge_color[node][eind] - 1, 0)

def finalize(nodeDP, node, eind):
  return nodeDP + 2 * color[node] - 1

rootDP, _, _ = rerooter(graph, default, combine, finalize)
print(*rootDP)
```
</spoiler>

## 2. Collection of reroot problems and solutions

Here is a collection of reroot problems on Codeforces, together with some short and simple solutions in both Python and C++ using the `rerooter` template. These are nice problems to practice on if you want to try out using this template. The difficulty rating ranges between 1700 and 2600. I've also put together a GYM contest with all of the problems: [Collection of Reroot DP problems (difficulty rating 1700 to 2600)](https://codeforces.com/contestInvitation/eb6f12aa75be484e2f00f86a9e73f7ec5e0aa376).

(1700 rating) [problem:219D]
: [Python solution](https://codeforces.com/contest/219/submission/240150642), [C++ solution](https://codeforces.com/contest/219/submission/240130674)

(2300 rating) [problem:543D]
: [Python solution](https://codeforces.com/contest/543/submission/240150668), [C++ solution](https://codeforces.com/contest/543/submission/240130635)

(2200 rating) [problem:592D]
: [Python solution](https://codeforces.com/contest/592/submission/242160006), [C++ solution](https://codeforces.com/contest/592/submission/242163483)

(2600 rating) [problem:627D]
: [Python solution](https://codeforces.com/contest/627/submission/240150708), [C++ solution](https://codeforces.com/contest/627/submission/240130592)

(2100 rating) [problem:852E]
: [Python solution](https://codeforces.com/contest/852/submission/240150734), [C++ solution](https://codeforces.com/contest/852/submission/240130838)

(2300 rating) [problem:960E]
: [Python solution](https://codeforces.com/contest/960/submission/240150756), [C++ solution](https://codeforces.com/contest/960/submission/240130918)
: Or alternatively using "edge DP":
: [Python solution](https://codeforces.com/contest/960/submission/240150781), [C++ solution](https://codeforces.com/contest/960/submission/240131037)

(1900 rating) [problem:1092F]
: [Python solution](https://codeforces.com/contest/1092/submission/240150804), [C++ solution](https://codeforces.com/contest/1092/submission/240131105)

(2200 rating) [problem:1156D]
: [Python solution](https://codeforces.com/contest/1156/submission/242160187), [C++ solution](https://codeforces.com/contest/1156/submission/242164560)

(2400 rating) [problem:1182D]
: [Python solution](https://codeforces.com/contest/1182/submission/240150829), [C++ solution](https://codeforces.com/contest/1182/submission/240131161)

(2100 rating) [problem:1187E]
: [Python solution](https://codeforces.com/contest/1187/submission/240150852), [C++ solution](https://codeforces.com/contest/1187/submission/240131416)

(2000 rating) [problem:1294F]
: [Python solution](https://codeforces.com/contest/1294/submission/240163333), [C++ solution](https://codeforces.com/contest/1294/submission/240163557)

(1800 rating) [problem:1324F]
: [Python solution](https://codeforces.com/contest/1324/submission/240150867), [C++ solution](https://codeforces.com/contest/1324/submission/240131453)

(2500 rating) [problem:1498F]
: [Python solution](https://codeforces.com/contest/1498/submission/240150889), [C++ solution](https://codeforces.com/contest/1498/submission/240131551)

(2400 rating) [problem:1626E]
: [Python solution](https://codeforces.com/contest/1626/submission/240150910), [C++ solution](https://codeforces.com/contest/1626/submission/240131643)

(2500 rating) [problem:1691F]
: [Python solution](https://codeforces.com/contest/1691/submission/240150929), [C++ solution](https://codeforces.com/contest/1691/submission/240131727)

(2400 rating) [problem:1794E]
: [Python solution](https://codeforces.com/contest/1794/submission/242160592), [C++ solution](https://codeforces.com/contest/1794/submission/242166648)

(2500 rating) [problem:1796E]
: [Python solution](https://codeforces.com/contest/1796/submission/242160866), [C++ solution](https://codeforces.com/contest/1796/submission/242167901)

(1700 rating) [problem:1881F]
: [Python solution](https://codeforces.com/contest/1881/submission/240150943), [C++ solution](https://codeforces.com/contest/1881/submission/240131762)

[problem:104008G]
: [Python solution](https://codeforces.com/gym/104008/submission/242169608), [C++ solution](https://codeforces.com/gym/104008/submission/242169690)

[problem:104665H]
: [Python solution](https://codeforces.com/gym/104665/submission/242169914), [C++ solution](https://codeforces.com/gym/104665/submission/242170843)

## 3. Understanding the `rerooter` black box

The following is the black box `rerooter` implemented naively:

<spoiler summary="Template (naive O(n^2) version)">
```py
def treeDP(root, graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
  DP = [0] * len(graph)
  def dfs(node, parent=-1):
    nodeDP = default[node]
    for eind, nei in enumerate(graph[node]):
      if nei != parent:
        neiDP = dfs(nei, node)
        nodeDP = combine(nodeDP, neiDP, node, eind)
    parent_eind = -1 if parent == -1 else graph[node].index(parent)
    DP[node] = finalize(nodeDP, node, parent_eind)
    return DP[node]

  dfs(root)
  return DP

def rerooter(graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
  n = len(graph)
  rootDP = []
  edgeDP = {}
  for root in range(n):
    DP = treeDP(root, graph, default, combine, finalize)
    rootDP.append(DP[root])
    for nei in graph[root]:
      edgeDP[root, nei] = DP[nei]

  forwardDP = [[edgeDP[node, nei] for nei in graph[node]] for node in range(n)]
  reverseDP = [[edgeDP[nei, node] for nei in graph[node]] for node in range(n)]

  return rootDP, forwardDP, reverseDP
```
</spoiler>

`rerooter` outputs three variables.

1. `rootDP` is a list, where `rootDP[node] = dfs(node)`.
2. `forwardDP` is a list of lists, where `forwardDP[node][eind] = dfs(nei, node)`, where `nei = graph[node][eind]`.
3. `reverseDP` is a list of lists, where `reverseDP[node][eind] = dfs(node, nei)`, where `nei = graph[node][eind]`.

If you don't understand the definitions of `rootDP`/`forwardDP`/`reverseDP`, then I recommend reading the naive $O(n^2)$ implementation of `rerooter`. It should be fairly self explanatory.

The rest of this blog is about the techniques of how to make `rerooter` run in $O(n \log n)$. So if you just want to use `rerooter` as a black box, then you don't have to read or understand the rest of this blog.

One last remark. If you've ever done rerooting before, you might recall that rerooting usually runs in $O(n)$ time. So why does this template run in $O(n \log n)$? The reason for this is that I restrict myself to use the `combine` function in a left folding procedure, e.g. `combine(combine(combine(nodeDP, neiDP1), neiDP2), neiDP3)`. My template is not allowed to do for example `combine(nodeDP, combine(neiDP1, combine(neiDP2, neiDP3)))`. While this limitation makes the template run slower, $O(n \log n)$ instead of $O(n)$, it also makes it a lot easier to use the template. If you still think that the $O(n)$ version is superior, then I don't think you've understood how nice and general the $O(n \log n)$ version truly is.

## 4. Rerooting and exclusivity

The general idea behind rerooting is that we first compute the DP as normal for some arbitrary node as the root (I use `node = 0` for this). After we have done this we can "move" the root of the tree by updating the DP value of the old root and the DP value of a neighbour to the old root. That neighbour then becomes the new root.

Let $u$ denote the current root, and let $v$ denote the neighbour of $u$ that we want to move the root to. At this point, we already know the value of `dfs(v, u)` since $u$ is the current root. But in order to be able to move the root from $u$ to $v$, we need to find the new DP value of $u$, i.e. `dfs(u, v)`.

If we think about this in terms of `forwardDP` and `reverseDP`, then we currently know `forwardDP[u]`, and our goal is to compute `reverseDP[u]`. This can be done naively in $O(\text{deg}(u)^2)$ time with a couple of for loops by calling `combine` $O(\text{deg}(u)^2)$ times, and then calling `finalize` $O(\text{deg}(u))$ times.

The bottle neck here are the $O(\text{deg}(u)^2)$ calls to `combine`. So for now, let us separate out the part of the code that calls `combine` from the rest of the code into a function called `exclusive`. The goal of the next section will then be to speed up the naively implemented `exclusive` function to run in $O(\text{deg}(u) \text{log} (\text{deg}(u)))$ time.

<spoiler summary="Rerooting using exclusivity (O(sum deg^2) version)">
```py
def exclusive(A, zero, combine, node):
    n = len(A)

    exclusiveA = [zero] * n
    for i in range(n):
        for j in range(n):
            if i != j:
                exclusiveA[i] = combine(exclusiveA[i], A[j], node, j)
    return exclusiveA

def treeDP(root, graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
  DP = [0] * len(graph)
  def dfs(node, parent=-1):
    nodeDP = default[node]
    for eind, nei in enumerate(graph[node]):
      if nei != parent:
        neiDP = dfs(nei, node)
        nodeDP = combine(nodeDP, neiDP, node, eind)
    parent_eind = -1 if parent == -1 else graph[node].index(parent)
    DP[node] = finalize(nodeDP, node, parent_eind)
    return DP[node]

  dfs(root)
  return DP

def rerooter(graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
    n = len(graph)
    rootDP = [0] * n
    forwardDP = [None] * n
    reverseDP = [None] * n

    # Compute DP for root=0
    DP = treeDP(0, graph, default, combine, finalize)

    # Do rerooting using the exclusive function
    def dfs(node, parent=-1, parent_eind=-1):
        forwardDP[node] = [DP[nei] for nei in graph[node]]
        rerootDP = exclusive(forwardDP[node], default[node], combine, node)
        reverseDP[node] = [finalize(nodeDP, node, eind) for eind, nodeDP in enumerate(rerootDP)]
        nodeDP = combine(rerootDP[0], forwardDP[node][0], node, 0) if n > 1 else default[node]
        rootDP[node] = finalize(nodeDP, node, -1)
        for eind, nei in enumerate(graph[node]):
            if nei != parent:
                DP[node] = reverseDP[node][eind]
                dfs(nei, node, eind)
    dfs(0)
    return rootDP, forwardDP, reverseDP
```
</spoiler>

## 5. The exclusive segment tree

We are almost done implementing the fast reroot template. The only operation left to speed up is the function `exclusive`. Currently it runs in $O(\sum \text{deg}^2)$ time. The trick to make `exclusive` run in $O(\sum \text{deg} \log{(\text{deg})})$ time is to create something similar to a segment tree.

Suppose you have a segment tree where each node in the segment tree accumulates all of the values outside of its interval. The leaves of such a segment tree can then be used as the output of `exclusive`. I call this data structure the _exclusive segment tree_.

<spoiler summary="Example: Exclusive segment tree of size n = 8">
Each node in the exclusive segment tree should accumulate everything outside of its interval. For example, in the following figure, the node marked with a red cross should accumulate the 4 values in the bottom right.
![ ](https://cdn.discordapp.com/attachments/572613134020247562/893515502486450207/unknown.png)

Likewise, the node marked here with a red cross should accumulate 6 values.
![ ](https://cdn.discordapp.com/attachments/572613134020247562/893512939187871755/unknown.png)
</spoiler>

The exclusive segment tree is naturally built from top to bottom, taking $O(n \log n)$ time. Here is an implementation of `rerooter` using the exclusive segment tree:

<spoiler summary="Rerooting using exclusivity (O(sum deg log(deg)) version)">
```py
def exclusive(A, zero, combine, node):
    n = len(A)
    exclusiveA = [zero] * n # Exclusive segment tree

    # Build exclusive segment tree
    for bit in range(n.bit_length())[::-1]:
        for i in range(n)[::-1]:
            # Propagate values down the segment tree
            exclusiveA[i] = exclusiveA[i // 2]
        for i in range(n & ~(bit == 0)):
            # Fold A[i] into exclusive segment tree
            ind = (i >> bit) ^ 1
            exclusiveA[ind] = combine(exclusiveA[ind], A[i], node, i)
    return exclusiveA

def treeDP(root, graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
  DP = [0] * len(graph)
  def dfs(node, parent=-1):
    nodeDP = default[node]
    for eind, nei in enumerate(graph[node]):
      if nei != parent:
        neiDP = dfs(nei, node)
        nodeDP = combine(nodeDP, neiDP, node, eind)
    parent_eind = -1 if parent == -1 else graph[node].index(parent)
    DP[node] = finalize(nodeDP, node, parent_eind)
    return DP[node]

  dfs(root)
  return DP

def rerooter(graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
    n = len(graph)
    rootDP = [0] * n
    forwardDP = [None] * n
    reverseDP = [None] * n

    # Compute DP for root=0
    DP = treeDP(0, graph, default, combine, finalize)

    # Do rerooting using the exclusive function
    def dfs(node, parent=-1, parent_eind=-1):
        forwardDP[node] = [DP[nei] for nei in graph[node]]
        rerootDP = exclusive(forwardDP[node], default[node], combine, node)
        reverseDP[node] = [finalize(nodeDP, node, eind) for eind, nodeDP in enumerate(rerootDP)]
        nodeDP = combine(rerootDP[0], forwardDP[node][0], node, 0) if n > 1 else default[node]
        rootDP[node] = finalize(nodeDP, node, -1)
        for eind, nei in enumerate(graph[node]):
            if nei != parent:
                DP[node] = reverseDP[node][eind]
                dfs(nei, node, eind)
    dfs(0)
    return rootDP, forwardDP, reverseDP

```
</spoiler>

This algorithm runs in $O(\sum \text{deg} \log{(\text{deg})})$, so we are essentially done. However, this implementation uses recursive DFS which especially for Python is a huge drawback. Recursion in Python is both relatively slow and increadibly memory hungry. So for a far more practical version, I've also implemented this same algorithm using a BFS instead of a DFS. This gives us the final version of the ultimate `rerooter` template!

<spoiler summary="Rerooting using exclusivity (O(sum deg log(deg)) version with BFS)">
```py
def exclusive(A, zero, combine, node):
    n = len(A)
    exclusiveA = [zero] * n # Exclusive segment tree

    # Build exclusive segment tree
    for bit in range(n.bit_length())[::-1]:
        for i in range(n)[::-1]:
            # Propagate values down the segment tree
            exclusiveA[i] = exclusiveA[i // 2]
        for i in range(n & ~(bit == 0)):
            # Fold A[i] into exclusive segment tree
            ind = (i >> bit) ^ 1
            exclusiveA[ind] = combine(exclusiveA[ind], A[i], node, i)
    return exclusiveA

def rerooter(graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
    n = len(graph)
    rootDP = [0] * n
    forwardDP = [None] * n
    reverseDP = [None] * n

    # Compute DP for root=0
    DP = [0] * n
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
    # DP for root=0 done

    # Use the exclusive function to reroot
    for node in bfs:
        DP[P[node]] = DP[node]
        forwardDP[node] = [DP[nei] for nei in graph[node]]
        rerootDP = exclusive(forwardDP[node], default[node], combine, node)
        reverseDP[node] = [finalize(nodeDP, node, eind) for eind, nodeDP in enumerate(rerootDP)]
        rootDP[node] = finalize((combine(rerootDP[0], forwardDP[node][0], node, 0) if n > 1 else default[node]), node, -1)
        for nei, dp in zip(graph[node], reverseDP[node]):
            DP[nei] = dp
    return rootDP, forwardDP, reverseDP


```
</spoiler>
