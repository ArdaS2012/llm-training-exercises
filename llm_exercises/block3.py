"""Prepared data, rendering and structural feedback; student steps stay in TODOs."""
import math
import random
from collections import Counter

Q = K = [[1, 0], [0, 1], [1, 1]]
V = [[1, 0], [0, 1], [1, 1]]
POSITIONS = ['A', 'B', 'C']
CANDIDATES = ['cat', 'dog', 'bird', 'fish']
LOGITS = [2.0, 1.0, 0.0, -1.0]
SCORES = [[sum(a*b for a, b in zip(q, k))/math.sqrt(2) for k in K] for q in Q]


def row_softmax(row):
    """Supplied Block 2 operation, reused only for the attention heatmaps."""
    shifted = [math.exp(x-max(row)) for x in row]
    return [x/sum(shifted) for x in shifted]


def check_mask(function):
    try:
        for scores in [SCORES, [[7]], [[-2, 0], [1, -3]]]:
            result = function([row[:] for row in scores])
            if result is None:
                return False, 'TODO 1 is waiting for your mask.'
            n = len(scores)
            if len(result) != n or any(len(row) != n for row in result):
                return False, 'Keep the square score-table shape.'
            for i in range(n):
                for j in range(n):
                    if j <= i and result[i][j] != scores[i][j]:
                        return False, 'Keep past positions and the diagonal unchanged.'
                    if j > i and result[i][j] != -math.inf:
                        return False, 'Future columns must have negative infinity, not zero.'
        return True, 'Mask passed: diagonal allowed, future blocked, including a single position.'
    except Exception as exc:
        return False, f'Check mask shape and return value: {exc}'


def valid_probabilities(p, size):
    return (isinstance(p, (list, tuple)) and len(p) == size
            and all(isinstance(x, (int, float)) and math.isfinite(x) and x >= 0 for x in p)
            and math.isclose(sum(p), 1, abs_tol=1e-9))


def check_temperature(function):
    try:
        results = [function(LOGITS[:], t) for t in [0.5, 1, 2]]
        if any(p is None for p in results):
            return False, 'TODO 2 is waiting for your probabilities.'
        if not all(valid_probabilities(p, 4) for p in results):
            return False, 'Return four finite nonnegative probabilities that sum to one.'
        if not results[0][0] > results[1][0] > results[2][0]:
            return False, 'For these fixed logits, lower temperature should sharpen the distribution.'
        for t, p in zip([0.5, 1, 2], results):
            if not math.isclose(math.log(p[0]/p[1]), 1/t, abs_tol=1e-9):
                return False, 'Check division by temperature before exponentiating.'
            if any(not math.isclose(a, b, abs_tol=1e-9) for a, b in zip(p, function([z+1000 for z in LOGITS], t))):
                return False, 'A common logit shift should not change probabilities.'
        if not valid_probabilities(function([0, 0], 1), 2) or function([5], 1) != [1.0]:
            return False, 'Check tied logits and a single candidate.'
        return True, 'Temperature passed: normalization, sharpening, ties and numerical stability.'
    except Exception as exc:
        return False, f'Check temperature softmax and subtract the largest scaled logit: {exc}'


def check_top_k(function):
    try:
        for p in [[0.1, 0.4, 0.2, 0.3], [0.25]*4, [1.0]]:
            for k in range(1, len(p)+1):
                result = function(p[:], k)
                if result is None:
                    return False, 'TODO 3 is waiting for your retained probabilities.'
                if not valid_probabilities(result, len(p)):
                    return False, 'Keep the original vector length; normalize the retained mass.'
                kept = [i for i, x in enumerate(result) if x > 0]
                if len(kept) != k or any(p[i] < p[j] for i in kept for j in range(len(p)) if j not in kept):
                    return False, 'Keep exactly k highest-probability entries; choose a consistent tie order.'
                ratios = [result[i]/p[i] for i in kept]
                if any(not math.isclose(x, ratios[0], abs_tol=1e-9) for x in ratios):
                    return False, 'Preserve relative probabilities among kept entries.'
        return True, 'Top-k passed: k=1, full vocabulary, ties and renormalization.'
    except Exception as exc:
        return False, f'Check top-k indices and return value: {exc}'


def comparison(temperature_function, top_k_function, seed=42, draws=200):
    rows = []
    for t in [0.5, 2.0]:
        for k in [1, 2]:
            p = top_k_function(temperature_function(LOGITS[:], t), k)
            rng = random.Random(seed)  # Reset once per controlled run, never per draw.
            counts = Counter(rng.choices(CANDIDATES, weights=p, k=draws))
            for label, probability in zip(CANDIDATES, p):
                rows.append({'T': t, 'k': k, 'Candidate': label, 'Probability': probability,
                             'Count': counts[label], 'Observed fraction': counts[label]/draws})
    return rows


def heatmap_svg(weights, title):
    from html import escape
    items = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 300" role="img" aria-label="{escape(title)}"><rect width="440" height="300" fill="white"/><g font-family="sans-serif" fill="#172033"><text x="20" y="24">{escape(title)}</text><text x="140" y="50">Source / Key column →</text><text x="8" y="85">Query ↓</text>']
    for j, label in enumerate(POSITIONS):
        items.append(f'<text x="{155+j*85}" y="80">{label}</text>')
    for i, row in enumerate(weights):
        items.append(f'<text x="80" y="{120+i*55}">{POSITIONS[i]}</text>')
        for j, p in enumerate(row):
            items.append(f'<rect x="{125+j*85}" y="{90+i*55}" width="80" height="50" fill="rgb({int(240-110*p)},{int(245-70*p)},250)"/><text x="{138+j*85}" y="{120+i*55}">{p:.3f}</text>')
    return ''.join(items)+'</g><text x="20" y="280" font-family="sans-serif">Weight scale: 0 (pale) → 1 (blue)</text></svg>'
