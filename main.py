from pprint import pprint
from pandas import pandas
from modules import shapley

DATASET_FOLDER = './test_datasets/'
DATASET_NAME = 'simple.csv'
CSV_SEPERATOR = ','

if __name__ == '__main__':
    dataset = pandas.read_csv(DATASET_FOLDER + DATASET_NAME, sep=CSV_SEPERATOR)

    s = shapley.Shapley(
        coalition_values=dataset.set_index(
            "channels").to_dict()["conversions"]
    )
shapley_values = s.run()

for participant, conversions in shapley_values.items():
    print(f"{participant} accounts for {conversions} conversions")
