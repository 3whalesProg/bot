from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token="6550185614:AAGKV1MKS9tab0gBzTZFWlELtlRj4tqkgfI")

dp = Dispatcher(bot, storage=storage)