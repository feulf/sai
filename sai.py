import click

from library.chatgpt import ChatGPT
from library.chatgpt import ONLY_ANSWER
from library.cli import IMPORTANT
from library.utils import train_project


@click.group()
def sai():
    """Sai is a command line tool to use ChatGPT to ask questions about your project"""


# todo: add ignore and parse wildcards option
@sai.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def train(path):
    """Read all the files in a folder and train ChatGPT on them via a prompt"""

    click.secho(
        "This command opens a new chat and train ChatGPT on the proejct you're listing."
    )
    input("Do you want to continue? (Press enter to continue)")

    chatgpt = ChatGPT()
    train_project(chatgpt, path)
    click.secho("Training done! Now you can ask questions about your project.")
    click.launch(chatgpt.chat_url.format(chatgpt.conversation_id))


@sai.command()
@click.argument("question", required=False)
def ask(question: str = None):
    """Ask any question about the project"""

    chatgpt = ChatGPT()
    chatgpt.verbosity = ONLY_ANSWER

    if question is None:
        click.secho("You can now start a conversation with ChatGPT.")
        click.secho("Write stop or exit to stop the conversation.", fg=IMPORTANT)
    else:
        chatgpt.ask(question)

    while True:
        prompt = input("You: ")
        if prompt in ["stop", "exit"]:
            break
        chatgpt.ask(prompt)


@sai.command()
def list():
    """List all the storage you have created"""
    chatgpt = ChatGPT()
    chatgpt.list_chats()


@sai.command()
@click.argument("conversation_ids", nargs=-1)
def delete(conversation_ids):
    """Delete a conversation"""
    chatgpt = ChatGPT()
    chatgpt.delete_chats(conversation_ids)


@sai.command()
@click.argument("conversation_id")
def select(conversation_id):
    """Delete a conversation"""
    chatgpt = ChatGPT()
    chatgpt.select_chat(chat_id=conversation_id)


@sai.command()
@click.argument("conversation_id", required=False)
def list_messages(conversation_id: str = None):
    """List all the storage you have created"""
    chatgpt = ChatGPT()
    chatgpt.messages_list(conversation_id)


if __name__ == "__main__":
    sai()
