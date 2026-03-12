import asyncio
from unittest.mock import MagicMock

from main import _handle_asyncio_exception


def test_suppresses_aioice_stun_invalid_state_error() -> None:
    """Benign aioice STUN transaction errors should be suppressed."""
    loop = MagicMock(spec=asyncio.AbstractEventLoop)
    context = {
        "message": "Exception in callback Transaction.__retry()",
        "exception": asyncio.InvalidStateError("invalid state"),
    }

    _handle_asyncio_exception(loop, context)

    loop.default_exception_handler.assert_not_called()


def test_forwards_other_invalid_state_errors_to_default_handler() -> None:
    """InvalidStateError not from Transaction.__retry should use default handler."""
    loop = MagicMock(spec=asyncio.AbstractEventLoop)
    context = {
        "message": "Exception in callback some_other_callback()",
        "exception": asyncio.InvalidStateError("invalid state"),
    }

    _handle_asyncio_exception(loop, context)

    loop.default_exception_handler.assert_called_once_with(context)


def test_forwards_non_invalid_state_errors_to_default_handler() -> None:
    """Non-InvalidStateError exceptions should use default handler."""
    loop = MagicMock(spec=asyncio.AbstractEventLoop)
    context = {
        "message": "Exception in callback Transaction.__retry()",
        "exception": RuntimeError("something else"),
    }

    _handle_asyncio_exception(loop, context)

    loop.default_exception_handler.assert_called_once_with(context)
