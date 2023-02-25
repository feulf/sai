from library.chatgpt import ChatGPT
from library.navigate import get_filepaths
from library.navigate import get_files_content

START_QUESTION = (
    "I'm going to paste the content of the files in my project and their filepaths. Wait for me to say UPLOAD_COMPLETED before you start answering. "  # noqa: E501
    "I'll ask you questions after that."
)


def prompt_from_filepath_and_content(contents: dict, question: str = None) -> str:
    if not question:
        question = START_QUESTION

    prompt = f"{question}\n\n"
    prompt += "\n\n".join(
        [
            f"# File: {filepath}\n\n{content}\n\n# end of file: {filepath}"
            for filepath, content in contents.items()
        ]
    )
    return prompt


def train_project(chatgpt: ChatGPT, path: str):
    filepaths = get_filepaths(path)
    contents = get_files_content(filepaths)

    chatgpt.ask(START_QUESTION)

    for filepath, content in contents.items():
        prompt = (
            "# File: " + filepath + "\n\n" + content + "\n\n# End of file: " + filepath
        )
        chatgpt.ask(prompt)

    return chatgpt.ask("UPLOAD_COMPLETED")


if __name__ == "__main__":
    chatgpt = ChatGPT()
    train_project(chatgpt, ".")
