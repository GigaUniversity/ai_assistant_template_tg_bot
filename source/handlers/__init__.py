from aiogram import Router
from .user_message import router as user_message_router
from .user_commands import router as user_commands_router

user_router = Router(name='user_router')


user_commands_router.include_router(user_message_router)
user_router.include_router(user_commands_router)

