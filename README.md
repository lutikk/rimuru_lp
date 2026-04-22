# rimuru_lp

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/vk-long--poll-4680C2.svg" alt="VK">
  <img src="https://img.shields.io/badge/framework-vkbottle-blueviolet.svg" alt="vkbottle">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

Лёгкий VK long-poll юзербот на [vkbottle](https://github.com/vkbottle/vkbottle) с модульной системой команд и собственными VBML-префиксами.

## Возможности

- **Long-poll клиент VK** — авторизация через user-токен
- **Модульные команды** — каждая команда живёт в `commands/<name>.py`
- **VBML-валидаторы** — префиксы `service`, `self`, `alias`
- **Секретный код** — автогенерация по токену для self-команд
- **Ignore-middleware** — фильтрация событий от игнор-листа
- **Локальное хранилище пользователя** — `models.User.load()` / `.save()`

## Установка

```bash
pip install -r req.txt
```

## Использование

```bash
python main.py
```

При первом запуске создастся профиль пользователя; токен укажите в модели `User`.

## Структура

```
rimuru_lp/
├── main.py             # Точка входа
├── lp.py               # Long-poll обёртка
├── utils.py            # get_code и др.
├── middlewares.py      # UserIgnore
├── validator.py        # VBML префиксы: service, self, alias
├── models.py           # Модель User (load/save)
├── commands/           # Обработчики команд
│   ├── ping.py         # Проверка связи
│   ├── info.py         # Информация
│   ├── chats.py        # Управление чатами
│   ├── send_signal.py  # Отправка сигнала
│   ├── ignore.py       # Игнор-лист
│   ├── alias.py        # Алиасы
│   └── dov.py          # Доверенные
└── req.txt
```

## Конфигурация

Настройки пользователя — в локальном файле модели (`models.User`). Секретный код вычисляется из токена при старте (`get_code(token)`).

Использует форк vkbottle: `git+https://github.com/lutikk/vkbottle.git`.
