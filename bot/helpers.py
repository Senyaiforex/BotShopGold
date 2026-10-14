import json
import os
import aiofiles
import asyncio

CONFIG_FILE = "config.json"
_lock = asyncio.Lock()  # защита от одновременной записи


async def load_config() -> dict:
    """Асинхронно читает конфиг из файла"""
    if not os.path.exists(CONFIG_FILE):
        default = {"rate": 60}
        await save_config(default)
        return default
    async with aiofiles.open(CONFIG_FILE, "r", encoding="utf-8") as f:
        content = await f.read()
    return json.loads(content)


async def save_config(config: dict) -> None:
    """Асинхронно сохраняет конфиг в файл."""
    async with _lock:
        async with aiofiles.open(CONFIG_FILE, "w", encoding="utf-8") as f:
            await f.write(json.dumps(config, ensure_ascii=False, indent=4))


async def get_value(key: str, default=None):
    """Получить значение по ключу"""
    config = await load_config()
    return config.get(key, default)


async def set_value(key: str, value) -> None:
    """Установить значение по ключу"""
    async with _lock:
        config = await load_config()
        config[key] = value
        async with aiofiles.open(CONFIG_FILE, "w", encoding="utf-8") as f:
            await f.write(json.dumps(config, ensure_ascii=False, indent=4))