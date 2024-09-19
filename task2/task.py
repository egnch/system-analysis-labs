import csv
import json


def read_graph_from_csv(csv_data: str, with_titles: bool = False) -> dict:
    lines = csv_data.strip().split("\n")

    reader = csv.reader(lines[1:] if with_titles else lines, delimiter=",")
    graph = {}
    for row in reader:
        if row[0] not in graph:
            graph[row[0]] = []
        if row[1] not in graph:
            graph[row[1]] = []
        graph[row[0]].append(row[1])

    return graph


def count_all_children(graph: dict) -> dict:
    result = {}

    def dfs(node: str) -> int:
        if node in result:
            return result[node]

        total = 0
        for child in graph[node]:
            total += 1 + dfs(child)
        result[node] = total
        return total

    for node in graph:
        dfs(node)

    return result


def main(data: str) -> str:
    graph = read_graph_from_csv(data)

    nodes = set(graph.keys()).union(*graph.values())
    nodes = {node: i for i, node in enumerate(sorted(nodes))}

    parents_dict = {node: [] for node in nodes}
    for node in graph:
        for child in graph[node]:
            parents_dict[child].append(node)
            current_node = node
            while parents_dict[current_node]:
                current_node = parents_dict[current_node][0]
                parents_dict[child].append(current_node)

    children_count = count_all_children(graph)
    extensional_lengths = [[0] * 5 for _ in range(len(nodes))]

    for node in graph:
        node_id = nodes[node]
        extensional_lengths[node_id][0] = len(graph[node])
        extensional_lengths[node_id][1] = 1 if parents_dict[node] else 0
        extensional_lengths[node_id][2] = children_count[node] - len(graph[node])

        if parents_dict[node]:
            parent = parents_dict[node][0]

            extensional_lengths[node_id][3] = len(parents_dict[parent])
            extensional_lengths[node_id][4] = len(graph[parent]) - 1

    return json.dumps(extensional_lengths)


if __name__ == "__main__":
    with open("graph.csv", "r") as file:
        data = file.read()

    print(main(data))
