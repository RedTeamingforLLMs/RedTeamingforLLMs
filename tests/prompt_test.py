from .env import generate_arithmetic_question, generate_puzzle_question
from .env import CodeContext
from .env import ExplainContext
from .env import ImpersonationContext
from .env import RestoryingContext


def run_prompt_tests(verbose=False):
    qf_arithmetic_code = generate_arithmetic_question(context_class=CodeContext())
    qf_arithmetic_explain = generate_arithmetic_question(context_class=ExplainContext())
    qf_arithmetic_impersonation = generate_arithmetic_question(context_class=ImpersonationContext())
    qf_arithmetic_restorying = generate_arithmetic_question(context_class=RestoryingContext())
    if verbose:
        print(f"Arithmetic code context:\n {qf_arithmetic_code()}\n")
        print(f"Arithmetic explain context:\n {qf_arithmetic_explain()}\n")
        print(f"Arithmetic impersonation context:\n {qf_arithmetic_impersonation()}\n")
        print(f"Arithmetic restorying context:\n {qf_arithmetic_restorying()}\n")

    qf_puzzle_code = generate_puzzle_question(context_class=CodeContext())
    qf_puzzle_explain = generate_puzzle_question(context_class=ExplainContext())
    qf_puzzle_impersonation = generate_puzzle_question(context_class=ImpersonationContext())
    qf_puzzle_restorying = generate_puzzle_question(context_class=RestoryingContext())
    if verbose:
        print(f"Puzzle code context:\n {qf_puzzle_code()}\n")
        print(f"Puzzle explain context:\n {qf_puzzle_explain()}\n")
        print(f"Puzzle impersonation context:\n {qf_puzzle_impersonation()}\n")
        print(f"Puzzle restorying context:\n {qf_puzzle_restorying()}\n")
