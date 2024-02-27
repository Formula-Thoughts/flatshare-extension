from formula_thoughts_web.abstractions import ApplicationContext


class SetGroupRequestContextCommand:

    def run(self, context: ApplicationContext) -> None:
        ...