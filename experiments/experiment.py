import json
from typing import List

from contexts.context import Context
from utils.pipeline import Pipeline


class Experiment:
    def __init__(self, contexts: List[Context], num_questions: List[int]):
        self.contexts = contexts
        self.num_questions = num_questions

    def get_questions(self):
        raise NotImplementedError

    def get_filenames(self):
        raise NotImplementedError

    def run_experiment(self, config_filename: str = None) -> List[str]:
        question_functions = self.get_questions()
        context_names = self.get_filenames()
        # Storing filenames with the output
        eval_filenames = []
        # Running the prompt batches
        for question_function, name, num_questions in zip(question_functions, context_names, self.num_questions):
            if config_filename:
                pipeline = Pipeline(question_function, num_questions=num_questions, config_filename=config_filename)
            else:
                pipeline = Pipeline(question_function, num_questions=num_questions)
            res = pipeline.run_pipeline(suffix="Preface the final answer with [FINAL ANSWER]")
            with open(f"{name}.json", "w") as f:
                # Saving to respective files
                f.write(json.dumps(res, indent=4))
            eval_filenames.append(name)

        return eval_filenames
