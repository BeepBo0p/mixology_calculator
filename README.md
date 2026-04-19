# Mixology Calculator

Calculates how much mixer to buy for a party, given a drinks menu and expected guest interest.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

```bash
uv sync
```

## Usage

```bash
uv run mix
```

By default this reads `config.yaml` in the current directory. To use a different config:

```bash
uv run mix --config path/to/other.yaml
```

## Config format

```yaml
people: 50                              # number of guests
mixer_bottle_size_ml: 500              # assumed bottle size for bottled mixers
expected_juice_content_per_lime_ml: 30  # juice yield per lime
expected_juice_content_per_lemon_ml: 45 # juice yield per lemon

drinks:
  - name: Gin & Tonic
    interest_percentage: 0.40  # fraction of guests expected to drink this
    servings: 2                # drinks per interested guest
    mixers:
      - name: Tonic Water
        amount_ml: 150
```

Mixers named `Lime Juice` or `Lemon Juice` are counted as fruits rather than bottles in the output, using the yield values from the top-level config.

## Example output

```
Shopping List for 50 people:
────────────────────────────────────────────────────────
  Lemon Juice   :   3,240 mL  (3.24 L)   72 lemons
  Lime Juice    :     720 mL  (0.72 L)   24 limes
  Orange Juice  :   1,920 mL  (1.92 L)   4 bottles
  Soda Water    :   2,520 mL  (2.52 L)   6 bottles
  Tonic Water   :   6,000 mL  (6.00 L)   12 bottles
```
