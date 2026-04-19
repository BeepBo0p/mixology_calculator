import argparse
import math
from collections import defaultdict

import yaml


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def compute_shopping_list(config: dict) -> dict[str, float]:
    people = config["people"]
    totals: dict[str, float] = defaultdict(float)

    for drink in config["drinks"]:
        interest = drink["interest_percentage"]
        servings_per_person = drink["servings"]
        total_servings = round(people * interest) * servings_per_person

        for mixer in drink["mixers"]:
            totals[mixer["name"]] += total_servings * mixer["amount_ml"]

    return dict(totals)


def print_shopping_list(
    people: int, totals: dict[str, float], bottle_size_ml: int = 500
) -> None:
    print(f"\nShopping List for {people} people:")
    print("─" * 56)

    col_w = max(len(n) for n in totals) + 2

    for mixer, ml in sorted(totals.items()):
        bottles = math.ceil(ml / bottle_size_ml)
        bottle_label = f"{bottles} bottle{'s' if bottles != 1 else ''}"
        print(
            f"  {mixer:<{col_w}}: {ml:>7,.0f} mL  ({ml / 1000:.2f} L)   {bottle_label}"
        )

    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate mixer quantities for a party."
    )
    parser.add_argument(
        "--config", default="config.yaml", help="Path to config YAML file"
    )
    args = parser.parse_args()

    config = load_config(args.config)
    totals = compute_shopping_list(config)

    bottle_size_ml = config["mixer_bottle_size_ml"]

    if bottle_size_ml:
        print_shopping_list(config["people"], totals, bottle_size_ml)
    else:
        print_shopping_list(config["people"], totals)


if __name__ == "__main__":
    main()
