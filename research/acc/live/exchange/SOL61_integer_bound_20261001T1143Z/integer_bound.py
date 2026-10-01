"""Exact lower bounds in the integer exponent projection of capped AC paths.

Standard library only. Applies to ac-r2-v1's fourteen moves, both ordered
unit finishes, and paths whose total relator length never exceeds `cap`.
This is not a bound for unrestricted Stable moves or uncapped AC paths.
"""
from collections import deque
from math import inf


def advance(matrix, move):
    a, b, c, d = matrix
    if move == 0:
        return -a, -b, c, d
    if move == 1:
        return a, b, -c, -d
    if move == 2:
        return a+c, b+d, c, d
    if move == 3:
        return a-c, b-d, c, d
    if move == 4:
        return a, b, c+a, d+b
    if move == 5:
        return a, b, c-a, d-b
    if 6 <= move < 14:
        return matrix
    raise ValueError('AC move must be in 0..13')


class IntegerLowerBound:
    def __init__(self, cap):
        if type(cap) is not int or not 2 <= cap <= 38:
            raise ValueError('supported cap range is 2..38')
        self.cap = cap
        root = (1, 0, 0, 1)
        self.distance = {root: 0}
        queue = deque([root])
        while queue:
            state = queue.popleft()
            for move in range(6):
                target = advance(state, move)
                if sum(map(abs, target)) <= cap and target not in self.distance:
                    self.distance[target] = self.distance[state] + 1
                    queue.append(target)

    def matrix_bound(self, matrix, finish='xy'):
        matrix = tuple(matrix)
        if len(matrix) != 4 or any(type(v) is not int for v in matrix):
            raise ValueError('matrix must have four integer entries in row order')
        if sum(map(abs, matrix)) > self.cap:
            raise ValueError('matrix lies outside this projected cap')
        if finish == 'yx':
            matrix = matrix[2:] + matrix[:2]
        elif finish != 'xy':
            raise ValueError('finish must be xy or yx')
        return self.distance.get(matrix, inf)

    def bound(self, state, finish='xy'):
        if len(state) != 2:
            raise ValueError('an AC state must have two relators')
        if sum(map(len, state)) > self.cap:
            raise ValueError('state exceeds the full-path cap used for this bound')
        if any(type(c) is not int or c not in (1, -1, 2, -2) for w in state for c in w):
            raise ValueError('letters must be official signed integers')
        matrix = tuple(sum(1 if c == g else -1 if c == -g else 0 for c in w)
                       for w in state for g in (1, 2))
        return self.matrix_bound(matrix, finish)
