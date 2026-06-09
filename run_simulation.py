#!/usr/bin/env python3
"""
Simple Monte Carlo simulation to test loyalty interventions for NorthSouth Coffee.

Simulates cohorts of customers over 6 months and compares baseline retention
to a set of proposed interventions.

Run: python3 run_simulation.py
"""
import random
import statistics


def simulate_cohort(n_customers, months, p_redeem=0.7, p_return_after_redeem=0.10, intervention_boost=0.0):
    """Simulate customers over `months`. Return metrics dict."""
    visits_per_customer = [0] * n_customers
    kept_after_first = 0

    for i in range(n_customers):
        # first month: signup and chance to redeem free drink
        if random.random() < p_redeem:
            visits = 1
            # subsequent monthly return probability
            p_return = min(0.6, p_return_after_redeem + intervention_boost)
            returned_after = False
            for m in range(1, months):
                if random.random() < p_return:
                    visits += 1
                    returned_after = True
            visits_per_customer[i] = visits
            if returned_after:
                kept_after_first += 1
        else:
            # did not redeem first reward within first month; assume low engagement
            visits_per_customer[i] = 0

    avg_visits = statistics.mean(visits_per_customer)
    pct_kept = kept_after_first / n_customers
    return {
        "avg_visits": avg_visits,
        "pct_kept_after_first": pct_kept,
        "visits_distribution_sample": visits_per_customer[:20],
    }


def run_experiments():
    n = 20000
    months = 6
    baseline = simulate_cohort(n, months, p_redeem=0.7, p_return_after_redeem=0.10, intervention_boost=0.0)

    interventions = {
        "micro_rewards": 0.10,   # more frequent small wins
        "onboarding": 0.07,      # better onboarding messaging
        "personalization": 0.12, # targeted offers
        "ux_friction_removal": 0.08, # smoother redemption
    }

    results = {"baseline": baseline}

    for name, boost in interventions.items():
        res = simulate_cohort(n, months, p_redeem=0.7, p_return_after_redeem=0.10, intervention_boost=boost)
        results[name] = res

    # combined intervention scenario
    combined_boost = sum(interventions.values())
    combined = simulate_cohort(n, months, p_redeem=0.7, p_return_after_redeem=0.10, intervention_boost=combined_boost)
    results["combined"] = combined

    print("NorthSouth Coffee loyalty simulation over {} months with {} customers".format(months, n))
    print()
    print("Baseline: avg visits per customer: {:.3f}, pct kept after first: {:.2%}".format(
        baseline["avg_visits"], baseline["pct_kept_after_first"]))
    print()

    for name in interventions:
        r = results[name]
        print("Intervention {:20s}: avg visits: {:.3f}, pct kept after first: {:.2%}".format(name, r["avg_visits"], r["pct_kept_after_first"]))

    r = results["combined"]
    print()
    print("Combined interventions     : avg visits: {:.3f}, pct kept after first: {:.2%}".format(r["avg_visits"], r["pct_kept_after_first"]))


if __name__ == "__main__":
    random.seed(42)
    run_experiments()
