import asyncio
import random
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChatAdminRequiredError

# ========== НАСТРОЙКИ (оставьте свои) ==========
API_ID = 123456        # Ваш API ID (число)
API_HASH = 'ваш_api_hash'
SESSION = 'my_session'

# ========== ФУНКЦИИ ЗАГРУЗКИ ДАННЫХ ==========
def load_usernames(file_path='usernames.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().replace('@', '') for line in f if line.strip()]

def load_message(file_path='message.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# ========== ОСНОВНАЯ ФУНКЦИЯ ==========
async def send_messages():
    # Запрашиваем номер телефона у пользователя
    phone = input('Введите ваш номер телефона в международном формате (например +79123456789): ').strip()
    if not phone:
        print('[✗] Номер не введён, завершение.')
        return

    # Создаём клиент (сессия сохранится – повторно код не запросит)
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start(phone=phone)   # номер передаётся, но если сессия уже есть – код не спросит
    print('[✓] Клиент запущен и авторизован')

    usernames = load_usernames('usernames.txt')
    message_text = load_message('message.txt')
    print(f'[•] Загружено чатов: {len(usernames)}')
    print(f'[•] Сообщение: {message_text[:50]}...')

    for idx, username in enumerate(usernames, 1):
        try:
            await client.send_message(username, message_text)
            print(f'[{idx}/{len(usernames)}] ✓ Отправлено в @{username}')
            await asyncio.sleep(random.uniform(5, 15))
        except FloodWaitError as e:
            print(f'[{idx}/{len(usernames)}] ✗ Лимит в @{username}: ждём {e.seconds} сек.')
            await asyncio.sleep(e.seconds)
            # Повторная попытка
            try:
                await client.send_message(username, message_text)
                print(f'[{idx}/{len(usernames)}] ✓ Отправлено в @{username}')
            except Exception as retry_err:
                print(f'[{idx}/{len(usernames)}] ✗ Ошибка повторной отправки: {retry_err}')
        except ChatAdminRequiredError:
            print(f'[{idx}/{len(usernames)}] ✗ Нет прав в @{username}')
        except Exception as e:
            print(f'[{idx}/{len(usernames)}] ✗ Ошибка: {type(e).__name__}: {e}')

    await client.disconnect()
    print('[✓] Рассылка завершена')

if __name__ == '__main__':
    print('[•] Запуск рассыльщика')
    asyncio.run(send_messages())
