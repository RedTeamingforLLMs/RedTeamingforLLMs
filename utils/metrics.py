# Generating the edit distance between two strings
import json
from typing import List

import numpy as np


def levenshtein(a: str, b: str):
    # We want a to be the (potentially) longer string
    if len(a) > len(b):
        a, b = b, a

    distances = range(len(a) + 1)
    for b_index, b_element in enumerate(b):
        min_distances = [b_index + 1]

        for a_index, a_element in enumerate(a):
            if a_element == b_element:
                min_distances.append(distances[a_index])
            else:
                min_distances.append(
                    1 + min(distances[a_index], distances[a_index + 1], min_distances[-1]))

        distances = min_distances
    return distances[0 - 1]


# Generates an object containing the ground truth, extracted prediction
# and the accuracy metrics
def evaluate_answer(ground_truth: str, prediction: str, prompt: str, response: str):
    result_dict = {
        "prompt": prompt,
        "response": response
    }

    if prediction:
        edit_distance = levenshtein(ground_truth, prediction)
        distance = abs(float(ground_truth) - float(prediction))

        result_dict.update({"metrics": {
            "ground_truth": ground_truth,
            "prediction": prediction,
            "abs_edit_distance": edit_distance,
            "rel_edit_distance": edit_distance / len(ground_truth),
            "abs_distance": distance,
            "rel_distance": distance / int(ground_truth)
        }})

    return result_dict


def evaluate_experiments(eval_filenames: List[str]):
    # Calculating average metrics per run
    names = []
    contexts_means = []
    no_contexts_means = []
    extraction_rates = []

    for name in eval_filenames:
        filename = f'{name}.json'

        with open(filename, 'r') as f:
            # Reading from respective files
            data = json.loads(f.read())

        context = []
        no_context = []

        metrics = ['abs_edit_distance', 'rel_edit_distance',
                   'abs_distance', 'rel_distance', 'accuracy']

        successful_extractions = 0
        prompts = 0

        # Each row is a single experiment run
        for row in data:
            for string, array in zip(['context', 'no_context'], [context, no_context]):
                results_row = []

                prompts += 1

                if 'metrics' in row[string]:
                    successful_extractions += 1

                    for metric in metrics[:4]:
                        results_row.append(row[string]['metrics'][metric])

                    # If the result matches ground truth increase the accuracy
                    if row[string]['metrics']['abs_distance'] == 0:
                        results_row.append(1)
                    else:
                        results_row.append(0)

                    array.append(results_row)

        mean_context = [np.mean(context, axis=0), np.std(context, axis=0)]
        mean_no_context = [np.mean(no_context, axis=0),
                           np.std(no_context, axis=0)]

        names.append(f'{name}')
        contexts_means.append(mean_context)
        no_contexts_means.append(mean_no_context)
        extraction_rates.append(successful_extractions / prompts if prompts > 0 else 0)

    results = []

    for name, context_result, no_context_result, extraction_rate in zip(names, contexts_means, no_contexts_means, extraction_rates):
        results.append({
            "name": name,
            "no_context": format_metric_results(metrics, no_context_result),
            "context": format_metric_results(metrics, context_result),
            "extraction_rate": extraction_rate
        })

    return results


def format_metric_results(metrics, results):
    return {k: {"mean": mean, "std": std} for k, mean, std in zip(metrics, results[0], results[1])}
