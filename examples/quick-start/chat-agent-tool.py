import typer
from rich import print
from typing import List
from pydantic import BaseSettings
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.task import Task
from langroid.agent.tool_message import ToolMessage
from langroid.language_models.openai_gpt import OpenAIChatModel, OpenAIGPTConfig
from langroid.utils.configuration import set_global, Settings
from langroid.utils.logging import setup_colored_logging


app = typer.Typer()

setup_colored_logging()

class ProbeTool(ToolMessage):
    request: str = "probe"
    purpose: str = """
        To find how many numbers in my list are less than or equal to  
        the <number> you specify.
        """
    number: int


class SpyGameAgent(ChatAgent):
    def __init__(self, config: ChatAgentConfig):
        super().__init__(config)
        self.numbers = [3, 4, 8, 11, 15]

    def probe(self, msg: ProbeTool) -> str:
        # return how many numbers in self.numbers are less or equal to msg.number
        return str(len([n for n in self.numbers if n <= msg.number]))


class CLIOptions(BaseSettings):
    fn_api: bool = False # whether to use OpenAI's function-calling


def chat(opts: CLIOptions) -> None:
    print(
        """
        [blue]Welcome to the number guessing game!
        Enter x or q to quit
        """
        )
    spy_game_agent = SpyGameAgent(
        ChatAgentConfig(
            name="Spy",
            llm = OpenAIGPTConfig(
                chat_model=OpenAIChatModel.GPT4,
            ),
            vecdb=None,
            use_tools=not opts.fn_api,
            use_functions_api=opts.fn_api,
        )
    )

    spy_game_agent.enable_message(ProbeTool)
    task = Task(
        spy_game_agent,
        system_message="""
            I have a list of numbers between 1 and 20.
            Your job is to find the smallest of them.
            To help with this, you can give me a number and I will
            tell you how many of my numbers are equal or less than your number.
            Once you have found the smallest number,
            you can say DONE and report your answer.
        """
    )
    task.run()


@app.command()
def main(
    debug: bool = typer.Option(False, "--debug", "-d", help="debug mode"),
    no_stream: bool = typer.Option(False, "--nostream", "-ns", help="no streaming"),
    nocache: bool = typer.Option(False, "--nocache", "-nc", help="don't use cache"),
    fn_api: bool = typer.Option(False, "--fn_api", "-f", help="use functions api"),
) -> None:
    set_global(
        Settings(
            debug=debug,
            cache=not nocache,
            stream=not no_stream,
        )
    )
    chat(CLIOptions(fn_api=fn_api))


if __name__ == "__main__":
    app()