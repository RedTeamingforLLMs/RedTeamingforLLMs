from typing import List

from contexts.context import Context
from experiments.experiment import Experiment
from utils.question_generation import generate_puzzle_question


class PuzzleExperiment(Experiment):
    def __init__(self, contexts: List[List[Context]], num_questions: List[int]):
        super().__init__(contexts, num_questions)

    def get_questions(self):
        questions = []
        for context in self.contexts:
            questions.append(generate_puzzle_question(context))

        return questions

    def get_filenames(self):
        filename = []
        for context in self.contexts:
            filename.append(context.get_context_name() + "_puzzle")

        return filename
