# SAI

SAI is a command line tool that allows you to use ChatGPT API to ask questions about the files in your project.

## Installation

1. Clone this repository: `git clone https://github.com/<username>/summarize-ai.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Go to https://chat.openai.com/, create an account and start a new conversation
4. Copy the cookie and the 
3. Set your OpenAI API key as an environment variable: `export OPENAI_API_KEY=<your-api-key>`
4. Run the CLI: `python sai.py`



## Functionalities
- train: it reads the files in your project and train chat gpt to answer questions about them
- ask: it asks a question to chat gpt, and it returns an answer
- conversation: it starts a conversation with chat gpt
- list: returns the list of the chats
- delete: deletes a chat
- select-conversation: it let you select one of the conversation, and let you continue from where you left

## Examples of how to use it

First run:
```bash
poetry run python sai.py train "{path_to_your_project}"
```

Then you can start asking questions:
```bash
poetry run python sai.py ask "write a unit test for the python files in my project"
```
And yes. This README.md was generated using SAI.

```bash
poetry run python sai.py conversation "what is this project doing?"
```

## Contributing
Contributions to SAI are welcome! If you find a bug or have a suggestion for a new feature, please open an issue on this repository.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# sai
