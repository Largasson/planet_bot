Constellation planet bot for Telegram
===================================
Бот определяет констелляцию планеты солнечной системы на текущую дату.
Бот находится в репозитории GitHub по адресу https://github.com/Largasson/planet_bot.
Функции бота:

1. Команда /start активирует бота, вызывает приветствие и информационное сообщение.
2. Команда /plant <planet> принимает имя планеты и возвращает информационное
   сообщение о том, в какой констелляции расположена запрашиваемая планета. Пример:
   Ввод - /planet mars Вывод - На данный момент Mars расположен в констелляции: <указывается констелляция>.
   Допускается вводить название планеты на русском или английском языке.
3. При некорректном вводе бот выведет сообщение об отсутствии такой команды или об ошибке именования планеты.

Установка бота:


1. Клонировать репозиторий на локальный компьютер или сервер.
2. Создать виртуальное окружение.
3. Установить требуемые пакеты из requirements.txt. 
4. Получить у botFather Telegram уникальный ключ для своего бота.
5. Создать в каталоге, где расположен файл бота файл settings.py.
6. Внести запись API_KEY = "ключ полученный от botFather Telegram", сохранить файл.

English

The bot determines the constellation of the planet of the solar system for the current date.
The bot is located in the GitHub repository at https://github.com/Largasson/planet_bot. 
Bot functions:

1. The /start command activates the bot, calls a greeting and an information message.
2. The /plant <planet> command takes the name of the planet and returns information
    a message indicating in which constellation the requested planet is located. Example:
    Input - /planet mars Output - At the moment, Mars is located in the constellation: <constellation indicated>.
    You can enter the name of the planet in Russian or English.
3. If you enter it incorrectly, the bot will display a message about the absence of such a command or about an error in naming the planet.

Bot installation:

1. Clone the repository to your local computer or server.
2. Create a virtual environment.
3. Install the required packages from requirements.txt.
4. Get a unique key for your bot from botFather Telegram.
5. Create a settings.py file in the directory where the bot file is located.
6. Enter the entry API_KEY = "key received from botFather Telegram", save the file.