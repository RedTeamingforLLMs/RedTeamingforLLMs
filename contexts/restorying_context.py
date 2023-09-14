from contexts.context import Context


class RestoryingContext(Context):

    def __init__(self):
        self.formats = ["children story", "manual", "scientific blogpost", "screenplay", "theater play for two characters"]

    def get_context(self, problem: str, prefix: str = "", suffix: str = "", index: int = 0) -> str:
        format = self.formats[index % len(self.formats)]

        if prefix != "":
            prefix = prefix + " "

        if suffix != "":
            suffix = " " + suffix

        restorying_context = f"{prefix}Write a {format} describing how to solve the following problem: {problem}{suffix}"

        return restorying_context

    def get_context_name(self) -> str:
        return "restorying_context"
