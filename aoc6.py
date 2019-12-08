from collections import defaultdict, deque

with open("aoc6.in", "r") as f:
    edges = defaultdict(list)
    weight = {}
    for line in f:
        a, b = line.strip().split(")")
        edges[a].append(b)
        edges[b].append(a)

    queue = deque()

    weight['YOU'] = 0
    queue.append('YOU')

    while queue:
        cur = queue.popleft()
        for nxt in edges[cur]:
            if nxt not in weight:
                weight[nxt] = weight[cur] + 1
                queue.append(nxt)

    print(weight['SAN'] - 2)
