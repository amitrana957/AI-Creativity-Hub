from langchain_core.runnables import RunnableLambda


class DebugRunnable(RunnableLambda):
    """
    A Runnable that prints both input and output for debugging purposes.
    Can be inserted anywhere in a Runnable chain.
    """

    # Some ANSI colors
    COLORS = [
        "\033[31m",  # Red
        "\033[32m",  # Green
        "\033[33m",  # Yellow
        "\033[34m",  # Blue
        "\033[35m",  # Magenta
        "\033[36m",  # Cyan
    ]
    _counter = 0

    def __init__(self, name=None, color=None):
        # Auto-assign colors in round-robin if not specified
        if color is None:
            color = DebugRunnable.COLORS[
                DebugRunnable._counter % len(DebugRunnable.COLORS)
            ]
            DebugRunnable._counter += 1

        self.name = name or "DebugRunnable"
        self.color = color
        super().__init__(self._debug)

    def _debug(self, x):
        reset = "\033[0m"
        print(f"{self.color}[DEBUG] {self.name} INPUT:{reset} {repr(x)}")
        # Pass value through
        result = x
        print(f"{self.color}[DEBUG] {self.name} OUTPUT:{reset} {repr(result)}\n")
        return result
