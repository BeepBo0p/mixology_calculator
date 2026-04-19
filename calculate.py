import argparse
import math
from collections import defaultdict

import yaml


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def _sum_ingredients(config: dict, key: str) -> dict[str, float]:
    people = config["people"]
    totals: dict[str, float] = defaultdict(float)
    for drink in config["drinks"]:
        total_servings = (
            round(people * drink["interest_percentage"]) * drink["servings"]
        )
        for item in drink.get(key, []):
            totals[item["name"]] += total_servings * item["amount_ml"]
    return dict(totals)


def print_shopping_list(
    section_title: str,
    people: int,
    totals: dict[str, float],
    bottle_size_ml: int = 500,
    fruit_yields: dict[str, tuple[str, str, float]] | None = None,
) -> None:
    if not totals:
        return
    if fruit_yields is None:
        fruit_yields = {}

    print(f"\n{section_title} — Shopping List for {people} people:")
    print("─" * 56)

    col_w = max(len(n) for n in totals) + 2

    for name, ml in sorted(totals.items()):
        if name in fruit_yields:
            singular, plural, ml_per_fruit = fruit_yields[name]
            count = math.ceil(ml / ml_per_fruit)
            quantity_label = f"{count} {singular if count == 1 else plural}"
        else:
            bottles = math.ceil(ml / bottle_size_ml)
            quantity_label = f"{bottles} bottle{'s' if bottles != 1 else ''}"
        print(
            f"  {name:<{col_w}}: {ml:>7,.0f} mL  ({ml / 1000:.2f} L)   {quantity_label}"
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

    fruit_yields: dict[str, tuple[str, str, float]] = {}
    if ml := config.get("expected_juice_content_per_lime_ml"):
        fruit_yields["Lime Juice"] = ("lime", "limes", ml)
    if ml := config.get("expected_juice_content_per_lemon_ml"):
        fruit_yields["Lemon Juice"] = ("lemon", "lemons", ml)

    mixer_totals = _sum_ingredients(config, "mixers")
    liquor_totals = _sum_ingredients(config, "liquors")

    print_shopping_list(
        "Mixers",
        config["people"],
        mixer_totals,
        config.get("mixer_bottle_size_ml", 500),
        fruit_yields,
    )
    print_shopping_list(
        "Liquors",
        config["people"],
        liquor_totals,
        config.get("liquor_bottle_size_ml", 700),
    )


if __name__ == "__main__":
    main()
