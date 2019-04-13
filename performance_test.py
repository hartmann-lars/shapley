"""
Performance testing of the Shapley module based on processing times


"""

from modules import shapley
from pprint import pprint
from pandas import pandas
from time import time

DATASET_SIMPLE = pandas.read_csv('./test_datasets/simple.csv', sep=',')
DATASET_MEDIUM = pandas.read_csv('./test_datasets/medium.csv', sep=',')

ITERATIONS = 1000
TIMING_PRECISION = 3


def run_sequences(dataset, sequence_identifier):
    """
    Run a sequence of executions and capture the average processing time

    Arguments:
        dataset {dict} -- [The target dataset]
        sequence_identifier {string} -- [Any name]

    Returns:
        [float] -- [the average processing time]
    """

    test_times = []
    for i in range(0, ITERATIONS):
        T_START = time()
        s = shapley.Shapley(
            coalition_values=dataset.set_index(
                "channels").to_dict()["conversions"]
        )
        s.run()
        test_times.append((time()-T_START))

    average_processing_time = round(
        _avg_time(test_times)*1000, TIMING_PRECISION
    )

    print(
        f"{sequence_identifier}, average processing time [n={ITERATIONS}]: {average_processing_time} ms"
    )

    return average_processing_time


def _avg_time(test_times):
    """
    Capture the average time from a set of times

    Arguments:
        test_times {list} -- [A list of times recorded]

    Returns:
        [float] -- [The average time]
    """

    _sum = 0
    for t in test_times:
        _sum += t
    return _sum / len(test_times)


if __name__ == "__main__":

    average_time_simple = run_sequences(DATASET_SIMPLE, 'Simple Dataset')

    average_time_medium = run_sequences(DATASET_MEDIUM, 'Medium Dataset')
