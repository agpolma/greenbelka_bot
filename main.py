import telebot
from telebot import types

bot = telebot.TeleBot('6547554591:AAFHMXCn0ues0CM2DaUR595ZbOFA2lAcyAQ')

condition = 0
prozero_text = 'Не принимается на акции, но можно сдать в <i>экоцентре ProZero</i>. Новосибирск, ул. Восход, 1.'
prozero_url_tg = "https://t.me/prozero_eco"
greenbelka_url_tg = "https://t.me/greenbelka"
greenbelka_url_vk = "https://vk.com/eco_week"

def main_menu(message):
    msg = 'Чем ещё я могу помочь?'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Начать сортировку", callback_data='начало сортировки'))
    markup.add(types.InlineKeyboardButton("Перейти в группу зелёной белки ТГ", url=greenbelka_url_tg))
    markup.add(types.InlineKeyboardButton("Перейти в группу зелёной белки ВК", url=greenbelka_url_vk))
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start_func(message):
    greet_message = f'Привет, {message.from_user.first_name} {message.from_user.last_name}!' \
                    f' Я - бот Зелёной белки, и я помогу тебе рассортировать вторсырьё.'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Начать сортировку", callback_data='начало сортировки'))
    markup.add(types.InlineKeyboardButton("Перейти в группу зелёной белки ТГ", url=greenbelka_url_tg))
    markup.add(types.InlineKeyboardButton("Перейти в группу зелёной белки ВК", url=greenbelka_url_vk))
    bot.send_message(message.chat.id, greet_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    start = types.KeyboardButton('/start')
    marks = types.KeyboardButton('Маркировки')
    markup.add(types.KeyboardButton("Перейти в группу зелёной белки"))
    markup.add(start, marks)
    bot.send_message(message.chat.id, 'Чем я могу тебе помочь?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'начало сортировки')
def sort_start(call):
    if call.message:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Из нескольких материалов", callback_data='несколько материалов'))
        markup.add(types.InlineKeyboardButton("Из нескольких частей", callback_data='разделить части'))
        markup.add(types.InlineKeyboardButton("Бумага или картон", callback_data='бумага'))
        markup.add(types.InlineKeyboardButton("Металл", callback_data='металл'))
        markup.add(types.InlineKeyboardButton("Стекло", callback_data='стекло'))
        markup.add(types.InlineKeyboardButton("Пластик", callback_data='пластик'))
        bot.send_message(call.message.chat.id, "Возьми предмет, который хочешь сдать на переработку " +
                                               "и отвечай на мои вопросы.",
                         parse_mode='html')
        bot.send_message(call.message.chat.id, "Из какого материала сделан предмет?", parse_mode='html',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'несколько материалов')
def several_materials(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Можно", callback_data='разделить части'))
    markup.add(types.InlineKeyboardButton("Нельзя", callback_data='нельзя разделить'))
    bot.send_message(call.message.chat.id, "Материалы можно отделить друг от друга?",
                     parse_mode='html',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'разделить части')
def divide(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Начать сортировку", callback_data='начало сортировки'))
    bot.send_message(call.message.chat.id, "Нужно разделить на части и для каждой пройти тест отдельно",
                     parse_mode='html',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'нельзя разделить')
def not_divide(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Да", callback_data='техника и батарейки'))
    markup.add(types.InlineKeyboardButton(text="Нет", callback_data='не принимается'))
    bot.send_message(call.message.chat.id, "Это техника или батарейка?",
                     parse_mode='html',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'техника и батарейки')
def technic(call):
    bot.send_message(call.message.chat.id,
                     'Принимается на акции. <i><b>Батарейки с аккумуляторами</b></i> отдельно, ' +
                     '<i><b>техника</b></i> отдельно',
                     parse_mode='html')
    main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'бумага')    # TODO заменить на startwith?
def paper(call):
    if call.data == 'бумага':
        photo = open('Пульперкартон.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='экоцентр'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='бумага, не втулки'))
        bot.send_message(call.message.chat.id, 'Это втулка, упаковка от яиц или подобные им (см.фото)?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'бумага, не втулки':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='бумага, не одноразовая'))
        bot.send_message(call.message.chat.id,
                         'Это бумага одноразового использования (салфетки, туалетная бумага и пр.)?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'бумага, не одноразовая':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='бумага, без ламинации'))
        bot.send_message(call.message.chat.id, 'На бумаге есть ламинация (плёнка, проверяется на надрыв)?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'бумага, без ламинации':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='бумага, без жира'))
        bot.send_message(call.message.chat.id, 'На бумаге есть пятна жира?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'бумага, без жира':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='бумага, не чек'))
        bot.send_message(call.message.chat.id, 'Это кассовый чек или пергамент?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'бумага, не чек':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции <b><i>(макулатура)</i></b>. Нужно удалить пружины с тетрадей, если ' +
                         'такие есть, и пройти для них тест отдельно. Бумагу нужно сложить в стопки и перевязать. ' +
                         'Или сложить в коробку и коробку перевязать. ' +
                         'Или сложить в бумажный пакет и перевязать у него ручки. ',
                         parse_mode='html')
        main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'стекло')
def glass(call):
    if call.data == 'стекло':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='стекло, не лампочка'))
        bot.send_message(call.message.chat.id, 'Это лампочка, зеркало, градусник или хрустальная посуда?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'стекло, не лампочка':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='стекло, посуда'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='стекло, не посуда'))
        bot.send_message(call.message.chat.id, 'Это стеклянная посуда?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'стекло, посуда':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='стекло, густо'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='не принимается'))
        bot.send_message(call.message.chat.id, 'Это прозрачная стеклянная посуда?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'стекло, густо':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Магазин Gusto", url='https://vk.com/charityshopgusto'))
        markup.add(types.InlineKeyboardButton("Контейнеры", url='https://tiger-sibir.ru/index.html'))
        bot.send_message(call.message.chat.id, "Принимается на акции в <i><b>стекло</b></i>, но целую посуду лучше " +
                         "сдать в Gusto, а остальную в контейнеры.",
                         parse_mode='html', reply_markup=markup)
        main_menu(call.message)
    elif call.data == 'стекло, не посуда':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Контейнеры", url='https://tiger-sibir.ru/index.html'))
        bot.send_message(call.message.chat.id,
                         "Принимается на акции в <i><b>стекло</b></i>, но лучше сдать в контейнеры.",
                         parse_mode='html',
                         reply_markup=markup)
        main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:6] == 'металл')
def metal(call):
    if call.data == 'металл':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, жесть'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, алюминий'))
        bot.send_message(call.message.chat.id, 'Металл магнитится?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, жесть':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, жесть конс'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, жесть проч'))
        bot.send_message(call.message.chat.id, 'Это консервная банка или закатывающаяся крышка от солений?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, жесть конс':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, жесть консервная'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, жесть конс смять'))
        bot.send_message(call.message.chat.id, 'Смятая?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, жесть конс смять':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Сделано", callback_data='металл, жесть консервная'))
        bot.send_message(call.message.chat.id, 'Консервную банку лучше сложить, как показано на фото.',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, жесть консервная':
        bot.send_message(call.message.chat.id, 'Принимается на акции в <i><b>Жесть консервная</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'металл, жесть проч':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, жесть сковорода'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, жесть прочая'))
        bot.send_message(call.message.chat.id, 'Это сковорода?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, жесть сковорода':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Сделано", callback_data='металл, жесть прочая'))
        bot.send_message(call.message.chat.id, 'Нужно убрать все пластиковые ручки.',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, жесть прочая':
        bot.send_message(call.message.chat.id, 'Принимается на акции в <i><b>Жесть прочая</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'металл, алюминий':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, фольга'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, алюм, не фольга'))
        bot.send_message(call.message.chat.id, 'Это фольга?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, фольга':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, алюминиевая фольга'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='не принимается'))
        bot.send_message(call.message.chat.id, 'Если смять, остаётся смятой?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, алюминиевая фольга':
        bot.send_message(call.message.chat.id, 'Принимается на акции в <i><b>Алюминиевая фольга</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'металл, алюм, не фольга':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, алюм банка'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, алюм прочий'))
        bot.send_message(call.message.chat.id, 'Это алюминиевая банка из-под напитка?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, алюм банка':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, алюминиевая банка'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, алюм банка смять'))
        bot.send_message(call.message.chat.id, 'Смятая?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, алюм банка смять':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Сделано", callback_data='металл, алюминиевая банка'))
        bot.send_message(call.message.chat.id, 'Банку лучше смять.',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, алюминиевая банка':
        bot.send_message(call.message.chat.id, 'Принимается на акции в <i><b>Алюминиевая банка</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'металл, алюм прочий':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, алюм баллон'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, алюм не баллон'))
        bot.send_message(call.message.chat.id, 'Это баллон под давлением?',
                         parse_mode='html',
                         reply_markup=markup)
    elif call.data == 'металл, алюм баллон':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Сделано", callback_data='металл, алюминий прочий'))
        bot.send_message(call.message.chat.id, 'Нужно проколоть.',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'металл, алюм не баллон':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='металл, алюм сковорода'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='металл, алюминий прочий'))
        bot.send_message(call.message.chat.id, 'Это сковорода?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'металл, алюм сковорода':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Сделано", callback_data='металл, алюминий прочий'))
        bot.send_message(call.message.chat.id, 'Нужно убрать все пластиковые ручки.',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'металл, алюминий прочий':
        bot.send_message(call.message.chat.id, 'Принимается на акции в <i><b>Алюминий прочий</b></i>.',
                         parse_mode='html')
        main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:7] == 'пластик')
def plastic(call):
    if call.data == 'пластик':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Да", callback_data='пластик, крышки енота'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='пластик, выбор марк'))
        markup.add(types.InlineKeyboardButton("Подробнее о маркировках", callback_data='маркировка' + call.data))
        bot.send_message(call.message.chat.id,
                         'Это крышка или дозатор или что-то размером с крышку (до 7 см) с маркировками 2, 4 или 5 ?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, крышки енота':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <b><i>Крышки енота</i></b>. Нужно удалить пружинки из дозаторов (' +
                         'для этого достаточно разрезать дозатор) и убрать белые вкладыши из крышек от кофейных банок.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'пластик, выбор марк':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Есть, 1 (PET)", callback_data='пластик, 1'))
        markup.add(types.InlineKeyboardButton("Есть, 2 (HDPE) или 4 (LDPE)", callback_data='пластик, 24'))
        markup.add(types.InlineKeyboardButton("Есть, 5 (PP)", callback_data='пластик, 5'))
        markup.add(types.InlineKeyboardButton("Есть, 6 (PS)", callback_data='пластик, 6'))
        markup.add(types.InlineKeyboardButton("Есть, 3 (PVC), 7 (OTHER)",
                                              callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Есть, цифра больше 7 (С/...)",
                                              callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton("Нет", callback_data='пластик, бм'))
        markup.add(types.InlineKeyboardButton("Подробнее о маркировках", callback_data='маркировка' + call.data))
        bot.send_message(call.message.chat.id,
                         'На изделии есть маркировка?',
                         parse_mode='html', reply_markup=markup)
    elif call.data[:10] == 'пластик, 1':
        plastic1(call)
    elif call.data[:11] == 'пластик, 24':
        plastic24(call)
    elif call.data[:10] == 'пластик, 5':
        plastic5(call)
    elif call.data[:10] == 'пластик, 6':
        plastic6(call)
    elif call.data.startswith('пластик, бм'):
        plastic_not_mark(call)


def plastic1(call):
    if call.data == 'пластик, 1':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 1, смять'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='не принимается'))
        bot.send_message(call.message.chat.id,
                         'Это бутылка или банка с точкой на дне?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 1, смять':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 1, сминаем'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 1, сдать'))
        bot.send_message(call.message.chat.id,
                         'Можно смять?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 1, сминаем':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Готово', callback_data='пластик, 1, сдать'))
        bot.send_message(call.message.chat.id,
                         'Нужно смять',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 1, сдать':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <i><b>1 PET</b></i>. Делится по цветам на <i>голубой, бесцветный</i>' +
                         ' и <i>прочие цвета</i>',
                         parse_mode='html')
        main_menu(call.message)


def plastic24(call):
    if call.data == 'пластик, 24':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 24, мягкий'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 24, твёрдый'))
        bot.send_message(call.message.chat.id,
                         'Это плёнка или пакет?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 24, мягкий':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 24, накл'))
        bot.send_message(call.message.chat.id,
                         'Это упаковка от заморозки?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 24, накл':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 24, удалить накл'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 24, мягкий, сдать'))
        bot.send_message(call.message.chat.id,
                         'Есть бумажные наклейки?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 24, удалить накл':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Готово', callback_data='пластик, 24, мягкий, сдать'))
        bot.send_message(call.message.chat.id,
                         'Нужно удалить все бумажные наклейки так, чтобы не осталось бумажных волокон ' +
                         '(проще будет их вырезать).',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 24, мягкий, сдать':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <i><b>Пакет с пакетами (2,4 мягкий)</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'пластик, 24, твёрдый':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 24, твёрдый, сдать'))
        bot.send_message(call.message.chat.id,
                         'Это тюбик (например от крема для рук)?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 24, твёрдый, сдать':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <i><b>2,4 твёрдый</b></i>.',
                         parse_mode='html')


def plastic5(call):
    if call.data == 'пластик, 5':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 5, накл'))
        bot.send_message(call.message.chat.id,
                         'Есть фольгированный блеск?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 5, накл':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 5, удал накл'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 5, тв/мгк'))
        bot.send_message(call.message.chat.id,
                         'Есть бумажные наклейки?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 5, удал накл':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Готово', callback_data='пластик, 5, тв/мгк'))
        bot.send_message(call.message.chat.id,
                         'Нужно удалить бумажные наклейки, чтобы не осталось волокон.',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 5, тв/мгк':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 5, мгк, сдать'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 5, тв, сдать'))
        bot.send_message(call.message.chat.id,
                         'Это плёнка или пакет?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 5, мгк, сдать':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <b><i>5 PP мягкий</i></b>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'пластик, 5, тв, сдать':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <b><i>5 PP твёрдый</i></b>.',
                         parse_mode='html')
        main_menu(call.message)


def plastic6(call):
    if call.data == 'пластик, 6':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 6, перфорация'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='не принимается'))
        bot.send_message(call.message.chat.id,
                         'Упаковка вспененная?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 6, перфорация':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='не принимается'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 6, этикетки'))
        bot.send_message(call.message.chat.id,
                         'Есть перфорация (маленькие дырочки) на дне?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 6, этикетки':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 6, удал этикетки'))
        markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, 6, вспен, сдать'))
        bot.send_message(call.message.chat.id,
                         'Есть бумажные этикетки?',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 6, удал этикетки':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Готово', callback_data='пластик, 6, вспен, сдать'))
        bot.send_message(call.message.chat.id,
                         'Нужно удалить бумажные наклейки, чтобы не осталось волокон.',
                         parse_mode='html', reply_markup=markup)
    elif call.data == 'пластик, 6, вспен, сдать':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <i><b>6 PS вcпененный</b></i>.',
                         parse_mode='html')
        main_menu(call.message)


def plastic_not_mark(call):
    if call.data == 'пластик, бм':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, бм, пакет'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, бм, не пакет'))
            bot.send_message(call.message.chat.id,
                             'Это пластиковый пакет?',
                             parse_mode='html', reply_markup=markup)
    elif call.data.startswith('пластик, бм, пакет'):
        if call.data == 'пластик, бм, пакет':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='не принимается'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, бм, пакет, чист'))
            bot.send_message(call.message.chat.id,
                             'Пакет биоразлагаемый?',
                             parse_mode='html', reply_markup=markup)
        elif call.data == 'пластик, бм, пакет, чист':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 24, накл'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='не принимается'))
            bot.send_message(call.message.chat.id,
                             'Пакет чистый?',
                             parse_mode='html', reply_markup=markup)

    elif call.data.startswith('пластик, бм, не'):
        if call.data == 'пластик, бм, не пакет':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, бм, стретч'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, бм, не стретч'))
            bot.send_message(call.message.chat.id,
                             'Это строительная стретч-плёнка?',
                             parse_mode='html', reply_markup=markup)
        elif call.data == 'пластик, бм, не стретч':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, бм, пупырка'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, бм, не пленка'))
            bot.send_message(call.message.chat.id,
                             'Это пупырчатая плёнка ("антистресс")?',
                             parse_mode='html', reply_markup=markup)
        elif call.data == 'пластик, бм, не пленка':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, 6, вспен, сдать'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='пластик, бм, не пенопласт'))
            bot.send_message(call.message.chat.id,
                             'Это пенопласт?',
                             parse_mode='html', reply_markup=markup)
        elif call.data == 'пластик, бм, не пенопласт':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Да', callback_data='пластик, бм, вспен полиэт'))
            markup.add(types.InlineKeyboardButton('Нет', callback_data='не принимается'))
            bot.send_message(call.message.chat.id,
                             'Это вспененная упаковочная плёнка?',
                             parse_mode='html', reply_markup=markup)

    elif call.data == 'пластик, бм, стретч':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <i><b>стретч-плёнка</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'пластик, бм, пупырка':
        bot.send_message(call.message.chat.id,
                         'Принимается на акции в <i><b>пупырку</b></i>.',
                         parse_mode='html')
        main_menu(call.message)
    elif call.data == 'пластик, бм, вспен полиэт':
        bot.send_message(call.message.chat.id,
                         'Скорее всего, принимается на акции в <i><b>пакет с пакетами</b></i>, ' +
                         'но лучше уточнить у волонтёров.',
                         parse_mode='html')
        main_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data[:10] == 'маркировка')
def marking(call):
    photo = open('маркировки пластика.jpeg', 'rb')
    bot.send_photo(call.message.chat.id, photo)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Вернуться обратно", callback_data=call.data[10:]))
    bot.send_message(call.message.chat.id,
                     'Маркировка на изделии - это треугольник из стрелочек, который сопровождается цифрами и/или ' +
                     'буквами. Маркировка несёт в себе информацию о материале из которого изготовлено изделие.' +
                     'Таблица маркировок пластика представлена на фото. <b>Важно!</b> Возможны различные варианты ' +
                     'сочетания цифр и букв (буквы без цифры, цифра без букв, буквы с цифрой). Но каждой цифре ' +
                     'могут соответствовать только аббревиатуры, написанные под ней в таблице.',
                     parse_mode='html', reply_markup=markup)


# @bot.message_handler(content_types=['text'])
# def get_user_text(message):
#     if message.text == 'photo':
#         photo = open('Untitled.png', 'rb')
#         bot.send_photo(message.chat.id, photo)

# @bot.message_handler(content_types=['photo'])
# def photo_react(message):
#     bot.send_message(message.chat.id, "Вау, крутое фото!", parse_mode='html')


# сообщение, что на акции это не принимается
@bot.callback_query_handler(func=lambda call: call.data == 'не принимается')
def not_accepted(call):
    bot.send_message(call.message.chat.id, '<b><i>Не принимается на акции</i></b>', parse_mode='html')
    main_menu(call.message)


# сообщение, что на акции это не принимается, но можно сдать в экоцентре
@bot.callback_query_handler(func=lambda call: call.data == 'экоцентр')
def prozero(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти в группу экоцентра ProZero", url=prozero_url_tg))
    markup.add(types.InlineKeyboardButton('Начать сортировку сначала', callback_data='начало сортировки'))
    bot.send_message(call.message.chat.id, prozero_text, parse_mode='html', reply_markup=markup)


# обработка различных текстовых сообщений
@bot.message_handler(content_types=['text'])
def group_link(message):
    greetings = ('Привет!', 'Привет', 'привет', 'привет!', 'Привет.', 'привет.',
                 'Здравствуй!', 'Здравствуй', 'Здравствуй.', 'здравствуй!', 'здравствуй', 'здравствуй.',
                 'Здравствуйте!', 'Здравствуйте', 'Здравствуйте.', 'здравствуйте!', 'здравствуйте', 'здравствуйте.')
    if message.text in greetings:
        start_func(message)
    elif message.text == "Перейти в группу зелёной белки":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти в группу зелёной белки ТГ", url=greenbelka_url_tg))
        markup.add(types.InlineKeyboardButton("Перейти в группу зелёной белки ВК", url=greenbelka_url_vk))
        bot.send_message(message.chat.id, 'Ты можешь перейти в группы по одной из следующих ссылок', parse_mode='html',
                         reply_markup=markup)
    elif message.text == "Маркировки":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Маркировки пластика", callback_data='маркировки'))
        # markup.add(types.InlineKeyboardButton("Остальные маркировки", callback_data='маркировки проч'))
        bot.send_message(message.chat.id, 'Подробнее о маркировках здесь', parse_mode='html',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю, попробуй изменить свой запрос", parse_mode='html')


bot.polling(none_stop=True)  # чтобы бот работал постоянно
