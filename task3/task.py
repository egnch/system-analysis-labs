import csv
import math


def read_graph_from_csv(csv_data: str, with_titles: bool = False) -> dict[str, list[str]]:
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


def count_all_children(graph: dict[str, list[str]]) -> dict[str, int]:
    result = {}

    def dfs(from_node: str) -> int:
        if from_node in result:
            return result[from_node]

        total = 0
        for child in graph[from_node]:
            total += 1 + dfs(child)
        result[from_node] = total
        return total

    for node in graph:
        dfs(node)

    return result


def reverse_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    reversed_graph = {node: [] for node in graph}
    for node in graph:
        for child in graph[node]:
            reversed_graph[child].append(node)
    return reversed_graph


def main(data: str) -> float:
    graph = read_graph_from_csv(data)

    nodes = set(graph.keys()).union(*graph.values())
    nodes = {node: i for i, node in enumerate(sorted(nodes))}

    reversed_graph = reverse_graph(graph)
    children_count = count_all_children(graph)
    parents_count = count_all_children(reversed_graph)

    extensional_lengths = [[0] * 5 for _ in range(len(nodes))]

    for node in graph:
        node_id = nodes[node]
        extensional_lengths[node_id][0] = len(graph[node])
        extensional_lengths[node_id][1] = 1 if parents_count[node] > 0 else 0
        extensional_lengths[node_id][2] = children_count[node] - len(graph[node])

        if reversed_graph[node]:
            parent = reversed_graph[node][0]

            extensional_lengths[node_id][3] = parents_count[parent]
            extensional_lengths[node_id][4] = len(graph[parent]) - 1

    entropy = 0.0
    for i in range(len(nodes)):
        for j in range(5):
            probability = extensional_lengths[i][j] / (len(nodes) - 1)
            if probability > 0:
                entropy += probability * math.log(probability, 2)

    return -entropy


if __name__ == "__main__":
    with open("graph.csv", "r") as file:
        print(main(file.read()))
