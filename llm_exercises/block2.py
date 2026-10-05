"""Supplied toy inputs and feedback, without completed student calculations."""
import math
from llm_exercises.block3 import heatmap_svg

Q = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
K = [row[:] for row in Q]
V = [[2.0, 0.0], [0.0, 2.0], [1.0, 1.0]]


def changed_inputs(target, row, column, delta):
    arrays = {name: [values[:] for values in source] for name, source in [('Q', Q), ('K', K), ('V', V)]}
    arrays[target][row][column] += delta
    return arrays['Q'], arrays['K'], arrays['V']


def matrix_valid(value, rows, columns):
    return (isinstance(value, (list, tuple)) and len(value) == rows
            and all(isinstance(row, (list, tuple)) and len(row) == columns
                    and all(isinstance(x, (int, float)) and math.isfinite(x) for x in row) for row in value))


def check_scores(function):
    try:
        result = function(Q, K)
        if result is None:
            return False, 'TODO 1 is waiting for your scaled scores.'
        if not matrix_valid(result, 3, 3):
            return False, 'Return a finite 3 × 3 table: Query rows, Key columns.'
        if not math.isclose(result[0][0], 1/math.sqrt(2), abs_tol=1e-9):
            return False, 'Check the dot product and scaling by feature width, not position count.'
        if result[0][1] != 0 or result[0][2] != result[0][0]:
            return False, 'Compare each Query with every Key, retaining source order.'
        rectangular = function([[1, 0]], [[0, 1], [1, 0]])
        if not matrix_valid(rectangular, 1, 2) or rectangular[0][0] != 0:
            return False, 'Output dimensions follow Query count × Key count.'
        single = function([[2]], [[3]])
        if not matrix_valid(single, 1, 1) or single[0][0] != 6:
            return False, 'Feature width one should leave the dot product unchanged.'
        return True, 'Scores passed: axes, scaling and unequal sequence lengths.'
    except Exception as exc:
        return False, f'Check score dimensions and return value: {exc}'


def check_softmax(function):
    try:
        result = function([[0, 1, 2], [0, 0, 0]])
        if result is None:
            return False, 'TODO 2 is waiting for your row probabilities.'
        if not matrix_valid(result, 2, 3) or any(x < 0 for row in result for x in row):
            return False, 'Return a finite nonnegative table of the same shape.'
        if any(not math.isclose(sum(row), 1, abs_tol=1e-9) for row in result):
            return False, 'Normalize each row separately, not the whole matrix.'
        if not result[0][0] < result[0][1] < result[0][2]:
            return False, 'Larger scores should receive larger weights.'
        if not all(math.isclose(x, 1/3, abs_tol=1e-9) for x in result[1]):
            return False, 'Equal scores should produce equal probabilities.'
        if not math.isclose(math.log(result[0][2]/result[0][1]), 1, abs_tol=1e-9):
            return False, 'Use exponentials, not direct division of raw scores.'
        shifted = function([[1000, 1001, 1002], [-1000, -1000, -1000]])
        if not matrix_valid(shifted, 2, 3) or any(not math.isclose(a, b, abs_tol=1e-9) for row_a, row_b in zip(result, shifted) for a,b in zip(row_a,row_b)):
            return False, 'Subtract each row maximum before exponentiating.'
        if function([[9]]) != [[1.0]]:
            return False, 'A single source has total probability one.'
        return True, 'Softmax passed: row sums, ties, order and large-score stability.'
    except Exception as exc:
        return False, f'Check row-wise softmax: {exc}'


def check_values(function):
    try:
        result = function([[1, 0], [0, 1]], [[2, -1, 3], [4, 5, -2]])
        if result is None:
            return False, 'TODO 3 is waiting for your contextualized vectors.'
        if result != [[2, -1, 3], [4, 5, -2]]:
            return False, 'A one-hot weight row should copy its selected Value vector.'
        blended = function([[0.5, 0.5]], [[2, -1, 3], [4, 5, -2]])
        if not matrix_valid(blended, 1, 3) or blended != [[3, 2, 0.5]]:
            return False, 'Mix every Value coordinate across source positions; keep d_v output columns.'
        return True, 'Value mixing passed: selected source, weighted average and output shape.'
    except Exception as exc:
        return False, f'Check weighted Values and matrix axes: {exc}'


def pipeline(score_function, softmax_function, value_function, q, k, v, ready):
    """Safely render intermediate work; later unfinished TODOs do not hide earlier stages."""
    scores = score_function(q,k) if ready[0] else None
    weights = softmax_function(scores) if scores is not None and ready[1] else None
    outputs = value_function(weights,v) if weights is not None and ready[2] else None
    return dict(scores=scores, weights=weights, outputs=outputs)


def matrix_rows(matrix):
    return [{'Query': 'ABC'[i], **{f'Column {j}': value for j,value in enumerate(row)}} for i,row in enumerate(matrix)]
