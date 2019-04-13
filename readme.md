# Shapley Values For Attribution Modelling
Inspired by: https://medium.com/data-from-the-trenches/marketing-attribution-e7fa7ae9e919

Lars Hartmann, 2019

## Requirements
- Python3.7+
- Pandas

## Usage
Quick example: `python3 main.py`

```
from modules import shapley

s = shapley.Shapley( coalition_values=your-dataset)

shapley_values = s.run()

Output example:
---
SEM accounts for 5.0 conversions
Organic accounts for 5.0 conversions
--
```

## Test
Run `pytest` in the root folder