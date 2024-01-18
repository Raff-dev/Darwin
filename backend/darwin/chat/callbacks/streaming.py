from __future__ import annotations

from queue import Queue
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue):
        self.queue = queue
        self.streaming_run_ids: set[UUID] = set()

    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        *_: Any,
        run_id: UUID,
        **__: Any,
    ) -> Any:
        if serialized.get("kwargs", {}).get("streaming"):
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(
        self,
        token: str,
        *_: Any,
        run_id: UUID,
        **__: Any,
    ) -> Any:
        if run_id in self.streaming_run_ids:
            self.queue.put(token)

    def on_llm_end(
        self,
        *_: Any,
        run_id: UUID,
        **__: Any,
    ) -> None:
        if run_id in self.streaming_run_ids:
            self.streaming_run_ids.remove(run_id)
            self.queue.put(None)

    def on_llm_error(
        self,
        *_,
        run_id: UUID,
        **__: Any,
    ) -> Any:
        if run_id in self.streaming_run_ids:
            self.streaming_run_ids.remove(run_id)
            self.queue.put(None)
