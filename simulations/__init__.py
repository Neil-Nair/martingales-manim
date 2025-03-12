"""
Stochastic simulations behind the martingales presentation.

random_walk  simple random walks, exit times, gambler's ruin, doubling strategy
brownian     Brownian paths, first hitting times, the Lévy distribution
verify       Monte Carlo checks of every closed form against simulation
             (run with: python -m simulations.verify)
"""

from .random_walk import (
    simple_random_walk,
    random_walk_ensemble,
    rescaled_random_walk,
    first_exit_index,
    simulate_exit,
    prob_hit_upper_first,
    expected_exit_time,
    doubling_strategy,
)
from .brownian import (
    brownian_path,
    first_hitting_index,
    simulate_hitting_times,
    laplace_transform_hitting_time,
    levy_pdf,
    levy_cdf,
    levy_mode,
    levy_median,
)
