import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- НАСТРОЙКИ ---
st.set_page_config(page_title="Аудит Маркетинга", layout="wide")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, 'marketing_data.csv')

st.title("📊 Авто-аудит: Контроль вашего маркетинга")

# --- ЗАГРУЗКА ---
if not os.path.exists(data_path):
    st.error(f"Файл данных не найден по пути: {data_path}")
    st.stop()

#df = pd.read_csv(data_path)
sheet_url = "https://docs.google.com/spreadsheets/d/1PiqXsG8lGjsU1aqWWUdqYkI90uCtTsYQlg6bfc8-_YU/edit?usp=sharing"
# Берем всё, что идет до /edit, и добавляем команду экспорта
csv_url = sheet_url.split('/edit')[0] + '/export?format=csv'

df = pd.read_csv(csv_url)

# Преобразуем дату
df['Дата'] = pd.to_datetime(df['Дата'])
last_date = df['Дата'].max()
day_df = df[df['Дата'] == last_date]

# --- АНАЛИТИКА (АЛЕРТЫ) ---
def get_alerts(df_day):
    alerts = []
    for _, row in df_day.iterrows():
        # Условие: Слив бюджета без лидов
        if row['Бюджет'] > 30 and row['Лиды'] == 0:
            alerts.append(f"🚨 **Критический слив!** Кампания '{row['Кампания']}' потратила {row['Бюджет']}$ и не принесла ни одного лида.")
        # Условие: ROI ниже -50%
        elif row['ROI'] < -50:
            alerts.append(f"⚠️ **Низкий ROI!** Кампания '{row['Кампания']}' имеет ROI {row['ROI']}% (Бюджет: {row['Бюджет']}$, Выручка: {row['Выручка']}$).")
    return alerts

# --- ИНТЕРФЕЙС ---
# Метрики
col1, col2, col3, col4 = st.columns(4)
col1.metric("Дата", last_date.strftime('%d.%m.%Y'))
col2.metric("Общий бюджет", f"{day_df['Бюджет'].sum():.0f} $")
col3.metric("Всего лидов", int(day_df['Лиды'].sum()))
col4.metric("ROI в среднем", f"{day_df['ROI'].mean():.1f}%")

st.divider()

# Алерты
st.subheader("🕵️ Отчет аудитора")
alerts = get_alerts(day_df)
if not alerts:
    st.success("✅ Всё в порядке. Маркетинг работает эффективно!")
else:
    for alert in alerts:
        st.warning(alert)

# Графики
c1, c2 = st.columns(2)
with c1:
    fig_roi = px.bar(day_df, x='Кампания', y='ROI', color='ROI', 
                     title="ROI по кампаниям",
                     color_continuous_scale=['red', 'yellow', 'green'])
    st.plotly_chart(fig_roi, use_container_width=True)

with c2:
    fig_spend = px.scatter(day_df, x='Бюджет', y='Выручка', size='Лиды', 
                           title="Эффективность: Бюджет vs Выручка",
                           hover_name='Кампания')
    st.plotly_chart(fig_spend, use_container_width=True)

with st.expander("Подробная таблица данных"):
    st.dataframe(df.sort_values(by='Дата', ascending=False))