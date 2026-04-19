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
    people: int,
    totals: dict[str, float],
    bottle_size_ml: int = 500,
    fruit_yields: dict[str, tuple[str, str, float]] | None = None,
) -> None:
    if fruit_yields is None:
        fruit_yields = {}

    print(f"\nShopping List for {people} people:")
    print("─" * 56)

    col_w = max(len(n) for n in totals) + 2

    for mixer, ml in sorted(totals.items()):
        if mixer in fruit_yields:
            singular, plural, ml_per_fruit = fruit_yields[mixer]
            count = math.ceil(ml / ml_per_fruit)
            quantity_label = f"{count} {singular if count == 1 else plural}"
        else:
            bottles = math.ceil(ml / bottle_size_ml)
            quantity_label = f"{bottles} bottle{'s' if bottles != 1 else ''}"
        print(
            f"  {mixer:<{col_w}}: {ml:>7,.0f} mL  ({ml / 1000:.2f} L)   {quantity_label}"
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

    bottle_size_ml = config.get("mixer_bottle_size_ml", 500)

    fruit_yields: dict[str, tuple[str, str, float]] = {}
    if ml := config.get("expected_juice_content_per_lime_ml"):
        fruit_yields["Lime Juice"] = ("lime", "limes", ml)
    if ml := config.get("expected_juice_content_per_lemon_ml"):
        fruit_yields["Lemon Juice"] = ("lemon", "lemons", ml)

    print_shopping_list(config["people"], totals, bottle_size_ml, fruit_yields)


if __name__ == "__main__":
    main()
