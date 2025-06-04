import time
import itertools
import math


def solve_tsp(points):
    n = len(points)

    if n <= 1:
        return [0], 0.0
    if n == 2:
        return [0, 1, 0], distance(points[0], points[1]) * 2

    min_path = None
    min_distance = float('inf')

    total_permutations = math.factorial(n - 1)
    processed = 0

    for perm in itertools.permutations(range(1, n)):
        path = [0] + list(perm) + [0]
        dist = total_distance(path, points)

        if dist < min_distance:
            min_distance = dist
            min_path = path

        processed += 1
        progress = int(processed / total_permutations * 100)
        if progress % 10 == 0:
            yield progress, None, None

    yield 100, min_path, min_distance


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def total_distance(path, points):
    return sum(distance(points[path[i]], points[path[i + 1]]) for i in range(len(path) - 1))
