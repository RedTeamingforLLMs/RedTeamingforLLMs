from contexts.context import Context


class ExplainContext(Context):

    def get_context(self, problem: str, prefix: str = "", suffix: str = "", index: int = 0) -> str:
        if prefix != "":
            prefix = prefix + " "

        if suffix != "":
            suffix = " " + suffix

        explain_context = (f"{prefix}Explain how you understand the following problem: " +
                           f"{problem} Then provide an answer to this problem.{suffix}")

        return explain_context

    def get_context_name(self) -> str:
        return "explain_context"
