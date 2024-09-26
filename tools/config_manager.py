import json

import aiofiles


async def read_config():
    """Returns config as a dict"""
    async with aiofiles.open('tools/config.json', mode='r') as f:
        config = await f.read()
        return json.loads(config)


async def write_config(config):
    """Writes config to file"""
    async with aiofiles.open('tools/config.json', mode='w') as f:
        await f.write(json.dumps(config))


async def update_config_value(key: str, value):
    """Updates value of a specific key in config"""
    config = await read_config()
    config[key] = float(value)
    await write_config(config)


async def get_config_value(key: str):
    """Returns value of a specific key in config"""
    config = await read_config()
    return config.get(key)
