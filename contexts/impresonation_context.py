from contexts.context import Context


class ImpersonationContext(Context):

    def __init__(self):
        self.mathematicians = ["Ada Lovelace", "Bernhard Riemann", "Carl Friedrich Gauss", "Isaac Newton", "Sophie Germain"]

    def get_context(self, problem: str, prefix: str = "", suffix: str = "", index: int = 0) -> str:
        mathematician = self.mathematicians[index % len(self.mathematicians)]

        if prefix != "":
            prefix = prefix + " "

        if suffix != "":
            suffix = " " + suffix

        impersonation_context = (f"{prefix}Imagine you are the mathematician {mathematician}. " +
                                 f"As {mathematician} answer the following problem: " +
                                 f"{problem}{suffix}")

        return impersonation_context

    def get_context_name(self) -> str:
        return "impersonation_context"
