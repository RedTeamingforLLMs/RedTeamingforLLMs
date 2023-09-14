from contexts.context import Context


class DefaultContext(Context):

    def get_context(self, problem: str, prefix: str = "", suffix: str = "", index: int = 0) -> str:
        if prefix != "":
            prefix = str(prefix) + " "

        if suffix != "":
            suffix = " " + suffix

        default_context = f"""{prefix}{problem}{suffix}"""

        return default_context

    def get_context_name(self) -> str:
        return "default_context"
