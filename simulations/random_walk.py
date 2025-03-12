"""
Simple symmetric random walks and the martingale results built on them.

Every sampler takes either a ``seed`` or a ``rng``:

* ``rng`` (a ``numpy.random.Generator``) is the recommended interface for
  new experiments, such as the Monte Carlo checks in ``simulations.verify``.
* ``seed`` (or neither) draws from NumPy's legacy global generator.  The
  animation scenes use this path so the frozen seeds reproduce exactly the
  same paths that appear in the presentation.
"""

import numpy as np


def _steps(n_steps, rng=None):
    """n_steps independent +/-1 steps with probability 1/2 each."""
    if rng is not None:
        return rng.choice([-1, 1], size=n_steps)
    return np.random.choice([-1, 1], size=n_steps)


# ─────────────────────────────────────────────────────────────
# Path samplers
# ─────────────────────────────────────────────────────────────
def simple_random_walk(n_steps, start=0, seed=None, rng=None):
    """
    One path X_0, ..., X_n of a simple symmetric random walk.

    X_0 = start and X_{k+1} = X_k +/- 1 with probability 1/2 each.
    Returns an integer array of length n_steps + 1.
    """
    if seed is not None and rng is None:
        np.random.seed(seed)
    steps = _steps(n_steps, rng)
    return np.concatenate([[start], start + np.cumsum(steps)])


def random_walk_ensemble(n_walks, n_steps, start=0, seed=None, rng=None):
    """
    n_walks independent walks, seeded once and then drawn one after another.
    Returns an array of shape (n_walks, n_steps + 1).
    """
    if seed is not None and rng is None:
        np.random.seed(seed)
    return np.array([simple_random_walk(n_steps, start, rng=rng)
                     for _ in range(n_walks)])


def rescaled_random_walk(n_steps, scale=4.0, seed=None, rng=None):
    """
    Diffusively rescaled walk X_k / sqrt(n), multiplied by ``scale``.

    As n grows, this path converges in distribution to Brownian motion on
    [0, 1] (Donsker's theorem).  Plotted against np.linspace(0, T, n + 1),
    it is the "random walk becomes Brownian motion" picture.
    """
    walk = simple_random_walk(n_steps, seed=seed, rng=rng)
    return walk / np.sqrt(n_steps) * scale


# ─────────────────────────────────────────────────────────────
# Stopping times
# ─────────────────────────────────────────────────────────────
def first_exit_index(path, lower, upper):
    """
    Stopping time T = min{k : X_k <= lower or X_k >= upper}.

    Returns the index of the first exit, or len(path) - 1 if the path
    never leaves (lower, upper).
    """
    for k, x in enumerate(path):
        if x <= lower or x >= upper:
            return k
    return len(path) - 1


def simulate_exit(start, lower, upper, n_sims, rng=None, max_steps=10**6):
    """
    Run n_sims walks from ``start`` until they leave (lower, upper).

    Returns (hit_upper, exit_time): a boolean array saying which barrier was
    reached and an integer array of exit times.
    """
    rng = np.random.default_rng() if rng is None else rng
    x = np.full(n_sims, start, dtype=np.int64)
    t = np.zeros(n_sims, dtype=np.int64)
    alive = (x > lower) & (x < upper)
    for _ in range(max_steps):
        if not alive.any():
            break
        idx = np.flatnonzero(alive)
        x[idx] += rng.choice([-1, 1], size=idx.size)
        t[idx] += 1
        alive[idx] = (x[idx] > lower) & (x[idx] < upper)
    return x >= upper, t


# ─────────────────────────────────────────────────────────────
# Closed forms from the optional stopping theorem
# ─────────────────────────────────────────────────────────────
def prob_hit_upper_first(start, lower, upper):
    """
    P(hit upper before lower) = (start - lower) / (upper - lower).

    X_n is a martingale, so E[X_T] = X_0 by optional stopping, and
    X_T only takes the values lower and upper.
    """
    return (start - lower) / (upper - lower)


def expected_exit_time(start, lower, upper):
    """
    E[T] = (start - lower) * (upper - start).

    M_n = (X_n - start)^2 - n is a martingale; optional stopping gives
    E[T] = E[(X_T - start)^2], which the hitting probabilities evaluate.
    """
    return (start - lower) * (upper - start)


# ─────────────────────────────────────────────────────────────
# The doubling ("martingale") betting strategy
# ─────────────────────────────────────────────────────────────
def doubling_strategy(n_sims, bankroll_limit, base_bet=1, rng=None):
    """
    Bet base_bet on a fair coin, double after every loss, stop at the first
    win, or when the next bet would exceed bankroll_limit.

    Returns the final profit of each run.  Every completed run wins exactly
    base_bet, but the rare run that hits the limit loses everything staked,
    so the mean profit is 0: optional stopping with a bounded stopping time.
    """
    rng = np.random.default_rng() if rng is None else rng
    profits = np.empty(n_sims)
    for i in range(n_sims):
        bet, lost = base_bet, 0
        while True:
            if rng.random() < 0.5:
                profits[i] = bet - lost
                break
            lost += bet
            bet *= 2
            if lost + bet > bankroll_limit:
                profits[i] = -lost
                break
    return profits
