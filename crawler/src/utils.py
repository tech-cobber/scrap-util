import yaml
import dataclasses
import argparse
import aiofiles

result_str = 'url: {0}\nstatus: {1}\ndata: {2}\n\n'


@dataclasses.dataclass
class Result:
    url: str
    status: int
    data: str

    def __str__(self):
        return result_str.format(self.url, self.status, self.data)


def parse_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("job", type=str, help='Name of the job file')
    args = parser.parse_args()
    return args.job


def get_job(filename: str) -> dict:
    config = {}
    with open(f'crawler/jobs/{filename}.yaml', 'rt') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return config


async def write_to_file(filepath: str, data: str):
    async with aiofiles.open(filepath, mode='w') as f:
        await f.write(data)
