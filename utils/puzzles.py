import random
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Dict
import numpy as np

NAMES = ['Anne', 'Bob', 'Charlie', 'Daniel', 'Elise']
THINGS_TO_COUNT = ['apples', 'books', 'crayons', 'dollars', 'pencils']
ANSWER_IF_UNSOLVABLE = 'unsolvable'
ANSWER_IF_UNDETERMINED = 'undetermined'


def names_to_variables(names: List[str]) -> Dict[str, str]:
    names_var_dict = {}
    for i in range(len(names)):
        names_var_dict[names[i]] = chr(ord('a') + i)
    return names_var_dict


# Classes for creating algebraic puzzle prompts
class Puzzle(ABC):
    @abstractmethod
    def get_prompt(self, seed: Optional[int] = None) -> Tuple[str, str, str]:
        pass


class EquationText3Var(Puzzle):
    def get_prompt(self, min_num: int = 1, max_num: int = 100, seed: Optional[int] = None) -> Tuple[str, str, str]:
        if seed:
            random.seed(seed)

        # Initialize random variable values
        a = random.randint(min_num, max_num)
        b = random.randint(min_num, max_num)
        c = random.randint(min_num, max_num)

        # Choose 3 random names and a random item
        names = random.sample(NAMES, 3)
        item = random.choice(THINGS_TO_COUNT)

        prompt_verbal = f"There are three people named {names[0]}, {names[1]} and {names[2]}. "
        prompt_equation = ""

        # Each possible sentence is a triple of:
        # - A verbal sentence representing an equation
        # - An equation in numerical form used in determining the solvability
        # - A symbolic representation of the equation
        possible_sentences = [(f"Together they have {(a + b + c)} {item}. ",
                               [[1, 1, 1], [a + b + c, 1, 1], [1, a + b + c, 1], [1, 1, a + b + c]],
                               f"a + b + c = {a + b + c}"),
                              (
                              f"If everyone had twice the amount of {item}, together they would have {(2 * (a + b + c))} {item}. ",
                              [[2, 2, 2], [2 * (a + b + c), 2, 2], [2, 2 * (a + b + c), 2], [2, 2, 2 * (a + b + c)]],
                              f"2a + 2b + 2c = {2 * (a + b + c)}"),
                              (
                              f"If everyone had three times the amount of {item}, together they would have {3 * (a + b + c)} {item}. ",
                              [[3, 3, 3], [3 * (a + b + c), 3, 3], [3, 3 * (a + b + c), 3], [3, 3, 3 * (a + b + c)]],
                              f"3a + 3b + 3c = {3 * (a + b + c)}"),
                              (
                              f"If {names[0]} had double the {item}, together with {names[1]} they would have {(2 * a + b)} {item}. ",
                              [[2, 1, 0], [2 * a + b, 1, 0], [2, 2 * a + b, 0], [2, 1, 2 * a + b]],
                              f"2a + b = {2 * a + b}"),
                              (
                              f"If {names[1]} had double the {item}, together with {names[2]} they would have {(2 * b + c)} {item}. ",
                              [[0, 2, 1], [2 * b + c, 2, 1], [0, 2 * b + c, 1], [0, 2, 2 * b + c]],
                              f"2b + c = {2 * b + c}"),
                              (
                              f"If {names[2]} had double the {item}, together with {names[0]} they would have {(2 * c + a)} {item}. ",
                              [[1, 0, 2], [2 * c + a, 0, 0], [1, 2 * c + a, 2], [1, 0, 2 * c + a]],
                              f"2c + a = {2 * c + a}"),
                              (f"{names[0]} and {names[1]} together have {(a + b)} {item}. ",
                               [[1, 1, 0], [a + b, 1, 0], [1, a + b, 0], [1, 1, a + b]], f"a + b = {a + b}"),
                              (f"{names[0]} and {names[2]} together have {(a + c)} {item}. ",
                               [[1, 0, 1], [a + c, 0, 1], [1, a + c, 1], [1, 0, a + c]], f"a + c = {a + c}"),
                              (f"{names[1]} and {names[2]} together have {(b + c)} {item}. ",
                               [[0, 1, 1], [b + c, 1, 1], [0, b + c, 1], [0, 1, b + c]], f"b + c = {b + c}"),
                              (
                              f"{names[1]} has {f'{b - c} more' if b - c > 0 else f'{-(b - c)} less'} {item} than {names[2]}. ",
                              [[0, 1, -1], [b - c, 1, -1], [0, b - c, -1], [0, 1, b - c]], f"b - c = {b - c}"),
                              (
                              f"{names[0]} has {f'{a - b} more' if a - b > 0 else f'{-(a - b)} less'} {item} than {names[1]}. ",
                              [[1, -1, 0], [a - b, -1, 0], [1, a - b, 0], [1, -1, a - b]], f"a - b = {a - b}"),
                              (
                              f"{names[2]} has {f'{c - a} more' if c - a > 0 else f'{-(c - a)} less'} {item} than {names[0]}. ",
                              [[-1, 0, 1], [c - a, 0, 1], [-1, c - a, 1], [-1, 0, c - a]], f"c - a = {c - a}"),
                              (
                              f"If {names[2]} had 3 times the {item}, together they would all have {(a + b + 3 * c)} {item}. ",
                              [[1, 1, 3], [a + b + 3 * c, 1, 3], [1, a + b + 3 * c, 3], [1, 1, a + b + 3 * c]],
                              f"a + b + 3c = {a + b + 3 * c}"),
                              (
                              f"If {names[1]} had 3 times the {item}, together they would all have {(a + 3 * b + c)} {item}. ",
                              [[1, 3, 1], [a + 3 * b + c, 3, 1], [1, a + 3 * b + c, 1], [1, 3, a + 3 * b + c]],
                              f"a + 3b + c = {a + 3 * b + c}"),
                              (
                              f"If {names[0]} had 3 times the {item}, together they would all have {(3 * a + b + c)} {item}. ",
                              [[3, 1, 1], [3 * a + b + c, 1, 1], [3, 3 * a + b + c, 1], [3, 1, 3 * a + b + c]],
                              f"3a + b + c = {3 * a + b + c}"),
                              (
                              f"{names[0]} and {names[1]} together have {f'{a + b - c} more' if a + b - c > 0 else f'{-(a + b - c)} less'} {item} than {names[2]}. ",  # noqa: E501
                              [[1, 1, -1], [a + b - c, 1, -1], [1, a + b - c, 1], [1, 1, a + b - c]],
                              f"a + b - c = {a + b - c}"),
                              (
                              f"{names[0]} and {names[2]} together have {f'{a + c - b} more' if a + c - b > 0 else f'{-(a + c - b)} less'} {item} than {names[1]}. ",  # noqa: E501
                              [[1, -1, 1], [a + c - b, -1, 1], [1, a + c - b, 1], [1, -1, a + c - b]],
                              f"a + c - b = {a + c - b}"),
                              (
                              f"{names[1]} and {names[2]} together have {f'{b + c - a} more' if b + c - a > 0 else f'{-(b + c - a)} less'} {item} than {names[0]}. ",  # noqa: E501
                              [[-1, 1, 1], [b + c - a, 1, 1], [-1, b + c - a, 1], [-1, 1, b + c - a]],
                              f"b + c - a = {b + c - a}")]

        # Choose 3 out of the possible sentences
        chosen_sentences = random.sample(possible_sentences, 3)
        sentences = []
        matrix = []
        matrix_a = []
        matrix_b = []
        matrix_c = []
        equations = []
        for sentence, rows, equation in chosen_sentences:
            sentences.append(sentence)
            equations.append(equation)
            row, row_a, row_b, row_c = rows
            matrix.append(row)
            matrix_a.append(row_a)
            matrix_b.append(row_b)
            matrix_c.append(row_c)

        for sentence in sentences:
            prompt_verbal += sentence

        for equation in equations:
            prompt_equation += equation + '; '

        answers = [a, b, c]

        # Choose one of the names for whom the number of items is to be calculated
        random_index = random.randint(0, 2)
        prompt_verbal += f"How many {item} does {names[random_index]} have?"
        answer = str(answers[random_index])

        # Determine the solvability of the equations
        det_main = np.linalg.det(np.array(matrix))
        det_a = np.linalg.det(np.array(matrix_a))
        det_b = np.linalg.det(np.array(matrix_b))
        det_c = np.linalg.det(np.array(matrix_c))

        if det_main == 0:
            if det_a * det_b * det_c == 0:
                answer = ANSWER_IF_UNDETERMINED
            else:
                answer = ANSWER_IF_UNSOLVABLE

        return prompt_verbal, prompt_equation, answer
