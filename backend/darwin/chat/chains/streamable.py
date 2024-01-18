from __future__ import annotations

from collections.abc import Iterator
from queue import Queue
from threading import Thread
from typing import Any

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.base import Chain

from darwin.chat.callbacks.streaming import StreamingHandler


class StreamableChainMixin(Chain):
    def stream(
        self, input: dict[str, Any], *args: Any, **kwargs: Any
    ) -> Iterator[dict[str, Any]]:
        queue: Queue = Queue()
        handler = StreamingHandler(queue=queue)
        question = input["question"]

        def run():
            self(question, *args, **kwargs, callbacks=[handler])

        thread = Thread(target=run)
        thread.start()

        while True:
            token: str = queue.get()
            if token is None:
                break
            yield {"token": token}


class StreamableConversationRetrievalChain(
    StreamableChainMixin, ConversationalRetrievalChain
):
    pass
