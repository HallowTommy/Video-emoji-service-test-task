import os
import asyncio
import tempfile
from pathlib import Path
import mimetypes

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


def _detect_extension_from_tg(file_obj) -> str:
    # пробуем взять расширение из имени файла
    name = getattr(file_obj, "file_name", "") or getattr(file_obj, "file_name", "")
    ext = Path(name or "").suffix.lower()
    if ext:
        return ext

    # пробуем по mime type
    mime = getattr(file_obj, "mime_type", "") or ""
    if mime:
        guessed = mimetypes.guess_extension(mime)
        if guessed:
            return guessed

    return ".mp4"


@dp.message(F.video | F.document)
async def handle_video(message: Message):
    file_obj = message.video or message.document

    mime = getattr(file_obj, "mime_type", "") or ""
    if not mime.startswith("video/"):
        await message.answer("Пришлите, пожалуйста, видеофайл (любой формат) 🙂")
        return

    await message.answer("Обрабатываю видео, подождите немного…")

    ext = _detect_extension_from_tg(file_obj)
    suffix = ext or ".mp4"

    # временные файлы для входа и выхода
    with tempfile.NamedTemporaryFile(suffix=suffix) as tmp_in, \
         tempfile.NamedTemporaryFile(suffix=suffix) as tmp_out:

        # скачиваем видео из Telegram
        file = await bot.get_file(file_obj.file_id)
        await bot.download_file(file, destination=tmp_in.name)

        # шлём в backend /api/add-emoji
        async with aiohttp.ClientSession() as session:
            with open(tmp_in.name, "rb") as f:
                form = aiohttp.FormData()
                form.add_field(
                    "file",
                    f,
                    filename=f"video{suffix}",
                    content_type=mime or "application/octet-stream",
                )
                async with session.post(
                    f"{BACKEND_URL}/api/add-emoji",
                    data=form,
                ) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        await message.answer(
                            f"Ошибка при обработке видео 😕\n{resp.status}: {text}"
                        )
                        return
                    tmp_out.write(await resp.read())
                    tmp_out.flush()

        # отправляем результат
        await message.answer_video(video=open(tmp_out.name, "rb"))
        # при желании можно посмотреть mime/формат и использовать send_document для нестандартных контейнеров


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
