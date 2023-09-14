from typing import List

from contexts.context import Context
from experiments.experiment import Experiment
from utils.question_generation import generate_arithmetic_question

LOW_RANGE = [0, 100]
HIGH_RANGE = [1000, 10000]


class ArithmeticExperiment(Experiment):
    def __init__(self, contexts: List[List[Context]], num_questions: List[int], num_range: List[int] = LOW_RANGE):
        super().__init__(contexts, num_questions)
        self.num_range = num_range

    def get_questions(self):
        questions = []
        for context in self.contexts:
            questions.append(generate_arithmetic_question(context, self.num_range[0], self.num_range[1]))

        return questions

    def get_filenames(self):
        filename = []
        for context in self.contexts:
            filename.append(context.get_context_name())

        return filename
