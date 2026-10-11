import random
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# Вставьте сюда токен вашего бота, полученный от @BotFather
BOT_TOKEN = "8802040946:AAEL_6ypupLJEgCfQgWXfQNTXdWUcDkhHDk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class QuizState(StatesGroup):
    waiting_for_answer = State()

# Выверенная база данных орфоэпического минимума ФИПИ
ORTHOEPY_DATABASE = [
    {"correct": "агЕнт", "incorrects": ["Агент"]},
    {"correct": "алфавИт", "incorrects": ["Алфавит"]},
    {"correct": "аэропОрты", "incorrects": ["аэропортЫ"]},
    {"correct": "бАнты", "incorrects": ["бантЫ"]},
    {"correct": "бОроду", "incorrects": ["бородУ"]},
    {"correct": "брАла", "incorrects": ["бралА"]},
    {"correct": "бралАсь", "incorrects": ["брАлась"]},
    {"correct": "бухгАлтеров", "incorrects": ["бухгалтерОв"]},
    {"correct": "вернА", "incorrects": ["вЕрна"]},
    {"correct": "взялА", "incorrects": ["взЯла"]},
    {"correct": "взялАсь", "incorrects": ["взЯлась"]},
    {"correct": "включЁн", "incorrects": ["вклЮчен"]},
    {"correct": "включЁнный", "incorrects": ["вклЮченный"]},
    {"correct": "включИт", "incorrects": ["вклЮчит"]},
    {"correct": "включИшь", "incorrects": ["вклЮчишь"]},
    {"correct": "влилАсь", "incorrects": ["влИлась"]},
    {"correct": "ворвалАсь", "incorrects": ["ворвАлась"]},
    {"correct": "воспринялА", "incorrects": ["воспрИняла"]},
    {"correct": "воссоздалА", "incorrects": ["воссоздАла"]},
    {"correct": "вручИт", "incorrects": ["врУчит"]},
    {"correct": "гналА", "incorrects": ["гнАла"]},
    {"correct": "гналАсь", "incorrects": ["гнАлась"]},
    {"correct": "дефИс", "incorrects": ["дЕфис"]},
    {"correct": "диспансЕр", "incorrects": ["диспансер"]},
    {"correct": "затЕмно", "incorrects": ["затемнО"]},
    {"correct": "звалА", "incorrects": ["звАла"]},
    {"correct": "звонИм", "incorrects": ["звОним"]},
    {"correct": "звонИт", "incorrects": ["звОнит"]},
    {"correct": "звонИшь", "incorrects": ["звОнишь"]},
    {"correct": "знАчимый", "incorrects": ["значИмый"]},
    {"correct": "Иксы", "incorrects": ["иксЫ"]},
    {"correct": "исчЕрпав", "incorrects": ["исчерпАв"]},
    {"correct": "исчЕрпать", "incorrects": ["исчерпАть"]},
    {"correct": "каталОг", "incorrects": ["катАлог"]},
    {"correct": "квартАл", "incorrects": ["квАртал"]},
    {"correct": "киломЕтр", "incorrects": ["килОметр"]},
    {"correct": "клАла", "incorrects": ["клалА"]},
    {"correct": "клЕить", "incorrects": ["клеИть"]},
    {"correct": "кОнусы", "incorrects": ["конусЫ"]},
    {"correct": "кормЯщий", "incorrects": ["кОрмящий"]},
    {"correct": "корЫсть", "incorrects": ["кОрысть"]},
    {"correct": "крАны", "incorrects": ["кранЫ"]},
    {"correct": "красИвее", "incorrects": ["красивЕе"]},
    {"correct": "красИвейший", "incorrects": ["красивЕйший"]},
    {"correct": "кремЕнь", "incorrects": ["крЕмень"]},
    {"correct": "кремнЯ", "incorrects": ["крЕмня"]},
    {"correct": "кровоточИть", "incorrects": ["кровотОчить"]},
    {"correct": "кУхонный", "incorrects": ["кухОнный"]},
    {"correct": "лгалА", "incorrects": ["лгАла"]},
    {"correct": "лЕктор", "incorrects": ["лектОр"]},
    {"correct": "лилА", "incorrects": ["лИла"]},
    {"correct": "нЕнависть", "incorrects": ["ненавИсть"]},
    {"correct": "ненадОлго", "incorrects": ["ненадОлгово"]},
    {"correct": "низведЁнный", "incorrects": ["низвЕденный"]},
    {"correct": "нОвости", "incorrects": ["новОсти"]},
    {"correct": "новостЕй", "incorrects": ["нОвостей"]},
    {"correct": "нОгтя", "incorrects": ["ногтЯ"]},
    {"correct": "обеспЕчение", "incorrects": ["обеспеченИе"]},
    {"correct": "обзвонИт", "incorrects": ["обзвОнит"]},
    {"correct": "облегчИт", "incorrects": ["облЕгчить"]},
    {"correct": "облилАсь", "incorrects": ["облИлась"]},
    {"correct": "обнялАсь", "incorrects": ["обнЯлась"]},
    {"correct": "обогналА", "incorrects": ["обогнАла"]},
    {"correct": "ободралА", "incorrects": ["ободрАла"]},
    {"correct": "ободрИть", "incorrects": ["обОдрить"]},
    {"correct": "ободрЁнный", "incorrects": ["обОдренный"]},
    {"correct": "ободрЁн", "incorrects": ["обОдрен"]},
    {"correct": "ободренА", "incorrects": ["обОдрена"]},
    {"correct": "обострЁнный", "incorrects": ["обОстренный"]},
    {"correct": "обострИть", "incorrects": ["обОстрить"]},
    {"correct": "одолжИт", "incorrects": ["одОлжит"]},
    {"correct": "озлобИть", "incorrects": ["озлОбить"]},
    {"correct": "оклейИть", "incorrects": ["оклЕить"]},
    {"correct": "окружИт", "incorrects": ["окрУжит"]},
    {"correct": "опломбировАть", "incorrects": ["опломбИровать"]},
    {"correct": "опОшлят", "incorrects": ["опошлЯт"]},
    {"correct": "определЁн", "incorrects": ["опредЕлен"]},
    {"correct": "оптОвый", "incorrects": ["Оптовый"]},
    {"correct": "освЕдомиться", "incorrects": ["осведомИться"]},
    {"correct": "отбылА", "incorrects": ["Отбыла"]},
    {"correct": "отдалА", "incorrects": ["Отдала"]},
    {"correct": "отдАв", "incorrects": ["отдáв"]},
    {"correct": "отключЁнный", "incorrects": ["отклЮченный"]},
    {"correct": "откУпорил", "incorrects": ["откупорИл"]},
    {"correct": "отозвалА", "incorrects": ["отозвАла"]},
    {"correct": "Отрочество", "incorrects": ["отрочЕство"]},
    {"correct": "рвалА", "incorrects": ["рвАла"]},
    {"correct": "свЁкла", "incorrects": ["свеклА"]},
    {"correct": "сверлИт", "incorrects": ["свЕрлит"]},
    {"correct": "серА", "incorrects": ["сЕра"]},
    {"correct": "сирОты", "incorrects": ["сиротЫ"]},
    {"correct": "слИвовый", "incorrects": ["сливОвый"]},
    {"correct": "снялА", "incorrects": ["снЯла"]},
    {"correct": "создалА", "incorrects": ["создАла"]},
    {"correct": "сОздана", "incorrects": ["создАна"]},
    {"correct": "созданА", "incorrects": ["создАна"]},
    {"correct": "срЕдства", "incorrects": ["средствА"]},
    {"correct": "стАтуя", "incorrects": ["статуЯ"]},
    {"correct": "столЯр", "incorrects": ["стОляр"]},
    {"correct": "стройнА", "incorrects": ["стрОйна"]},
    {"correct": "тОрты", "incorrects": ["тортЫ"]},
    {"correct": "тОтчас", "incorrects": ["тотчАс"]},
    {"correct": "убралА", "incorrects": ["Убрала"]},
    {"correct": "углубИть", "incorrects": ["углУбить"]},
    {"correct": "укрепИт", "incorrects": ["укрЕпит"]},
    {"correct": "цемЕнт", "incorrects": ["цЕмент"]},
    {"correct": "цЕнтнер", "incorrects": ["центнЕр"]},
    {"correct": "чЕлюстей", "incorrects": ["челюстЕй"]},
    {"correct": "чЕрпать", "incorrects": ["черпАть"]}
]

