import streamlit as st
import pandas as pd
import os

st.title("Тест запуска")
st.write("Скрипт успешно запустился!")

# Проверяем наличие файла
file_name = 'marketing_data.csv'
if os.path.exists(file_name):
    st.success(f"Файл {file_name} найден!")
    df = pd.read_csv(file_name)
    st.dataframe(df.head())
else:
    st.error(f"ОШИБКА: Файл {file_name} не найден!")
    st.write(f"Текущая папка: {os.getcwd()}")
    st.write("Список файлов в папке:")
    st.write(os.listdir('.'))