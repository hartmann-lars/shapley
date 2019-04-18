# Shapley Values For Attribution Modelling
Inspired by: https://medium.com/data-from-the-trenches/marketing-attribution-e7fa7ae9e919

By Lars Hartmann, 2019

## Requirements
- Python3.7+
- Pandas

## Usage
### Quick example
The `main.py` contains an example for calculating the Shapley Values of a simple dataset.
```
from modules import shapley

s = shapley.Shapley(coalition_values=your-dataset)

shapley_values = s.run()

Output example:
---
SEM accounts for 5.0 conversions
Organic accounts for 5.0 conversions
--
```
Run this script with `python3 main.py`

### Generate a dataset
Use this tool for easy generating datasets to use for testing or experiments.
Edit `PARTICIPANTS` and run the script: `python3 performance_test.py`

## Test
### Unit Tests
Run all unit tests with `pytest` in the root folder.

### Performance Tests
Run the performance tests with `python3 performance_test.py`