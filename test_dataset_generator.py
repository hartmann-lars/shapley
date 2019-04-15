import csv
import random
import itertools
from math import factorial
from pprint import pprint


class TestDatasetGenerator():
    # General settings
    OUTPUT_FOLDER = './generated_datasets/'
    CSV_DELIMITER = ','
    CSV_QUOTE_CHAR = '"'

    # Content settings
    HEADER = ['channels', 'conversions']
    PARTICIPANTS = [
        'Display',
        'Referral',
        'Paid Social',
        'Unpaid Social',
        'Brand Marketing',
        'Email',
        'Other',
        'Youtube',
        'SEM',
        'SEO',
        'Direct',
    ]
    PARTICIPANT_CONVERSION_RANGE = (0, 100)
    PARTICIPANT_CONVERSION_STEP = 1.0
    # DATASET_ROWS = 10

    def __init__(self):
        pass

    def _generate_content(self):
        content = []

        for i in range(1, len(self.PARTICIPANTS)+1):
            coalitions = map(sorted, map(
                list, itertools.combinations(self.PARTICIPANTS, i))
            )
            for coalition in coalitions:
                conversion = random.randrange(
                    self.PARTICIPANT_CONVERSION_RANGE[0],
                    self.PARTICIPANT_CONVERSION_RANGE[1],
                    self.PARTICIPANT_CONVERSION_STEP
                )
                coalition_string = ",".join(sorted(coalition))
                content.append([coalition_string, conversion])

        return content

    def write_dataset(self, output_filename, output_folder=None):

        if output_folder is None:
            output_folder = self.OUTPUT_FOLDER

        with open(output_folder+output_filename, 'w', newline='') as file:
            writer = csv.writer(
                file,
                delimiter=self.CSV_DELIMITER,
                quotechar=self.CSV_QUOTE_CHAR,
                quoting=csv.QUOTE_MINIMAL
            )
            # Write header
            writer.writerow(self.HEADER)

            # Write generated content
            for row in self._generate_content():
                writer.writerow(row)


if __name__ == '__main__':
    t = TestDatasetGenerator()
    t.write_dataset(
        output_filename='generated_test_1.csv'
    )
