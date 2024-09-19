import csv
import json


def read_graph_from_csv(file_path: str) -> dict:
    with open(file_path, "r") as file:
        lines = file.readlines()

    reader = csv.reader(lines[1:], delimiter=",")
    graph = {}
    for row in reader:
        if row[0] not in graph:
            graph[row[0]] = []
        if row[1] not in graph:
            graph[row[1]] = []
        graph[row[0]].append(row[1])
        graph[row[1]].append(row[0])

    return graph


def write_graph_to_csv(graph: dict, file_path: str) -> None:
    with open(file_path, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["source", "target"])
        for edge in graph_to_list_of_edges(graph):
            writer.writerow(edge)


def read_graph_from_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        content = file.read()

    return json.loads(content)["nodes"]


def write_graph_to_json(graph: dict, file_path: str) -> None:
    with open(file_path, "w") as file:
        content = {"nodes": graph}
        file.write(json.dumps(content))


def graph_to_connectivity_matrix(graph: dict) -> list:
    nodes = get_graph_nodes(graph)
    node_index = {node: idx for idx, node in enumerate(nodes)}
    size = len(nodes)
    matrix = [[0] * size for _ in range(size)]
    
    for node, targets in graph.items():
        i = node_index[node]
        for target in targets:
            j = node_index[target]
            matrix[i][j] = 1
    
    return matrix


def get_graph_nodes(graph: dict) -> list:
    nodes = set(graph.keys())
    for targets in graph.values():
        nodes.update(targets)
    return sorted(nodes)


def graph_to_list_of_edges(graph: dict) -> list:
    edges = set()
    for source, targets in graph.items():
        for target in targets:
            edge = tuple(sorted((source, target)))
            edges.add(edge)
    return list(edges)


def print_matrix(matrix: list) -> None:
    for row in matrix:
        print(row)


def print_graph(graph: dict) -> None:
    print(json.dumps(graph, indent=4))


def main() -> None:
    graph = read_graph_from_csv("graph.csv")
    print("1. Список смежности")
    print_graph(graph)

    print(f"2. Матрица смежности:")
    print_matrix(graph_to_connectivity_matrix(graph))

    edges = graph_to_list_of_edges(graph)
    print(f"3. Список ребер: {edges}")

    write_graph_to_json(graph, "graph_new.json")
    write_graph_to_csv(graph, "graph_new.csv")
    print(f"Результаты записаны в файлы graph_new.json и graph_new.csv")


if __name__ == "__main__":
    main()
