import os

from unittest.mock import MagicMock

from .env import Pipeline
from .env import extract_answer
from .env import generate_arithmetic_question


def get_config_filepath():
    return os.path.join(os.path.dirname(__file__), 'test_config.json')


def test_arguments():
    test_question = "What is the product of 7 and 6?"

    def question_function():
        return 42, test_question, test_question

    pipeline = Pipeline(question_function, 1, config_filename=get_config_filepath())

    mock_response = {'choices': [{'message': {'content': "The answer is [FINAL ANSWER] 44"}}]}
    pipeline.api_function = MagicMock(return_value=mock_response)

    evals = pipeline.run_pipeline()
    eval_metrics = evals[0]['no_context']["metrics"]
    assert eval_metrics['ground_truth'] == '42'
    assert eval_metrics['prediction'] == '44'
    assert eval_metrics['abs_edit_distance'] == 1
    assert eval_metrics['rel_edit_distance'] == 0.5
    assert eval_metrics['abs_distance'] == 2
    assert eval_metrics['rel_distance'] == 2 / 42

    message = [{'role': 'user', 'content': test_question}]
    pipeline.api_function.assert_called_with(model="gpt-3.5-turbo",
                                             messages=message,
                                             max_tokens=500,
                                             top_p=0.2)


def test_metrics_and_parsing():
    test_question = "What is the product of 7 and 6?"

    def question_function():
        return 42, test_question, test_question

    pipeline = Pipeline(question_function, 1, config_filename=get_config_filepath())

    mock_response = {'choices': [{'message': {'content': "[FINAL ANSWER] The answer is -40"}}]}
    pipeline.api_function = MagicMock(return_value=mock_response)

    evals = pipeline.run_pipeline()
    eval_metrics = evals[0]['no_context']["metrics"]
    assert eval_metrics['ground_truth'] == '42'
    assert eval_metrics['prediction'] == '-40'
    assert eval_metrics['abs_edit_distance'] == 2
    assert eval_metrics['rel_edit_distance'] == 1
    assert eval_metrics['abs_distance'] == 82
    assert eval_metrics['rel_distance'] == 82 / 42


# Needs a valid api key in config.json to pass
def test_api(api_key):
    test_question = "What is the product of 7 and 6?"
    question_function = generate_arithmetic_question()
    pipeline = Pipeline(question_function, 1, api_key=api_key)

    message = [{'role': 'user', 'content': test_question}]
    pipeline.api_function(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=500,
        top_p=0.2
    )


def test_extract_answer():
    prompt = "What is the product of 7 and 6?"
    response1 = "The product of 7 and 6 is 42"
    response2 = "[FINAL ANSWER] The product of 7 and 6 is 42 "
    response3 = "[FINAL ANSWER] The product of 7 and 6 is 42."
    response4 = "[FINAL ANSWER] The product of 7 and 6 is 42.0."
    response5 = "[FINAL ANSWER] The product of 7 and 6 is -42?"
    response6 = "[FINAL ANSWER] The product of 7 and 6 is forty-two"
    response7 = "[FINAL ANSWER] The product of 7 and 6 is .42!"

    assert extract_answer(prompt=prompt, response=response1) == "42"
    assert extract_answer(prompt=prompt, response=response2) == "42"
    assert extract_answer(prompt=prompt, response=response3) == "42"
    assert extract_answer(prompt=prompt, response=response4) == "42"
    assert extract_answer(prompt=prompt, response=response5) == "-42"
    assert extract_answer(prompt=prompt, response=response6) is None
    assert extract_answer(prompt=prompt, response=response7) == "0.42"


def run_pipeline_tests(api_tests=False, api_key=None):
    test_arguments()
    test_metrics_and_parsing()
    test_extract_answer()
    if api_tests:
        test_api(api_key)
