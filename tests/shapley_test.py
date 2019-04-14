import pandas
import pytest
from modules.shapley import Shapley


def test_calculate_expected_shapley_values_dataframe():
    """
    Test using a dataframe for the input dataset
    """
    dataset = pandas.read_csv('./test_datasets/simple.csv', sep=',')

    s = Shapley(
        coalition_values=dataset.set_index(
            "channels").to_dict()["conversions"]
    )
    assert s.run() == {
        'SEM': 5.0,
        'Organic': 5.0
    }


def test_calculate_expected_shapley_values_dict():
    """
    Test using a dictionary for the input dataset
    """

    dataset = {
        'SEM': 1,
        'Organic': 1,
        'Organic,SEM': 8
    }
    s = Shapley(coalition_values=dataset)
    assert s.run() == {
        'SEM': 5.0,
        'Organic': 5.0
    }


def test_calculate_one_participant_result():
    """
    Test using a a dataset with one participant
    """

    dataset = {
        'SEM': 1
    }
    s = Shapley(coalition_values=dataset)
    assert s.run() == {
        'SEM': 1.0
    }


def test_calculate_two_participants_result():
    """
    Test using a dataset with two participants
    """

    dataset = {
        'SEM': 1,
        'SEO': 1
    }
    s = Shapley(coalition_values=dataset)
    assert s.run() == {
        'SEM': 1.0,
        'SEO': 1.0
    }


def test_calculate_one_participant_and_foreign_coalition_result():
    """
    Test using a dataset with one participant and a participant found in
    the coalition only
    """

    dataset = {
        'SEM': 1,
        'SEM,SEO': 1
    }
    s = Shapley(coalition_values=dataset)
    assert s.run() == {
        'SEM': 1.5,
        'SEO': 0.5
    }


def test_calculate_expected_shapley_values_unordered_participants_in_coalitions():
    """
    Test using a not ascending alphabetical ordered participant coalition
    """

    unordered_participants_dataset = {
        'SEM': 1,
        'Organic': 1,
        'SEM,Organic': 8  # Wrong order

    }
    s = Shapley(coalition_values=unordered_participants_dataset)
    assert s.run() == {
        'SEM': 5.0,
        'Organic': 5.0
    }


def test_calculate_expected_shapley_values_spaces_in_coalitions():
    """
    Test using a coalition containing spaces
    """

    spaces_in_participants_dataset = {
        'SEM': 1,
        'Organic': 1,
        'Organic, SEM': 8  # Unwanted space
    }
    s = Shapley(coalition_values=spaces_in_participants_dataset)
    assert s.run() == {
        'SEM': 5.0,
        'Organic': 5.0
    }


def test_raise_alert_when_duplicate_participants_in_one_coalition():
    """
    Test an error is raised when a duplicate particant is found in a coalition
    """
    double_participant_in_dataset = {
        'SEM': 1,
        'Organic': 1,
        'SEM,SEM': 8
    }

    with pytest.raises(ValueError):
        Shapley(coalition_values=double_participant_in_dataset)


# Todo: Test non-numerical values
# Todo: Add case insenstive participant mapping
