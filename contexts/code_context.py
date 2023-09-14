from contexts.context import Context


class CodeContext(Context):

    def __init__(self):
        self.languages = ["C++", "Java", "JavaScript", "Python", "Rust"]

    def get_context(self, problem: str, prefix: str = "", suffix: str = "", index: int = 0) -> str:
        language = self.languages[index % len(self.languages)]

        if prefix != "":
            prefix = prefix + " "

        if suffix != "":
            suffix = " " + suffix

        code_context = (f"{prefix}Write code in {language} to solve the following problem: " +
                        f"{problem} Then simulate the execution of this code to provide an answer to this problem.{suffix}")

        return code_context

    def get_context_name(self) -> str:
        return "code_context"
