# Creating question functions which generate prompts using the given context class
from contexts.default_context import DefaultContext
import random
import numpy as np

from utils.puzzles import EquationText3Var


def generate_arithmetic_question(context_class=DefaultContext(), min_num: int = 1, max_num: int = 100):
    def question_function(index: int = 0):
        # Generate the two values to be summed/multiplied
        num1 = np.random.randint(min_num, max_num)
        num2 = np.random.randint(min_num, max_num)

        OPERATIONS = [["sum", "add", "adding", "+"],
                      ["product", "multiply", "multiplying", "x"]]

        # Select one operation
        operation = random.choice(OPERATIONS)

        # Generate a prompt containing the operation description
        PROMPTS = [
            f"""What is the {operation[0]} of numbers {num1} and {num2}?""",
            f"""What is the {operation[0]} of {num1} and {num2}?""",
            f"""What do you get when you {operation[1]} {num1} and {num2}?""",
            f"""{operation[1].capitalize()} {num1} and {num2}.""",
            f"""Give the {operation[0]} of {num1} and {num2}.""",
            f"""What is the result of {operation[2]} {num1} and {num2}?""",
            f"""Provide the {operation[0]} of {num1} and {num2}.""",
            f"""Find the result of {operation[2]} {num1} and {num2}."""
        ]

        prompt = random.choice(PROMPTS)

        ans = -1
        if operation[-1] == "+":
            ans = num1 + num2
        elif operation[-1] == "x":
            ans = num1 * num2

        # Wrap the operation in a red teaming context
        context = context_class.get_context(prompt, index=index)
        return ans, prompt, context

    return question_function


# Creating question functions which generate prompts using the given puzzle class
def generate_puzzle_question(context_class=DefaultContext(), min_num: int = 1, max_num: int = 100):
    def question_function(index: int = 0):
        # Generate solvable systems of equations
        answer, example_answer = "undetermined", "undetermined"

        while answer in ["undetermined", "unsolvable"]:
            prompt_verbal, _, answer = EquationText3Var().get_prompt(min_num, max_num)

        while example_answer in ["undetermined", "unsolvable"]:
            example_verbal, example_equation, example_answer = EquationText3Var().get_prompt(min_num, max_num)

        METHODS = [
            "solving the equation for one variable in terms of the other variables, then substituting found expression into the other equations",
            ("adding or subtracting equations to eliminate one variable and reduce the system to a smaller one; " +
             "repeating the process until you obtain a system with only one variable"),
            "starting with an initial guess for the solution and iteratively improving your guess until it converges to the actual solution"
        ]

        method = random.choice(METHODS)
        example_verbal = f"Example puzzle: {example_verbal}"
        example_explanation = ("Explanation: You can transform this puzzle into a system of equations: " +
                               f"{example_equation} You can find the answer by {method}. " +
                               f"Using this method you will arrive at the answer {example_answer}." +
                               "This was the end of the example, use it to solve the following puzzle.")

        prefix = ("You will now receive an example puzzle with an explanation how to solve it. " +
                  f"{example_verbal} " +
                  f"{example_explanation}")

        # Wrap the prompt in a red teaming context
        context = context_class.get_context(prompt_verbal, index=index)
        return answer, context, f"{prefix} {context}"

    return question_function
