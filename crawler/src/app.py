import asyncio
import aiohttp
import uvloop
from typing import List
from .tracing import trace_config
from .utils import parse_args, get_job, write_to_file, Result
from .handlers import keywords
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Job:

    operations = {
        'keywords': keywords
    }

    def __init__(self, name: str,
                 operation: str,
                 urls: List[str],
                 workers: int):
        self.filepath = f'crawler/results/{name}'
        self.operation = operation
        self.urls = urls
        self.semaphore = asyncio.Semaphore(workers)
        self.results = []

    def scrap(self, data: str) -> str:
        ''' Synchronous! '''
        return Job.operations[self.operation](data)

    async def get(self, session: aiohttp.ClientSession, url: str):
        async with self.semaphore:
            try:
                async with session.get(url, timeout=5) as response:
                    data = self.scrap(await response.text())
                    result = Result(url, response.status, data)
            except Exception as exception:
                result = Result(url, 0, type(exception).__name__)
        self.results.append(result)

    async def parse(self, urls: List[str], workers: int = 10):
        timeout = aiohttp.ClientTimeout()
        async with aiohttp.ClientSession(trace_configs=[trace_config],
                                         timeout=timeout) as session:
            await asyncio.gather(*(self.get(session, url) for url in urls))
            data = [str(result) for result in self.results]
            await write_to_file(self.filepath, ''.join(data))


def run():
    name = parse_args()
    job_config = get_job(name)
    urls = job_config['urls']
    operation = job_config['operation']
    workers = job_config['workers']
    loop = asyncio.get_event_loop()
    job = Job(name, operation, urls, workers)
    loop.run_until_complete(job.parse(urls, workers))
    loop.close()
