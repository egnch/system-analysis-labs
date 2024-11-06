import json


def flatten(data: list[int | list[int]]) -> list[int]:
    result = []
    for element in data:
        if isinstance(element, list):
            result.extend(element)
        else:
            result.append(element)
    return result


def load_test_data() -> tuple[str, str]:
    with open("a.json") as f:
        a = f.read()
    with open("b.json") as f:
        b = f.read()
    return a, b


def make_positions(x: list[int | list[int]]) -> dict[int, int]:
    positions = {}
    for index, element in enumerate(x):
        if not isinstance(element, list):
            positions[element] = index
            continue
        for value in element:
            positions[value] = index
    return positions


def make_relation_matrix(x: list[int | list[int]]) -> list[list[int]]:
    positions = make_positions(x)

    flat_x = sorted(flatten(x))
    result = [[0 for _ in range(len(flat_x))] for _ in range(len(flat_x))]

    for i in range(len(flat_x)):
        for j in range(len(flat_x)):
            if positions[flat_x[i]] <= positions[flat_x[j]]:
                result[i][j] = 1

    return result


def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:
    return [
        [matrix[j][i] for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]


def logical_and(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    len_x = len(a)
    len_y = len(a[0])
    return [
        [a[i][j] and b[i][j] for j in range(len_y)]
        for i in range(len_x)
    ]


def logical_or(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    len_x = len(a)
    len_y = len(a[0])
    return [
        [a[i][j] or b[i][j] for j in range(len_y)]
        for i in range(len_x)
    ]


def print_matrix(matrix: list[list[int]]) -> None:
    for row in matrix:
        print(" ".join(str(x) for x in row))


def task(a: str, b: str) -> str:
    a = json.loads(a)
    b = json.loads(b)

    a_elements = flatten(a)
    b_elements = flatten(b)

    if len(a_elements) != len(b_elements):
        raise ValueError("Arrays have different lengths")

    y_a = make_relation_matrix(a)
    y_b = make_relation_matrix(b)

    y_ab = logical_and(y_a, y_b)
    y_ab_t = logical_and(transpose_matrix(y_a), transpose_matrix(y_b))

    y_ab_or_ab_t = logical_or(y_ab, y_ab_t)
    contradiction_core = []

    for i in range(len(y_ab_or_ab_t)):
        for j in range(i, len(y_ab_or_ab_t[0])):
            if y_ab_or_ab_t[i][j] == 0:
                contradiction_core.append((i + 1, j + 1))

    return json.dumps(contradiction_core)


if __name__ == "__main__":
    result = task(*load_test_data())
    print(result)
