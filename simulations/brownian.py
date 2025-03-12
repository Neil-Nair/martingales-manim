"""
Brownian motion paths, first hitting times, and the Lévy distribution.

As in ``random_walk``, samplers accept ``rng`` (recommended) or ``seed``
(legacy global generator, used by the animation scenes so their frozen
seeds reproduce the paths shown in the talk).
"""

import math

import numpy as np


# ─────────────────────────────────────────────────────────────
# Path samplers
# ─────────────────────────────────────────────────────────────
def brownian_path(n_steps, dt, scale=1.0, seed=None, rng=None):
    """
    Discretised Brownian motion B_0 = 0, B_{k+1} = B_k + N(0, dt).

    Returns (t, B), each of length n_steps + 1.  ``scale`` multiplies the
    path (sigma * B_t), which the scenes use to fit the plot.
    """
    if seed is not None and rng is None:
        np.random.seed(seed)
    normal = rng.normal if rng is not None else np.random.normal
    dB = normal(0, np.sqrt(dt), n_steps)
    B = np.concatenate([[0], np.cumsum(dB)]) * scale
    t = np.arange(len(B)) * dt
    return t, B


def first_hitting_index(path, level):
    """
    Index of the first k >= 1 with path[k] >= level (the hitting time T_a),
    or len(path) - 1 if the level is never reached.
    """
    for k in range(1, len(path)):
        if path[k] >= level:
            return k
    return len(path) - 1


def simulate_hitting_times(a, n_paths, dt=1e-3, t_max=50.0, rng=None):
    """
    Monte Carlo sample of T_a = inf{t : B_t >= a} for standard BM.

    Paths that have not hit a by t_max are returned as np.inf (T_a is
    finite almost surely, but has a heavy tail with infinite mean).

    Checking the level only on the time grid would miss crossings that
    happen between grid points and bias T_a upward.  A Brownian bridge
    correction removes this: given B_k = x and B_{k+1} = y, both below a,
    the path crossed a in between with probability
    exp(-2 (a - x)(a - y) / dt).
    """
    rng = np.random.default_rng() if rng is None else rng
    n_steps = int(t_max / dt)
    B = np.zeros(n_paths)
    T = np.full(n_paths, np.inf)
    alive = np.ones(n_paths, dtype=bool)
    for k in range(1, n_steps + 1):
        idx = np.flatnonzero(alive)
        if idx.size == 0:
            break
        x = B[idx]
        y = x + rng.normal(0, math.sqrt(dt), idx.size)
        B[idx] = y
        p_bridge = np.exp(-2 * (a - x) * np.maximum(a - y, 0) / dt)
        crossed = (y >= a) | (rng.random(idx.size) < p_bridge)
        hit = idx[crossed]
        T[hit] = k * dt
        alive[hit] = False
    return T


# ─────────────────────────────────────────────────────────────
# Closed forms from the exponential martingale
# ─────────────────────────────────────────────────────────────
def laplace_transform_hitting_time(a, lam):
    """
    E[exp(-lam * T_a)] = exp(-a * sqrt(2 * lam)).

    From optional stopping applied to exp(alpha B_t - alpha^2 t / 2),
    with lam = alpha^2 / 2.
    """
    return math.exp(-a * math.sqrt(2 * lam))


def levy_pdf(t, a):
    """Density of T_a: a / sqrt(2 pi t^3) * exp(-a^2 / (2t))."""
    t = np.asarray(t, dtype=float)
    return a / np.sqrt(2 * np.pi * t**3) * np.exp(-a**2 / (2 * t))


def levy_cdf(t, a):
    """P(T_a <= t) = erfc(a / sqrt(2t)) = 2 P(B_t >= a) (reflection principle)."""
    return np.vectorize(lambda s: math.erfc(a / math.sqrt(2 * s)))(t)


def levy_mode(a):
    """Most likely hitting time, a^2 / 3."""
    return a**2 / 3


def levy_median(a):
    """Median hitting time, a^2 / (2 * erfcinv(1/2)^2) ~ 2.198 a^2."""
    return a**2 / (2 * 0.4769362762044699**2)
