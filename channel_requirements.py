from aiogram import Bot, types
from aiogram.filters import Filter
from config import CHANNEL_LINK as channel_link, CHANNEL_ID as channel_id

class CheckSubRequirement(Filter):
    async def __call__(self, message: types.Message, bot: Bot):
        channels_tick = 0
        for i in channel_id:
            user_status = await bot.get_chat_member(i, message.from_user.id)
            if user_status.status in ['creator', 'administrator', 'member']:
                channels_tick += 1
        if channels_tick == len(channel_id):
            return False
        return True

channels_dict = {
    'Reclams (☠)': f'{channel_link[0]}',
    'Images (🎂)': f'{channel_link[1]}'
}
