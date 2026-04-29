import asyncio
import random
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChatAdminRequiredError

# ========== НАСТРОЙКИ ==========
API_ID = 28995296      # Ваш API ID
API_HASH =  '4008ef493fc810f39892762fbdcba660' # Ваш API Hash
PHONE = '+######'   # Ваш номер телефона в международном формате
SESSION = 'my_session'     # Имя файла сессии
BOT_TOKEN = None           # Если вы бот, укажите его токен

# ========== ФУНКЦИЯ ЗАГРУЗКИ ЮЗЕРНЕЙМОВ ==========
def load_usernames(file_path='usernames.txt'):
    """Читает юзернеймы из файла (каждый с новой строки)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().replace('@', '') for line in f if line.strip()]

# ========== ФУНКЦИЯ ЗАГРУЗКИ СООБЩЕНИЯ ==========
def load_message(file_path='message.txt'):
    """Читает текст сообщения из файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# ========== ОСНОВНАЯ АСИНХРОННАЯ ФУНКЦИЯ ==========
async def send_messages():
    # Создаём клиент
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start(phone=PHONE)
    print('[✓] Клиент запущен и авторизован')

    # Загружаем данные
    usernames = load_usernames('usernames.txt')
    message_text = load_message('message.txt')
    print(f'[•] Загружено чатов: {len(usernames)}')
    print(f'[•] Сообщение: {message_text[:50]}...')

    # Отправляем сообщения
    for idx, username in enumerate(usernames, 1):
        try:
            # Отправляем сообщение в чат или канал
            await client.send_message(username, message_text)
            print(f'[{idx}/{len(usernames)}] ✓ Отправлено в @{username}')

            # Задержка между отправками (5-15 секунд)
            delay = random.uniform(5, 15)
            await asyncio.sleep(delay)

        except FloodWaitError as e:
            print(f'[{idx}/{len(usernames)}] ✗ Лимит в @{username}: ждём {e.seconds} сек.')
            await asyncio.sleep(e.seconds)
            # После ожидания пробуем отправить ещё раз
            try:
                await client.send_message(username, message_text)
                print(f'[{idx}/{len(usernames)}] ✓ Отправлено в @{username}')
            except Exception as retry_err:
                print(f'[{idx}/{len(usernames)}] ✗ Ошибка повторной отправки: {retry_err}')

        except ChatAdminRequiredError:
            print(f'[{idx}/{len(usernames)}] ✗ Не хватает прав в @{username}')

        except Exception as e:
            print(f'[{idx}/{len(usernames)}] ✗ Ошибка: {type(e).__name__}: {e}')

    await client.disconnect()
    print('[✓] Рассылка завершена, клиент отключён\nBy @Xalarus')

# ========== ТОЧКА ВХОДА ==========
if __name__ == '__main__':
    print('[•] Запуск программы рассылки\nBy @Xalarus ,по всем вопросам пиши мне')
    asyncio.run(send_messages())