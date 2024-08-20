from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Определяем область доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Получаем содержимое JSON-файла из переменной окружения
credentials_json = os.environ.get('telegram-432911-305d284f8269.json')

# Преобразуем JSON-строку в объект
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials_json), scope)

# Подключаемся к Google Sheets
client = gspread.authorize(creds)
sheet = client.open("Расходы").sheet1


# Настройка магазинов, групп, подгрупп и дополнительных подгрупп
STORES = {
    "Охта Молл": {
        "Часовое направление": {
            "Ремни и прочее": [],
            "Элементы питания": [],
            "Запчасти и механизмы": [],
            "Работы аутсорс": []
        },
        "Ювелирное направление": {
            "Материал": ["Золото", "Серебро", "Платина"],
            "3D-моделирование": [],
            "Восковые модели": [],
            "Литьё": [],
            "ТО оборудования": [],
            "Ювелирные вставки": ["ДК (1-я группа)", "Другие"],
            "Расх. мат. для юв. серв.": [],
            "Фурнитура для юв. серв.": ["Золото", "Серебро", "Бижутерия"],
            "Юв. полуфабрикаты": ["Золото", "Серебро"],
            "Юв. работы аутсорс": ["Золото", "Серебро", "Монтировка", "Гальваника", "ЗЮВ", "Цепи/браслеты ручные"],
            "Другое": []
        },
        "Услуги гравировки": {
            "Расходные материалы": [],
            "ТО оборудования": [],
            "Работы аутсорс": [],
            "Другое": []
        },
        "Прочие расходы": {
            "Хоз. обеспечение": [],
            "Логистика": [],
            "Ремонт/обсл. оф. техники": [],
            "Инструмент": []
        },
        "Развитие мастерской": {
            "Оборудование": [],
            "Инструмент": [],
            "Сайт": [],
            "Социальные сети": [],
            "Бизнес-процессы": [],
            "Другое": []
        },
        "Маркетинг": {
            "Полиграфия": [],
            "Рекламные носители": [],
            "Сайт": [],
            "Услуги дизайнеров": [],
            "Другое": []
        }
    },
    "Охтинский бульвар": {
        "Часовое направление": {
            "Ремни и прочее": [],
            "Элементы питания": [],
            "Запчасти и механизмы": [],
            "Работы аутсорс": []
        },
        "Ювелирное направление": {
            "Материал": ["Золото", "Серебро", "Платина"],
            "3D-моделирование": [],
            "Восковые модели": [],
            "Литьё": [],
            "ТО оборудования": [],
            "Ювелирные вставки": ["ДК (1-я группа)", "Другие"],
            "Расх. мат. для юв. серв.": [],
            "Фурнитура для юв. серв.": ["Золото", "Серебро", "Бижутерия"],
            "Юв. полуфабрикаты": ["Золото", "Серебро"],
            "Юв. работы аутсорс": ["Золото", "Серебро", "Монтировка", "Гальваника", "ЗЮВ", "Цепи/браслеты ручные"],
            "Другое": []
        },
        "Услуги гравировки": {
            "Расходные материалы": [],
            "ТО оборудования": [],
            "Работы аутсорс": [],
            "Другое": []
        },
        "Прочие расходы": {
            "Хоз. обеспечение": [],
            "Логистика": [],
            "Ремонт/обсл. оф. техники": [],
            "Инструмент": []
        },
        "Развитие мастерской": {
            "Оборудование": [],
            "Инструмент": [],
            "Сайт": [],
            "Социальные сети": [],
            "Бизнес-процессы": [],
            "Другое": []
        },
        "Маркетинг": {
            "Полиграфия": [],
            "Рекламные носители": [],
            "Сайт": [],
            "Услуги дизайнеров": [],
            "Другое": []
        }
    },
    "Пять озёр": {
        "Часовое направление": {
            "Ремни и прочее": [],
            "Элементы питания": [],
            "Запчасти и механизмы": [],
            "Работы аутсорс": []
        },
        "Ювелирное направление": {
            "Материал": ["Золото", "Серебро", "Платина"],
            "3D-моделирование": [],
            "Восковые модели": [],
            "Литьё": [],
            "ТО оборудования": [],
            "Ювелирные вставки": ["ДК (1-я группа)", "Другие"],
            "Расх. мат. для юв. серв.": [],
            "Фурнитура для юв. серв.": ["Золото", "Серебро", "Бижутерия"],
            "Юв. полуфабрикаты": ["Золото", "Серебро"],
            "Юв. работы аутсорс": ["Золото", "Серебро", "Монтировка", "Гальваника", "ЗЮВ", "Цепи/браслеты ручные"],
            "Другое": []
        },
        "Услуги гравировки": {
            "Расходные материалы": [],
            "ТО оборудования": [],
            "Работы аутсорс": [],
            "Другое": []
        },
        "Прочие расходы": {
            "Хоз. обеспечение": [],
            "Логистика": [],
            "Ремонт/обсл. оф. техники": [],
            "Инструмент": []
        },
        "Развитие мастерской": {
            "Оборудование": [],
            "Инструмент": [],
            "Сайт": [],
            "Социальные сети": [],
            "Бизнес-процессы": [],
            "Другое": []
        },
        "Маркетинг": {
            "Полиграфия": [],
            "Рекламные носители": [],
            "Сайт": [],
            "Услуги дизайнеров": [],
            "Другое": []
        }
    },
    "Общее": {
        "Часовое направление": {
            "Ремни и прочее": [],
            "Элементы питания": [],
            "Запчасти и механизмы": [],
            "Работы аутсорс": []
        },
        "Ювелирное направление": {
            "Материал": ["Золото", "Серебро", "Платина"],
            "3D-моделирование": [],
            "Восковые модели": [],
            "Литьё": [],
            "ТО оборудования": [],
            "Ювелирные вставки": ["ДК (1-я группа)", "Другие"],
            "Расх. мат. для юв. серв.": [],
            "Фурнитура для юв. серв.": ["Золото", "Серебро", "Бижутерия"],
            "Юв. полуфабрикаты": ["Золото", "Серебро"],
            "Юв. работы аутсорс": ["Золото", "Серебро", "Монтировка", "Гальваника", "ЗЮВ", "Цепи/браслеты ручные"],
            "Другое": []
        },
        "Услуги гравировки": {
            "Расходные материалы": [],
            "ТО оборудования": [],
            "Работы аутсорс": [],
            "Другое": []
        },
        "Прочие расходы": {
            "Хоз. обеспечение": [],
            "Логистика": [],
            "Ремонт/обсл. оф. техники": [],
            "Инструмент": []
        },
        "Развитие мастерской": {
            "Оборудование": [],
            "Инструмент": [],
            "Сайт": [],
            "Социальные сети": [],
            "Бизнес-процессы": [],
            "Другое": []
        },
        "Маркетинг": {
            "Полиграфия": [],
            "Рекламные носители": [],
            "Сайт": [],
            "Услуги дизайнеров": [],
            "Другое": []
        }
    }
}

