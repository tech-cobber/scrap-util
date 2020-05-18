from aiohttp import TraceConfig, ClientSession
from aiohttp.tracing import (TraceRequestEndParams,
                             TraceRequestStartParams,
                             TraceRequestRedirectParams,
                             TraceRequestExceptionParams)
from types import SimpleNamespace
from loguru import logger


async def on_request_start(session: ClientSession,
                           trace_config_ctx: SimpleNamespace,
                           params: TraceRequestStartParams):
    logger.debug(f"Starting request {params.method}: {params.url}")


async def on_request_end(session: ClientSession,
                         trace_config_ctx: SimpleNamespace,
                         params: TraceRequestEndParams):
    status: int = params.response.status
    if status == 200:
        logger.debug(f"[{status}]")
    else:
        method, url = params.method, params.url
        logger.debug(f"Ending request {method}: {url} with status [{status}]")


async def on_request_exception(session: ClientSession,
                               trace_config_ctx: SimpleNamespace,
                               params: TraceRequestExceptionParams):
    method, url, exception = params.method, params.url, type(params.exception)
    logger.error(f"{method}: {url} raised {exception.__name__}")


async def on_request_redirect(session: ClientSession,
                              trace_config_ctx: SimpleNamespace,
                              params: TraceRequestRedirectParams):
    logger.info(f"Redirected to {params.response.url}")

trace_config = TraceConfig()
trace_config.on_request_start.append(on_request_start)
trace_config.on_request_end.append(on_request_end)
trace_config.on_request_redirect.append(on_request_redirect)
trace_config.on_request_exception.append(on_request_exception)
