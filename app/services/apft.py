import bisect
import json
from dataclasses import dataclass

AGE_RANGES: dict = {
    '17-21': range(17, 21),
    '22-26': range(22, 26),
    '27-31': range(27, 31),
    '32-36': range(32, 36),
    '37-41': range(37, 41),
    '42-46': range(41, 46),
    '47-51': range(47, 51),
    '52-56': range(52, 56),
    '57-61': range(57, 61),
    '62+': range(62, 101),
}


@dataclass
class APFTCalculator:
    """A class that calculates the APFT (Army Physical Fitness Test).

    score based on gender, age, push-ups, sit-ups, and run time.
    """

    gender: str
    age: int
    pushups: int
    situps: int
    run: str

    def __post_init__(self) -> None:
        """Initializes the APFTCalculator object.

        Sets up dictionaries for male and female standards for push-ups, sit-ups, and run time.
        Converts the run time values to integers for comparison.
        Determines if the gender is male or female.
        Determines the age range based on the given age.
        """
        with open('app/services/apft_standards.json') as f:
            apft_standards = json.load(f)

            self.male_pu_dict = apft_standards['male']['push-ups']
            self.male_su_dict = apft_standards['male']['sit-ups']
            self.male_run_dict = apft_standards['male']['run']
            self.female_pu_dict = apft_standards['female']['push-ups']
            self.female_su_dict = apft_standards['female']['sit-ups']
            self.female_run_dict = apft_standards['female']['run']
            self.run_time_int_list = [int(runtime) for runtime in self.male_run_dict]

        self.is_male = self.gender == 'male'
        self.age_range = self.get_age_range()
        if isinstance(self.run, str):
            self.run = int(self.run.replace(':', ''))

    def get_age_range(self) -> str:
        """Determines the age range based on the given age.

        Args:
            age (int): The age of the individual.

        Returns:
            str: The age range of the individual.
        """
        for age_range, ages in AGE_RANGES.items():
            if self.age in ages:
                return age_range
        return None

    def get_score(self, score_dict: dict, score: int, min_score: int, max_score: int) -> int:
        """Calculates the score.

        based on the given score dictionary, score value, minimum score, and maximum score.

        Args:
            score_dict (dict): The dictionary containing the score ranges and corresponding scores.
            score (int): The score value.
            min_score (int): The minimum score for the given exercise.
            max_score (int): The maximum score for the given exercise.

        Returns:
            int: The calculated score.
        """
        if score < min_score:
            return 0
        if score > max_score:
            return 100
        return score_dict[str(score)].get(self.age_range, 50)

    def round_up_run(self) -> int:
        """Rounds up the run time to the nearest value in the run time list.

        Returns:
            int: The rounded up run time.
        """
        try:
            if self.run in self.run_time_int_list:
                return self.run
            round_up = bisect.bisect_right(self.run_time_int_list, self.run)
            return self.run_time_int_list[round_up]
        except IndexError:
            return 0

    def pu_score(self) -> int:
        """Calculates the push-up score.

        Returns:
            int: The push-up score.
        """
        score_dict = self.male_pu_dict if self.is_male else self.female_pu_dict
        return self.get_score(score_dict, self.pushups, 5, 77 if self.is_male else 50)

    def su_score(self) -> int:
        """Calculates the sit-up score.

        Returns:
            int: The sit-up score.
        """
        score_dict = self.male_su_dict if self.is_male else self.female_su_dict
        return self.get_score(score_dict, self.situps, 21, 82)

    def run_score(self) -> int:
        """Calculates the run score.

        Returns:
            int: The run score.
        """
        run = self.round_up_run()
        score_dict = self.male_run_dict if self.is_male else self.female_run_dict
        return self.get_score(score_dict, run, 1254, 2630)

    def calculate_score(self) -> tuple:
        """Calculates the total APFT score.

        Returns:
            tuple: A tuple containing the push-up score, sit-up score, run score, and total score.
        """
        pu_score_value = self.pu_score()
        su_score_value = self.su_score()
        run_score_value = self.run_score()
        return pu_score_value + su_score_value + run_score_value