# Глобальные переменные для хранения данных пользователя
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_data[user_id] = {}  # Инициализируем словарь для хранения данных пользователя
    keyboard = [
        [InlineKeyboardButton(store, callback_data=f'store_{store}')] for store in STORES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите магазин:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if query.data.startswith('store_'):
        store = query.data.split('_')[1]
        user_data[user_id]['store'] = store
        keyboard = [
            [InlineKeyboardButton(group, callback_data=f'group_{group}')] for group in STORES[store]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text('Выберите направление:', reply_markup=reply_markup)

    elif query.data.startswith('group_'):
        group = query.data.split('_')[1]
        user_data[user_id]['group'] = group
        store = user_data[user_id]['store']

        # Проверка, есть ли подгруппы для выбранной группы
        if isinstance(STORES[store][group], dict):  # Если есть вложенный словарь (подгруппы)
            keyboard = [
                [InlineKeyboardButton(subgroup, callback_data=f'subgroup_{subgroup}')] for subgroup in STORES[store][group]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text('Выберите категорию:', reply_markup=reply_markup)
        elif isinstance(STORES[store][group], list) and STORES[store][group]:  # Если есть список элементов
            keyboard = [
                [InlineKeyboardButton(item, callback_data=f'item_{item}')] for item in STORES[store][group]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text('Выберите подкатегорию:', reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Введите стоимость:")
            context.user_data['awaiting_cost'] = True

    elif query.data.startswith('subgroup_'):
        subgroup = query.data.split('_')[1]
        user_data[user_id]['subgroup'] = subgroup
        store = user_data[user_id]['store']
        group = user_data[user_id]['group']

               # Проверка, есть ли дополнительные подгруппы для подгруппы
        if isinstance(STORES[store][group][subgroup], list) and STORES[store][group][subgroup]:  # Если конечный список
            keyboard = [
                [InlineKeyboardButton(option, callback_data=f'option_{option}')] for option in STORES[store][group][subgroup]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text('Выберите дополнительную категорию:', reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Введите стоимость:")
            context.user_data['awaiting_cost'] = True

    elif query.data.startswith('item_'):
        item = query.data.split('_')[1]
        user_data[user_id]['item'] = item
        await context.bot.send_message(chat_id=query.message.chat_id, text="Введите стоимость:")
        context.user_data['awaiting_cost'] = True

    elif query.data.startswith('option_'):
        option = query.data.split('_')[1]
        user_data[user_id]['option'] = option
        await context.bot.send_message(chat_id=query.message.chat_id, text="Введите стоимость:")
        context.user_data['awaiting_cost'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if context.user_data.get('awaiting_cost'):
        user_data[user_id]['cost'] = update.message.text
        await context.bot.send_message(chat_id=chat_id, text="Введите комментарий:")
        context.user_data['awaiting_comment'] = True
        context.user_data['awaiting_cost'] = False

    elif context.user_data.get('awaiting_comment'):
        user_data[user_id]['comment'] = update.message.text

        # Подготавливаем данные для записи
        data_row = [
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),  # A - Дата
            update.message.from_user.username or "Unknown",  # B - Имя пользователя (или "Unknown", если нет)
            user_data[user_id].get('store'),              # C - 1-й выбор
            user_data[user_id].get('group'),              # D - 2-й выбор
            user_data[user_id].get('subgroup', ''),       # E - 3-й выбор
            user_data[user_id].get('option', ''),         # F - 4-й выбор (если есть)
            user_data[user_id].get('cost'),               # G - Стоимость
            user_data[user_id].get('comment')             # H - Комментарий
        ]

        # Записываем данные в Google Sheets в конкретные столбцы, начиная с первой доступной строки
        range_cells = f"A{len(sheet.get_all_values())+1}:H{len(sheet.get_all_values())+1}"
        sheet.update(values=[data_row], range_name=range_cells)

        await context.bot.send_message(chat_id=chat_id, text="Данные успешно сохранены! Нажмите /start, чтобы начать заново.")
        user_data.pop(user_id, None)  # Очищаем данные пользователя
        context.user_data['awaiting_comment'] = False

# Создаем приложение
application = Application.builder().token("7432281200:AAHOlKfslVHds5l3bN39CGl6ElBDt3U89pU").build()

application.add_handler(CommandHandler('start', start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
application.run_polling(drop_pending_updates=True)

