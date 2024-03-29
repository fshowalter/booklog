from __future__ import annotations

from typing import Callable, Generator, Sequence

import pytest
from prompt_toolkit.application.current import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

MockInput = Callable[[Sequence[str]], None]


@pytest.fixture(autouse=True, scope="function")
def mock_input() -> Generator[MockInput, None, None]:
    with create_pipe_input() as pipe_input:
        with create_app_session(input=pipe_input, output=DummyOutput()):

            def factory(input_sequence: Sequence[str]) -> None:  # noqa: WPS 430
                pipe_input.send_text("".join(input_sequence))

            yield factory
