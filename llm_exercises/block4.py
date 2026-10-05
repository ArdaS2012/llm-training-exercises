"""Supplied output-layer training; the loss and scalar update remain student TODOs."""
import math
from html import escape

PREFIXES = ['The cat can', 'The bird can', 'The fish can']
VOCABULARY = ['meow', 'fly', 'swim', 'sleep']
TARGETS = [0, 1, 2]
FEATURES = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def softmax(logits):
    """Provided stable softmax from Block 3; not the new coding task."""
    weights = [math.exp(z - max(logits)) for z in logits]
    return [w / sum(weights) for w in weights]


def check_loss(function):
    try:
        values = [function(p) for p in [1.0, 0.5, 0.25, 0.1]]
        if any(x is None for x in values):
            return False, 'TODO 1 is waiting for your target loss.'
        if any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in values):
            return False, 'Return one finite number for each valid probability.'
        if not math.isclose(values[0], 0, abs_tol=1e-10) or not 0 < values[1] < values[2] < values[3]:
            return False, 'Certain targets have zero loss; less likely targets have greater loss.'
        if not math.isclose(math.exp(-values[1]), 0.5, abs_tol=1e-10) or not math.isclose(values[2], 2 * values[1], abs_tol=1e-10):
            return False, 'Use the negative natural logarithm, not 1-p or a base-10 logarithm.'
        for invalid in [0, -0.1, 1.1]:
            try:
                function(invalid)
            except ValueError:
                continue
            return False, 'Keep the supplied validation: valid target probabilities are 0 < p ≤ 1.'
        return True, 'Loss passed: probability boundary, ordering, natural-log scale and invalid inputs.'
    except Exception as exc:
        return False, f'Check the scalar return value and natural logarithm: {exc}'


def check_update(function):
    try:
        result = function(1.0, 0.4, 0.1)
        if result is None:
            return False, 'TODO 2 is waiting for your updated parameter.'
        for parameter, gradient, rate in [(1, 0.4, 0.1), (0, -0.8, 0.1), (-2, 3, 0), (0.5, 0, 0.8)]:
            changed = function(parameter, gradient, rate)
            if not isinstance(changed, (int, float)) or not math.isfinite(changed):
                return False, 'Return a finite scalar; the loop calls your step for each weight and bias.'
            if not math.isclose(parameter-changed, rate*gradient, abs_tol=1e-10):
                return False, 'Subtract the learning-rate-scaled gradient; zero rate/gradient must preserve the parameter.'
        return True, 'Update passed: gradient sign, learning-rate scaling and zero-update cases.'
    except Exception as exc:
        return False, f'Check parameter, gradient and learning rate: {exc}'


def train(loss_function, update_function, rate=0.5, steps=40):
    """Reset to zero on every run; full-batch gradient descent on a fixed feature table.

    z=HW+b; G=(P-one_hot_targets)/N; grad_W=H^T G; grad_b=sum_rows(G).
    Student functions supply the loss measurement and each scalar update.
    """
    if not 0 <= rate <= 100 or not isinstance(steps, int) or not 0 <= steps <= 200:
        raise ValueError('Use learning rate 0–100 and integer steps 0–200.')
    n, d, v = len(FEATURES), len(FEATURES[0]), len(VOCABULARY)
    weights, bias = [[0.0]*v for _ in range(d)], [0.0]*v
    history, snapshots = [], []
    for step in range(steps+1):
        logits = [[sum(h[a]*weights[a][j] for a in range(d))+bias[j] for j in range(v)] for h in FEATURES]
        probabilities = [softmax(row) for row in logits]
        if any(row[y] <= 0 for row, y in zip(probabilities, TARGETS)):
            return {'history': history, 'error': 'Target probability underflowed. Reduce the learning rate; real training uses log-softmax from logits.'}
        losses = [loss_function(row[y]) for row, y in zip(probabilities, TARGETS)]
        if any(x is None or not math.isfinite(x) for x in losses):
            raise ValueError('Complete the loss TODO before training.')
        history.append({'Step': step, 'Mean loss': sum(losses)/n})
        if step in [0, steps]:
            snapshots.append({'step': step, 'weights': [row[:] for row in weights], 'bias': bias[:],
                              'probabilities': probabilities, 'target_losses': losses})
        if step == steps:
            break
        # Provided derivative of softmax cross-entropy, averaged across training contexts.
        gradient_logits = [[(p[j]-(1 if j == y else 0))/n for j in range(v)] for p, y in zip(probabilities, TARGETS)]
        gradient_weights = [[sum(FEATURES[i][a]*gradient_logits[i][j] for i in range(n)) for j in range(v)] for a in range(d)]
        gradient_bias = [sum(row[j] for row in gradient_logits) for j in range(v)]
        weights = [[update_function(weights[a][j], gradient_weights[a][j], rate) for j in range(v)] for a in range(d)]
        bias = [update_function(bias[j], gradient_bias[j], rate) for j in range(v)]
    before, after = snapshots[0], snapshots[-1]
    rows = [{'Prefix': prefix, 'Target': VOCABULARY[y], 'Before p(target)': before['probabilities'][i][y],
             'After p(target)': after['probabilities'][i][y], 'Before loss': before['target_losses'][i],
             'After loss': after['target_losses'][i], 'After row sum': sum(after['probabilities'][i])}
            for i, (prefix, y) in enumerate(zip(PREFIXES, TARGETS))]
    return {'history': history, 'before': before, 'after': after, 'rows': rows, 'rate': rate, 'steps': steps}


def loss_plot(history, title='Mean training loss by update step'):
    """Accurate SVG plot, with zero-based axes and measured points; no smoothing."""
    ymax = max(1.5, max(row['Mean loss'] for row in history)*1.1)
    xmax = max(1, history[-1]['Step'])
    points = ' '.join(f"{70+row['Step']/xmax*520:.3f},{280-row['Mean loss']/ymax*220:.3f}" for row in history)
    ticks = ''.join(f'<text x="58" y="{284-i*220/4}" text-anchor="end">{ymax*i/4:.2f}</text>' for i in range(5))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 350" role="img" aria-label="{escape(title)}">'
            f'<rect width="640" height="350" fill="white"/><g font-family="sans-serif" font-size="14" fill="#172033">'
            f'<text x="70" y="24">{escape(title)}</text><text x="70" y="47">Loss (nats / target)</text>'
            f'<path d="M70 60V280H590" fill="none" stroke="#172033"/>{ticks}'
            f'<polyline points="{points}" fill="none" stroke="#476bff" stroke-width="2"/>'
            f'<text x="70" y="302">0</text><text x="590" y="302" text-anchor="end">{history[-1]["Step"]}</text>'
            '<text x="280" y="333">Update step (not elapsed time)</text></g></svg>')
