from typing import Any

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from pyboxen import boxen


def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))


class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(
        self, serialized: dict[str, Any], messages: list[list[BaseMessage]], *_, **__
    ) -> Any:
        print("\n\n========== Sending Messages ==========\n\n")

        for message in messages[0]:
            if message.type == "system":
                boxen_print(message.content, title=message.type, color="yellow")
            elif message.type == "human":
                boxen_print(message.content, title=message.type, color="green")
            elif message.type == "ai" and "function_call" in message.additional_kwargs:
                call = message.additional_kwargs["function_call"]
                content = f"Running tool {call['name']} with args {call['arguments']}"
                boxen_print(content, title=message.type, color="cyan")
            elif message.type == "ai":
                boxen_print(message.content, title=message.type, color="blue")
            elif message.type == "function":
                boxen_print(message.content, title=message.type, color="purple")
            else:
                boxen_print(message.content, title=message.type, color="red")
