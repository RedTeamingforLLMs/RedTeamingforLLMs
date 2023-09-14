import json
from contexts.code_context import CodeContext
from contexts.default_context import DefaultContext
from contexts.explain_context import ExplainContext
from contexts.impresonation_context import ImpersonationContext
from contexts.restorying_context import RestoryingContext
from experiments.puzzle_experiment import PuzzleExperiment
from experiments.arithmetic_experiment import ArithmeticExperiment
from utils.metrics import evaluate_experiments

from datetime import datetime
from enum import Enum
import argparse
import os


class Context(Enum):
    Code = CodeContext
    Default = DefaultContext
    Explain = ExplainContext
    Impersonation = ImpersonationContext
    Restorying = RestoryingContext


class Experiment(Enum):
    Arithmetic = ArithmeticExperiment
    Puzzle = PuzzleExperiment


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set up experiment parameters')
    parser.add_argument('--name', type=str, required=False, default=datetime.now().strftime('%Y%m%d%H%M%S'))
    parser.add_argument('--num_questions', nargs="*", required=False, default=[100])
    parser.add_argument('--contexts', nargs="*", required=False, default=["Default"])
    parser.add_argument('--experiment', type=str, required=False, default="Arithmetic")
    parser.add_argument('--range', type=int, nargs="*", required=False, default=[1, 100])

    args = parser.parse_args()
    contexts = [Context[t].value() for t in args.contexts]

    num_questions = [int(i) for i in args.num_questions]

    # If multiple contexts are provided but only one value for number of questions
    if len(contexts) > len(num_questions):
        num_questions = [num_questions[0]] * len(contexts)

    if args.experiment == "Arithmetic":
        experiment = Experiment[args.experiment].value(contexts, num_questions, args.range)
    else:
        experiment = Experiment[args.experiment].value(contexts, num_questions)

    # Create directory structure
    if not os.path.exists("results"):
        os.mkdir("results")
    os.chdir(os.path.expanduser("results"))
    dir = f"{args.name}"
    os.mkdir(dir)
    os.chdir(os.path.expanduser(dir))

    experiment.run_experiment("../../config.json")
    eval_filenames = experiment.get_filenames()
    results = evaluate_experiments(eval_filenames)
    print(results)

    with open('results.json', 'w') as file:
        file.write(json.dumps(results, indent=4))
