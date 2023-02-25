import json
import os
import uuid
from datetime import datetime

import click
import requests

from library.cli import BRIGHT_BLACK
from library.cli import CHATGPT
from library.cli import IMPORTANT
from library.cli import YOU

FULL_VERBOSITY = 3
ONLY_ANSWER = 2
ONLY_QUESTIONS = 1
NO_VERBOSITY = 0


class ChatGPT:
    url = "https://chat.openai.com/backend-api/conversation"
    chat_list_url = "https://chat.openai.com/backend-api/conversations"
    conversation_url = (
        "https://chat.openai.com/backend-api/conversation/{conversation_id}"
    )
    chat_url = "https://chat.openai.com/chat/{chat_id}"

    def __init__(
        self,
        chatgtp_token: str = None,
        chatgpt_cookie: str = None,
        conversation_id: str = None,
    ):
        chatgtp_token = chatgtp_token or os.getenv("OPENAI_BEARER_TOKEN")
        chatgpt_cookie = chatgpt_cookie or os.getenv("OPENAI_COOKIE")

        self.headers = self._set_headers(chatgtp_token, chatgpt_cookie)
        self.verbosity = FULL_VERBOSITY

        self.last_message_id = uuid.uuid4().hex
        self.conversation_id = conversation_id
        self._load_latest_chat_id()

    def ask(self, prompt: str):
        message_id = uuid.uuid4().hex
        parent_message_id = self.last_message_id
        conversation_id = self.conversation_id

        question_payload = {
            "action": "next",
            "messages": [
                {
                    "id": message_id,
                    "author": {"role": "user"},
                    "role": "user",
                    "content": {"content_type": "text", "parts": [prompt]},
                }
            ],
            "parent_message_id": parent_message_id,
            "model": "text-davinci-002-render-sha",
        }
        if conversation_id:
            question_payload["conversation_id"] = conversation_id

        self._you_speak(prompt)
        response = self._post(question_payload)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} {response.text}")

        if response.status_code in (401, 403):
            click.secho("You need to refresh your ChatGPT credentials.", fg=IMPORTANT)

        parsed_response = self._parse_response(response)

        answer = parsed_response["message"]["content"]["parts"][0]
        self.last_message_id = parsed_response["message"]["id"]
        self.conversation_id = parsed_response["conversation_id"]

        self._chatgpt_speaks(answer)
        return answer

    def list_chats(self):
        response = self._get_chat_list()
        click.secho("Here's the list of our conversations: ", fg=CHATGPT)

        for i in range(len(response["items"])):
            chat = response["items"][i]
            time = datetime.fromisoformat(chat["create_time"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if chat["id"] == self.conversation_id:
                click.secho(f"{i + 1}.", nl=False, fg=IMPORTANT)
                click.secho(f" {time}", nl=False)
                click.secho(f" {chat['id']}", fg=BRIGHT_BLACK, nl=False)
                click.secho(f" {chat['title']}")
            else:
                click.secho(f"{i + 1}.", nl=False, fg=BRIGHT_BLACK)
                click.secho(f" {time}", nl=False)
                click.secho(f" {chat['id']}", fg=BRIGHT_BLACK, nl=False)
                click.secho(f" {chat['title']}")

        click.secho(
            f"Total: {response['total']}, Limit: {response['limit']}, Offset: {response['offset']}"  # noqa: E501
        )

        if not self.conversation_id:
            click.echo("\n")
            self.select_chat(response["items"])

    def delete_chats(self, conversation_id: list[str]):
        for _id in conversation_id:
            click.secho(f"Deleting chat {_id}", fg=CHATGPT)
            response = requests.patch(
                self.conversation_url.format(conversation_id=_id),
                headers=self.headers,
                json={"is_visible": False},
            )
            if response.status_code != 200:
                raise Exception(f"Error: {response.status_code} {response.text}")

    def select_chat(self, chats: list[dict] = None, chat_id: str = None):
        if not chats:
            response = self._get_chat_list()
            chats = response["items"]

        if not chat_id:
            while not chat_id:
                click.secho(
                    "You must select a conversation. Select with the number (e.g. 1), passing a part or the full chat_id (e.g. a63fe212), or enter 'new' to create a new one",  # noqa: E501
                    fg=CHATGPT,
                )
                chat_id = input()

            if chat_id == "new":
                self._save_chat_id()
                self.ask("Creating a new chat")
                click.launch(self.chat_url.format(chat_id=self.conversation_id))
                return

        # select by number
        if len(chat_id) < 3 and int(chat_id) <= len(chats):
            conversation_id = chats[int(chat_id) - 1]["id"]
            last_message = self._get_last_message(conversation_id)
            self._save_chat_id(last_message["id"], conversation_id)
            return

        # select by chat_id
        for chat in chats:
            if chat_id.startswith(chat["id"].split("-")[0]):
                conversation_id = chat_id
                last_message = self._get_last_message(conversation_id)
                self._save_chat_id(last_message["id"], conversation_id)

    def list_messages(self, conversation_id: str):
        conversation_id = conversation_id or self.conversation_id
        messages, title = self._get_messages_in_chat(conversation_id)
        click.secho("Here's the list of messages in ", fg=CHATGPT, nl=False)
        click.secho(f"{title}: ", fg=IMPORTANT)
        for message in messages:
            click.secho(f"{message['create_time']} ", fg=BRIGHT_BLACK, nl=False)
            click.secho(
                f"{message['message']}",
                fg=YOU if message["author"] == "user" else CHATGPT,
            )  # noqa: E501

    def _get_last_message(self, conversation_id: str) -> dict:
        messages, _ = self._get_messages_in_chat(conversation_id)
        return messages[-1]

    def _get_messages_in_chat(self, conversation_id: str):
        response = requests.get(
            self.conversation_url.format(conversation_id=conversation_id),
            headers=self.headers,
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} {response.text}")

        response = response.json()

        messages = []
        for _id, message in response["mapping"].items():
            if not message["message"] or not message["message"]["content"]["parts"][0]:
                continue

            message = message["message"]
            messages.append(
                {
                    "id": _id,
                    "create_time": datetime.fromtimestamp(
                        message["create_time"]
                    ).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # noqa: E501
                    "author": message["author"]["role"],
                    "message": message["content"]["parts"][0],
                }
            )
        return messages, response["title"]

    def _post(self, payload: dict):
        return requests.post(self.url, headers=self.headers, json=payload)

    @staticmethod
    def _parse_response(response):
        text = response.text.split("\n")[-5]

        # Split the text into two parts: "data: " and the JSON payload
        data_str = text.split("data: ")[1]

        try:
            return json.loads(data_str)
        except Exception as e:
            print("Error parsing response", e)
            import pdb

            pdb.set_trace()
            return {}

    @staticmethod
    def _set_headers(chatgtp_token: str, chatgpt_cookie: str):
        return {
            "authority": "chat.openai.com",
            "accept": "text/event-stream",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"Bearer {chatgtp_token}",
            "content-type": "application/json",
            "cookie": chatgpt_cookie,
            "origin": "https://chat.openai.com",
            "referer": "https://chat.openai.com/chat",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',  # noqa: E501
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",  # noqa: E501
        }

    def _you_speak(self, message: str):
        if self.verbosity in (NO_VERBOSITY, ONLY_ANSWER):
            return
        click.secho(message, fg=YOU)

    def _chatgpt_speaks(self, message: str):
        if self.verbosity in (NO_VERBOSITY, ONLY_QUESTIONS):
            return
        click.secho(message, fg=CHATGPT)

    def _save_chat_id(self, last_message_id: str = None, conversation_id: str = None):
        self.last_message_id = last_message_id or str(uuid.uuid4())
        self.conversation_id = conversation_id
        json.dump(
            {
                "last_message_id": self.last_message_id,
                "conversation_id": self.conversation_id,
            },
            open("./storage/latest.json", "w"),
            indent=4,
        )

    def _load_latest_chat_id(self):
        try:
            obj = json.load(open("./storage/latest.json"))
            self.last_message_id = obj["last_message_id"]
            self.conversation_id = obj["conversation_id"]
        except Exception as e:
            click.secho(
                "No project selected. Select one or create a new one\n", fg=CHATGPT
            )

    def _get_chat_list(self):
        response = requests.get(self.chat_list_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} {response.text}")
        return response.json()


if __name__ == "__main__":
    chatgpt = ChatGPT()
    chatgpt.list_chats()
    # chatgpt.ask("Where is Rome?")
    # chatgpt.ask("How many people does have?")
    # chatgpt.ask("How many people does have?")
