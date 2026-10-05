import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

# Настройки страницы и темы Winter Arc
st.set_page_config(
    page_title="Winter Arc Dashboard 2026",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомный CSS для темной неоновой темы Winter Arc
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #58a6ff;
    }
    .discipline-high { color: #238636; font-size: 28px; font-weight: bold; }
    .discipline-warn { color: #d29922; font-size: 28px; font-weight: bold; }
    .discipline-low { color: #f85149; font-size: 28px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

DB_FILE = "winter_arc_data.json"

# Инициализация базы данных
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"days": {}, "weekly_notes": {}}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# Расчет дат челленджа
START_DATE = date(2026, 10, 5)
END_DATE = date(2026, 12, 31)
today = date.today()

# Корректировка для отображения в рамках дат
today_str = today.strftime("%Y-%m-%d")
total_days = (END_DATE - START_DATE).days + 1
days_passed = (today - START_DATE).days

if days_passed < 0:
    days_passed = 0
elif days_passed > total_days:
    days_passed = total_days

days_left = total_days - days_passed
progress_pct = min(100, int((days_passed / total_days) * 100))

# --- БОКОВАЯ ПАНЕЛЬ (Статистика Арки) ---
st.sidebar.title("❄️ WINTER ARC 2026")
st.sidebar.write("⚡ *Дисциплина. Фокус. Результат.*")
st.sidebar.markdown("---")

st.sidebar.subheader("Прогресс Челленджа")
st.sidebar.progress(progress_pct / 100)
st.sidebar.write(f"Пройдено: **{days_passed}** из **{total_days}** дней ({progress_pct}%)")
st.sidebar.write(f"Осталось: **{days_left}** дней")

# Инициализация сегодняшнего дня, если его нет в базе
if today_str not in data["days"]:
    data["days"][today_str] = {
        "instagram_detox": False,
        "sweet_moderation": False,
        "steps": 0,
        "reading_pages": 0,
        "spanish": False,
        "python_course": False,
        "competence_30min": False
    }

# --- ГЛАВНЫЙ ЭКРАН ---
st.title("Личный Дашборд Эффективности")
st.write(f"📆 Сегодня: **{today.strftime('%d.%m.%Y')}**")

# Расчет дисциплины за сегодня
today_habits = data["days"][today_str]
total_habits_count = 7
missed_count = 0

if not today_habits["instagram_detox"]: missed_count += 1
if not today_habits["sweet_moderation"]: missed_count += 1
if today_habits["steps"] < 10000: missed_count += 1
if today_habits["reading_pages"] == 0: missed_count += 1
if not today_habits["spanish"]: missed_count += 1
if not today_habits["python_course"]: missed_count += 1
if not today_habits["competence_30min"]: missed_count += 1

discipline_score = max(0, 100 - (missed_count * 5))

# Виджеты верхнего уровня
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Шкала Дисциплины (Сегодня)")
    if discipline_score >= 80:
        st.markdown(f'<span class="discipline-high">{discipline_score} / 100 🔥</span>', unsafe_allow_html=True)
        st.caption("Отличный темп! Держи планку выше 80!")
    elif discipline_score >= 60:
        st.markdown(f'<span class="discipline-warn">{discipline_score} / 100 ⚠️</span>', unsafe_allow_html=True)
        st.caption("Внимание! Дисциплина проседает.")
    else:
        st.markdown(f'<span class="discipline-low">{discipline_score} / 100 🚨</span>', unsafe_allow_html=True)
        st.caption("Срочно вернись в строй!")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Глобальный фокус")
    st.markdown('<span class="metric-value">🚀 Стать крутым РОПом / Менеджером по продажам</span>', unsafe_allow_html=True)
    st.caption("Каждое действие сегодня приближает тебя к этой цели.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 📥 Ввод достижений за сегодня")

tab1, tab2, tab3 = st.tabs(["📋 Ежедневные привычки", "💼 Проф. развитие", "📝 Итоги недели"])

with tab1:
    st.subheader("Физическое и ментальное состояние")
    inst = st.checkbox("📵 Цифровой детокс (Без Instagram)", value=today_habits["instagram_detox"])
    sweet = st.checkbox("🍏 Умеренное употребление сладкого", value=today_habits["sweet_moderation"])
    steps = st.number_input("👟 Шаги (Цель: 10 000)", min_value=0, max_value=100000, value=int(today_habits["steps"]), step=500)
    pages = st.number_input("📚 Чтение книг (Количество страниц)", min_value=0, max_value=500, value=int(today_habits["reading_pages"]), step=1)
    spanish = st.checkbox("🇪🇸 Испанский язык (Минимум 15-20 минут)", value=today_habits["spanish"])

with tab2:
    st.subheader("Прокачка жестких и мягких навыков")
    python = st.checkbox("🐍 Обучение: Курс «Поколение Python»", value=today_habits["python_course"])
    comp = st.checkbox("📈 Правило 30 минут: «Сегодня я стал компетентнее на 30 минут в продажах»", value=today_habits["competence_30min"])

# Получение текущей недели года для архива
current_week = f"Неделя {today.isocalendar()[1]} ({today.strftime('%b %Y')})"

with tab3:
    st.subheader("Архив качественных изменений")
    saved_note = data["weekly_notes"].get(current_week, "")
    weekly_note = st.text_area(f"Итоги недели / Главная победа ({current_week}):", value=saved_note, placeholder="Например: Прошел тему со списками в Python, закрыл крупного клиента...")

# Сохранение изменений
if st.button("💾 Сохранить все данные", type="primary"):
    data["days"][today_str] = {
        "instagram_detox": inst,
        "sweet_moderation": sweet,
        "steps": steps,
        "reading_pages": pages,
        "spanish": spanish,
        "python_course": python,
        "competence_30min": comp
    }
    data["weekly_notes"][current_week] = weekly_note
    save_data(data)
    st.success("Данные успешно сохранены! Шкала дисциплины обновлена.")
    st.rerun()

# --- АНАЛИТИКА И ИСТОРИЯ ---
st.markdown("---")
st.markdown("### 📊 Аналитика и История")

if data["days"]:
    # Подготовка данных для графика
    history_list = []
    for d_str, habits in data["days"].items():
        m_count = 0
        if not habits.get("instagram_detox", False): m_count += 1
        if not habits.get("sweet_moderation", False): m_count += 1
        if habits.get("steps", 0) < 10000: m_count += 1
        if habits.get("reading_pages", 0) == 0: m_count += 1
        if not habits.get("spanish", False): m_count += 1
        if not habits.get("python_course", False): m_count += 1
        if not habits.get("competence_30min", False): m_count += 1
        score = max(0, 100 - (m_count * 5))
        history_list.append({"Дата": d_str, "Рейтинг Дисциплины": score})
    
    df = pd.DataFrame(history_list).sort_values(by="Дата")
    
    col_chart, col_notes = st.columns(2)
    with col_chart:
        st.write("📈 Динамика твоей дисциплины по дням:")
        st.line_chart(df.set_index("Дата"))
    
    with col_notes:
        st.write("🗄️ Сохраненные итоги недель:")
        for w, note in data["weekly_notes"].items():
            if note.strip():
                st.info(f"**{w}**:\n{note}")
else:
    st.info("Здесь будет отображаться график, когда появится история за несколько дней.")
