"""
Check every result in the presentation against Monte Carlo simulation.

    python -m simulations.verify            # print the comparison tables
    python -m simulations.verify --plot     # also show figures (needs matplotlib)
    python -m simulations.verify --sims 50000 --seed 1
"""

import argparse

import numpy as np

from .random_walk import (
    simulate_exit,
    prob_hit_upper_first,
    expected_exit_time,
    doubling_strategy,
)
from .brownian import (
    simulate_hitting_times,
    laplace_transform_hitting_time,
    levy_cdf,
    levy_pdf,
)


def _row(label, theory, estimate, stderr):
    print(f"  {label:<34} theory {theory:>9.4f}   simulated {estimate:>9.4f} "
          f"± {1.96 * stderr:.4f}")


def check_doubling(n_sims, rng):
    print("\nDoubling strategy (fair coin, bankroll limit 1023)")
    p = doubling_strategy(n_sims, bankroll_limit=1023, rng=rng)
    _row("E[profit]", 0.0, p.mean(), p.std() / np.sqrt(n_sims))
    _row("P(ruin before first win)", 2**-10, (p < 0).mean(),
         np.sqrt((p < 0).mean() * (1 - (p < 0).mean()) / n_sims))
    return p


def check_gamblers_ruin(n_sims, rng, start=3, lower=0, upper=10):
    print(f"\nRandom walk from {start}, barriers at {lower} and {upper}")
    hit_upper, T = simulate_exit(start, lower, upper, n_sims, rng=rng)
    p = hit_upper.mean()
    _row("P(hit upper first)", prob_hit_upper_first(start, lower, upper),
         p, np.sqrt(p * (1 - p) / n_sims))
    _row("E[T]", expected_exit_time(start, lower, upper),
         T.mean(), T.std() / np.sqrt(n_sims))
    return hit_upper, T


def check_brownian_hitting(n_paths, rng, a=1.0, dt=1e-3, t_max=20.0):
    print(f"\nBrownian first hitting time of a = {a} (dt = {dt})")
    T = simulate_hitting_times(a, n_paths, dt=dt, t_max=t_max, rng=rng)
    for t in (0.5, 1.0, 5.0):
        q = (T <= t).mean()
        _row(f"P(T_a <= {t})", float(levy_cdf(t, a)), q,
             np.sqrt(q * (1 - q) / n_paths))
    for lam in (0.5, 2.0):
        v = np.exp(-lam * T)        # exp(-inf) = 0 for paths not yet hit
        _row(f"E[exp(-{lam} T_a)]", laplace_transform_hitting_time(a, lam),
             v.mean(), v.std() / np.sqrt(n_paths))
    return T


def plot(profits, T_walk, T_bm, a=1.0):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

    ax = axes[0]
    ax.hist(profits, bins=60, color="#1565C0")
    ax.set_yscale("log")
    ax.set_title("Doubling strategy: final profit")
    ax.set_xlabel("profit")

    ax = axes[1]
    ax.hist(T_walk, bins=60, color="#2E7D32")
    ax.set_title("Random walk exit time T")
    ax.set_xlabel("steps")

    ax = axes[2]
    finite = T_bm[np.isfinite(T_bm)]
    t = np.linspace(0.01, 6, 400)
    ax.hist(finite[finite <= 6], bins=120, density=True, color="#F57F17",
            alpha=0.6, label="simulated")
    ax.plot(t, levy_pdf(t, a) / levy_cdf(6, a), color="#C62828",
            label="Lévy density")
    ax.set_title(f"Brownian hitting time of a = {a} (T ≤ 6)")
    ax.set_xlabel("t")
    ax.legend()

    fig.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--sims", type=int, default=20000,
                        help="number of simulations per check (default 20000)")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--plot", action="store_true",
                        help="show histograms (requires matplotlib)")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    print(f"Monte Carlo checks, {args.sims} simulations each, "
          f"95% intervals shown as ±")
    profits = check_doubling(args.sims, rng)
    _, T_walk = check_gamblers_ruin(args.sims, rng)
    T_bm = check_brownian_hitting(args.sims, rng)

    if args.plot:
        plot(profits, T_walk, T_bm)


if __name__ == "__main__":
    main()
