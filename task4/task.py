import csv
import math


def load_data(file_path: str) -> list[list[int]]:
    with open(file_path) as f:
        reader = csv.reader(f)
        data = list(reader)

    data = [list(map(int, row[1:])) for row in data[1:]]
    return data


def task():
    data = load_data("data.csv")
    total_sum = sum(sum(row) for row in data)

    probabilities = [[element / total_sum for element in row] for row in data]

    p_y = [sum(row) for row in probabilities]
    p_x = [sum(row) for row in zip(*probabilities)]

    h_x = sum(-p_y[i] * math.log2(p_y[i]) for i in range(len(p_y)))
    h_y = sum(-p_x[i] * math.log2(p_x[i]) for i in range(len(p_x)))

    h_xy = 0
    for row in probabilities:
        for prob in row:
            h_xy += -prob * math.log2(prob)

    h_x_y = h_xy - h_y
    info_gain = h_x - h_x_y

    return [h_xy, h_x, h_y, h_x_y, info_gain]


if __name__ == "__main__":
    print(task())