def generate_task():
    """Генерирует Задание 4: 5 слов, от 2 до 4 правильных."""
    selected = random.sample(ORTHOEPY_DATABASE, 5)
    num_correct = random.randint(2, 4)
    correct_indices = set(random.sample(range(5), num_correct))
    
    task_lines = []
    answer_keys = []
    
    for idx, item in enumerate(selected):
        line_num = idx + 1
        if idx in correct_indices:
            task_lines.append(f"<b>{line_num})</b> {item['correct']}")
            answer_keys.append(str(line_num))
        else:
            fake_word = random.choice(item['incorrects'])
            task_lines.append(f"<b>{line_num})</b> {fake_word}")
            
    correct_answer = "".join(sorted(answer_keys))
    return task_lines, correct_answer

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="📝 Решать Задание 4")
    kb.adjust(1)
    
    await message.answer(
        "👋 Привет! Это бот-тренажер для подготовки к **Заданию 4 ЕГЭ по русскому языку** (орфоэпия).\n\n"
        "Нажми кнопку ниже, чтобы начать тренировку!",
        reply_markup=kb.as_markup(resize_keyboard=True),
        parse_mode="HTML"
    )

@dp.message(F.text == "📝 Решать Задание 4")
@dp.message(Command("next"))
async def send_new_task(message: types.Message, state: FSMContext):
    task_lines, correct_answer = generate_task()
    
    await state.update_data(correct_answer=correct_answer)
    await state.set_state(QuizState.waiting_for_answer)
    
    text = (
        "📌 <b>Задание 4. Укажите варианты ответов, в которых ВЕРНО выделена буква, "
        "обозначающая ударный гласный звук. Запишите номера этих ответов.</b>\n\n"
        + "\n".join(task_lines) +
        "\n\n✍️ <i>Отправьте цифры в чат (например: 134)</i>"
    )
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Пропустить / Следующее", callback_data="skip_task")
    
    await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "skip_task")
async def skip_task_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await send_new_task(callback.message, state)

@dp.message(QuizState.waiting_for_answer)
async def check_user_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    correct_answer = user_data.get("correct_answer")
    
    user_input = "".join(sorted(c for c in message.text if c.isdigit()))
    
    kb = ReplyKeyboardBuilder()
    kb.button(text="📝 Решать Задание 4")
    kb.adjust(1)
    
    if user_input == correct_answer:
        await message.answer(
            f"✅ <b>Верно! Отличная работа!</b>\nПравильный ответ: <b>{correct_answer}</b>",
            reply_markup=kb.as_markup(resize_keyboard=True),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"❌ <b>Неверно.</b>\nВаш ответ: {user_input or '—'}\nПравильный ответ: <b>{correct_answer}</b>",
            reply_markup=kb.as_markup(resize_keyboard=True),
            parse_mode="HTML"
        )
    
    await state.clear()

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())