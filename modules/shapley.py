"""
Shapley v004
Calculate the Shapley values

Heavily inspired by: https://medium.com/data-from-the-trenches/marketing-attribution-e7fa7ae9e919

Refactored by Lars Hartmann

Returns:
    [dict] -- [A set of all inputs and their Shapley value]
"""
import itertools
from math import factorial
from collections import defaultdict
#  todo: make sure to get a list or dict and not a dataframe


class Shapley:
    participant_amount = None
    coalition_values = None

    def __init__(self, coalition_values):
        self.coalition_values = self.__sanitize_coalition_format(
            coalition_values
        )

    def run(self):
        shapley_values = defaultdict(int)

        participants = self.__extract_unique_participants(
            self.coalition_values.keys()
        )

        self.participant_amount = len(participants)

        # Get the contribution sum for each possible coalition
        v_values = self.__calculate_v_values(participants)

        for participant in participants:

            # for possible_coalition in v_values.keys():
            for possible_coalition, coalition_value in v_values.items():

                if participant not in possible_coalition.split(","):
                    possible_coalition_size = len(
                        possible_coalition.split(",")
                    )
                    possible_coalition_participants = possible_coalition.split(
                        ",")

                    possible_coalition_participants.append(participant)

                    possible_coalition_participants = ",".join(
                        sorted(possible_coalition_participants)
                    )
                    shapley_value = self.__calculate_shapley_value(
                        possible_coalition_v_value=v_values[possible_coalition_participants],
                        actual_coalition_v_value=coalition_value,
                        possible_coalition_size=possible_coalition_size
                    )
                    shapley_values[participant] += shapley_value
            # Add the term corresponding to the empty set
            shapley_values[participant] += v_values[participant] / \
                self.participant_amount

        return shapley_values

    def __calculate_v_values(self, participants):
        """
        Calculate the sum of all possible coalitions based on the participants

        Arguments:
            participants {dict or list} -- [A dict or list of the unique participants]

        Returns:
            [dict] -- [A dict containing each coalition's value sum]
        """

        v_values = {}

        for coalition in self.__subsets(participants):
            v_values[coalition] = self.__v_function(coalition)

        return v_values

    def __calculate_shapley_value(self, possible_coalition_v_value, actual_coalition_v_value, possible_coalition_size):
        return (possible_coalition_v_value - actual_coalition_v_value) *\
            (factorial(possible_coalition_size) *
             factorial(self.participant_amount - possible_coalition_size-1)/factorial(self.participant_amount))

    def __extract_unique_participants(self, coalitions):
        """
        Extracts unique participants from a set of coalitions

        Arguments:
            coalitions {[dict or list]} -- [The set of all coalitions]

        Returns:
            [dict] -- [a dictionary containing unique participants]
        """

        unique_participants = {}
        for coalition in coalitions:
            participants = coalition.split(",")
            for participant in participants:
                unique_participants[participant] = participant
        return unique_participants

    def __subsets(self, input_sets):
        """
        Generate all possible combinations of the input set as subsets

        Arguments:
            input_sets {dict or list} -- [A dict or list containing all input sets]

        Raises:
            ValueError -- [Unexcpeted input format]

        Returns:
            [dict or list] -- [A dict or list containing all possible __subsets]
        """

        # Only accept list or dict as input
        if not (isinstance(input_sets, dict) or isinstance(input_sets, list)):
            input_type = type(input_sets)
            raise ValueError(
                f'subsets expected a list or dict as input, but got "{input_type}"'
            )

        if len(input_sets) == 1:
            return input_sets
        else:
            sub_channels = []
            for i in range(1, len(input_sets)+1):
                # Map the touples to lists
                sub_channels.extend(
                    map(list, itertools.combinations(input_sets, i))
                )
        # return a string of sorted list items
        return map(",".join, map(sorted, sub_channels))

    def __v_function(self, coalition):
        """
        Sum the values of each subset in a coalition

        Arguments:
            coalition {string} -- [A comma seperated string containing all coalitions]

        Returns:
            [float] -- [The total sum of ]
        """

        __subsets_of_coalition = self.__subsets(coalition.split(","))

        worth_of_coalition = 0
        for subset in __subsets_of_coalition:
            if subset in self.coalition_values:
                worth_of_coalition += self.coalition_values[subset]
        return worth_of_coalition

    def __sanitize_coalition_format(self, coalition_values):
        """
        Make sure the order of participant is ascending
        in order to match the possible coalitions generated later
        Also remove trailing and ending whitespaces

        Arguments:
            coalition_values {dict} -- [The dataset with coalitions to sanitize]

        Returns:
            [dict] -- [The input dataset with sanitized participants]
        """

        ordered_participants_coalition_values = {}
        for coalition in coalition_values:
            participants = []
            items = coalition.split(',')

            # Ensure each coalition contains unique participants
            if not self.__list_items_are_unique(items):
                raise ValueError(
                    'Found coalitions with non-unique participants. Please review the input dataset.'
                )

            for item in items:
                participants.append(item.strip())

            ordered_string = ','.join(sorted(participants))

            ordered_participants_coalition_values[ordered_string] = coalition_values[coalition]

        return ordered_participants_coalition_values

    def __list_items_are_unique(self, list_items):
        """
        Check if the input items length matches the unique items found

        Arguments:
            list_items {list} -- [The input items]

        Returns:
            [bool] -- [Whether or not the list contained unique items]
        """

        if len(list_items) == 1:
            return True

        unique_items = {}

        for item in list_items:
            unique_items[item] = item

        return len(list_items) == len(unique_items)
