

# Rimuru LP - Приемник сигналов для https://duty.rimuruproject.ru

## Содержание
1. [Установка Python](#установка-python)
   - [Для Windows](#для-windows)
   - [Для Linux (Ubuntu/Debian)](#для-linux-ubuntu-debian)
2. [Установка и запуск бота](#установка-и-запуск-бота)
3. [Настройка бота](#настройка-бота)
4. [Команды бота](#команды-бота)
5. [Управление ботом](#управление-ботом)
6. [Помощь](#помощь)

---

## Установка Python

### Для Windows
1. Скачайте Python 3.11 с [официального сайта](https://www.python.org/downloads/)
2. Запустите установщик:
   - **ВАЖНО:** Отметьте галочку "Add Python 3.11 to PATH"
   - Нажмите "Install Now"
3. Проверьте установку:
   - Откройте командную строку (Win+R → введите `cmd` → Enter)
   - Введите: `python --version`
   - Должно появиться: `Python 3.11.x`

### Для Linux (Ubuntu/Debian)
```bash
sudo apt-get update -y
sudo apt-get install python3.11 python3.11-venv -y
```

Проверьте установку:
```bash
python3.11 --version
```

---

## Установка и запуск бота

1. **Скачайте проект**
   - Перейдите на [страницу проекта](https://github.com/lutikk/rimuru_lp)
   - Нажмите "Code" → "Download ZIP"
   - Распакуйте архив в удобное место

2. **Перейдите в папку с проектом**
      ```bash
   cd путь_до_папки
   ```


3. **Создайте виртуальное окружение**
   - Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   - Linux:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

4. **Установите зависимости**
```bash
pip install -r req.txt
```

5. **Запустите бота**
```bash
python main.py  # Windows
python3.11 main.py  # Linux
```

6. **При первом запуске:**
   - Введите ваш VK API токен (где получить: https://vkhost.github.io/)
   - Нажмите Enter

---




## Команды бота

### Основные команды (префиксы: .л, !л)
| Команда       | Описание                  | Пример          |
|---------------|---------------------------|-----------------|
| `!л пинг`     | Проверка работоспособности| `!л пинг`       |
| `!л <текст>`  | Отправка сигнала на сервер| `!л тест`       |

### Административные команды (префиксы: .слп, !слп)
#### Управление алиасами
| Команда                     | Описание                          | Пример              |
|-----------------------------|-----------------------------------|---------------------|
| `!слп +алиас <имя>\n<сокр>\n<полн>` | Создать алиас           | `!слп +алиас тест\nт\nтест` |
| `!слп -алиас <имя>`         | Удалить алиас                    | `!слп -алиас тест`  |
| `!слп алиасы`               | Список алиасов                   | `!слп алиасы`       |

#### Управление доверенными пользователями
| Команда               | Описание                          | Пример          |
|-----------------------|-----------------------------------|-----------------|
| `!слп +дов [@user]`   | Добавить в доверенные             | `!слп +дов @user` |
| `!слп -дов [@user]`   | Удалить из доверенных             | `!слп -дов @user` |
| `!слп довы`           | Список доверенных пользователей   | `!слп довы`     |
| `!слп дов <префикс>`  | Установить префикс для доверенных | `!слп дов !`    |

#### Управление игнором
| Команда               | Описание                          | Пример          |
|-----------------------|-----------------------------------|-----------------|
| `!слп +игнор [@user]` | Добавить в игнор                  | `!слп +игнор @user` |
| `!слп -игнор [@user]` | Удалить из игнора                 | `!слп -игнор @user` |
| `!слп +глоигнор [@user]` | Глобальный игнор              | `!слп +глоигнор @user` |
| `!слп -глоигнор [@user]` | Удалить из глобального игнора | `!слп -глоигнор @user` |
| `!слп игнор лист`     | Список игнорируемых в чате        | `!слп игнор лист` |
| `!слп глоигнор лист`  | Список глобально игнорируемых     | `!слп глоигнор лист` |

#### Приветствия
| Команда               | Описание                          | Пример          |
|-----------------------|-----------------------------------|-----------------|
| `!слп +приветствие\n<текст>` | Установить приветствие    | `!слп +приветствие\nПривет!` |
| `!слп -приветствие`   | Удалить приветствие               | `!слп -приветствие` |

#### Системные команды
| Команда               | Описание                          | Пример          |
|-----------------------|-----------------------------------|-----------------|
| `!слп инфо`           | Информация о боте                 | `!слп инфо`     |
| `!слп сервер`         | Статистика сервера                | `!слп сервер`   |
| `!слп +преф <префикс>`| Добавить префикс                  | `!слп +преф ?`  |
| `!слп -преф <префикс>`| Удалить префикс                   | `!слп -преф ?`  |

---

## Управление ботом
- **Запуск:** 
  ```bash
  source venv/bin/activate  # Активация окружения (Linux)
  python main.py
  ```

- **Остановка:**
  - Нажмите `Ctrl+C` в окне терминала

- **Автозапуск на сервере (Linux):**
  ```bash
  sudo nano /etc/systemd/system/rimuru.service
  ```
  Добавьте:
  ```ini
  [Unit]
  Description=Rimuru LP Service
  After=network.target

  [Service]
  User=root
  WorkingDirectory=/path/to/bot
  ExecStart=/path/to/venv/bin/python /path/to/bot/main.py
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
  Затем:
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable rimuru
  sudo systemctl start rimuru
  ```

---

## Помощь
При возникновении проблем обращайтесь:
- [@allbanned](https://vk.com/allbanned)
- [@misha_meow](https://vk.com/misha_meow)

> Бот создан для удобного взаимодействия с Rimuru Project. Не злоупотребляйте командами!
