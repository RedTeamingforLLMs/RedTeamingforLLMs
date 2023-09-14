import json
import re
import time
from typing import List, Dict

import openai

from collections import Counter
from utils.metrics import evaluate_answer


class Pipeline:

    # Creates a pipeline object using a question function.
    # Upon being called, the question function should return
    # The expected answer, a prompt and a prompt using a context
    def __init__(self, question_function, num_questions: int, config_filename: str = "config.json", api_key: str = None):

        self.qf = question_function

        # Read config file
        with open(config_filename, "r") as f:
            config = json.load(f)

        self.model = config["model"]
        self.top_p = config["parameters"]["top_p"]
        self.max_tokens = config["parameters"]["max_tokens"]
        self.n_queries = num_questions

        self.api_function = openai.ChatCompletion.create

        if api_key is not None:
            openai.api_key = api_key
        else:
            openai.api_key = open(config["key_file"]).readline()

    # Runs the querying process for n iterations using the supplied question function
    def run_pipeline(self, prefix: str = "", suffix: str = ""):

        evals = []
        for i in range(self.n_queries):
            print(f"Query {i + 1}/{self.n_queries}")
            # The following naming convention might be confusing if the 'puzzle' experiment is run
            # In that case, the context prompt is the example prompt
            # while the regular prompt, already contains the question with context
            ans, regular_prompt, context_prompt = self.qf()
            complete_regular_prompt = ""
            complete_context_prompt = ""

            if prefix != "":
                complete_regular_prompt += prefix + " "
                complete_context_prompt += prefix + " "
            complete_regular_prompt += regular_prompt
            complete_context_prompt += context_prompt

            if suffix != "":
                complete_regular_prompt += " " + suffix
                complete_context_prompt += " " + suffix

            regular_response = self.query_gpt([complete_regular_prompt])
            context_response = self.query_gpt([complete_context_prompt])

            regular_answer = None
            context_answer = None

            try:
                regular_answer = extract_answer(regular_response, regular_prompt)
            except IndexError:
                print(f"Could not parse regular response: {regular_response}")
            try:
                context_answer = extract_answer(context_response, regular_prompt)
            except IndexError:
                print(f"Could not parse context response: {context_response}")

            evals.append({"no_context": evaluate_answer(str(ans), regular_answer, regular_prompt, regular_response),
                          "context": evaluate_answer(str(ans), context_answer, context_prompt, context_response)})

        return evals

    def query_gpt(self, prompt: List[str]):
        messages = form_message_dicts(prompt)

        response = None

        while not response:
            try:
                response = self.api_function(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p
                )
            except Exception as e:
                print('Retry')
                time.sleep(5)
                print(e)

        return response['choices'][0]['message']['content']

    def query_gpt_legacy(self, prompt: str):
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            max_tokens=500,
            top_p=0.2,
            stream=True,
        )

        completion_text = ''
        for event in response:
            event_text = event['choices'][0]['text']  # extract the text
            completion_text += event_text  # append the text

        return completion_text


def extract_answer(response: str, prompt: str, behavior: str = "max"):
    prompt_numbers = [float(num) for num in re.findall(r'(?: |^)([+-]?\d*\.?\d+)(?: |\D|$)', prompt)]
    # Consider the part of response after [FINAL ANSWER] marker and remove thousands separator (if exists)
    final_answer = response.split("[FINAL ANSWER]")[-1].replace(",", "")
    # Find all numbers in the answer (it may be in the form "The result of adding A and B is C")
    response_numbers = [float(num) for num in re.findall(r'(?: |^)([+-]?\d*\.?\d+)(?: |\D|$)', final_answer)]

    # Remove occurrences of numbers from the prompt since parts of the prompt may be repeated in the answer
    if len(response_numbers) > 1:
        counts = Counter(prompt_numbers)
        result = []
        for num in response_numbers:
            if counts[num]:
                counts[num] -= 1
            else:
                result.append(num)
    else:
        result = response_numbers

    # Cast integral numbers as int, otherwise keep floats
    result = [int(num) if (num).is_integer() else num for num in result]

    # Check if there is any result at all, otherwise return None to be solved in metric calculation
    if len(result) == 0:
        return None

    if behavior == "last":
        # Take (somewhat arbitrarily) the last element if required
        return str(result[-1])
    else:
        # We consider only additions and multiplications of positive numbers so take the maximum if multiple numbers (A, B, C) were found
        return str(max(result))


def form_message_dicts(prompts: List[str]) -> List[Dict]:
    return [{"role": "user", "content": prompt} for prompt in prompts]
