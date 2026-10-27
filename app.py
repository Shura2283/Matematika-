Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import streamlit as st
import random

# Sahifa sozlamalari
st.set_page_config(page_title="Matematika Trenajori", page_icon="🧮", layout="centered")

st.title("🧮 Matematika Trenajori")
st.write("Bilimingizni sinab ko'ring va hisoblash tezligingizni oshiring!")

# Dastur xotirasi (Session State) - ballar va savollarni saqlash uchun
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(1, 20)
    st.session_state.num2 = random.randint(1, 20)
    st.session_state.operation = random.choice(["+", "-", "*"])
    st.session_state.score = 0
    st.session_state.total = 0

# Yangi savol generatsiya qilish funksiyasi
def yangi_savol():
    st.session_state.num1 = random.randint(1, 20)
    st.session_state.num2 = random.randint(1, 20)
    st.session_state.operation = random.choice(["+", "-", "*"])

# Natijani hisoblash
n1 = st.session_state.num1
n2 = st.session_state.num2
op = st.session_state.operation

if op == "+":
    togri_javob = n1 + n2
elif op == "-":
    togri_javob = n1 - n2
else:
...     togri_javob = n1 * n2
... 
... # Statistika paneli
... col1, col2 = st.columns(2)
... col1.metric("To'g'ri javoblar", f"{st.session_state.score}")
... col2.metric("Jami savollar", f"{st.session_state.total}")
... 
... st.markdown("---")
... 
... # Savol maydoni
... st.subheader(f"Misolni yeching:  **{n1} {op} {n2} = ?**")
... 
... # Foydalanuvchi javob kiritadigan forma
... with st.form("javob_formasi", clear_on_submit=True):
...     foydalanuvchi_javobi = st.number_input("Javobingizni kiriting:", step=1, value=None, placeholder="Son kiriting...")
...     yuborish = st.form_submit_button("Tekshirish")
... 
...     if yuborish:
...         if foydalanuvchi_javobi is not None:
...             st.session_state.total += 1
...             if int(foydalanuvchi_javobi) == togri_javob:
...                 st.session_state.score += 1
...                 st.success(f"To'g'ri! Barakalla 🎉 ({n1} {op} {n2} = {togri_javob})")
...             else:
...                 st.error(f"Noto'g'ri! To'g'ri javob: {togri_javob} edi ❌")
...             
...             # Yangi savolga o'tish
...             yangi_savol()
...             st.rerun()
...         else:
...             st.warning("Iltimos, avval javobni yozing!")
... 
... # O'yinni qayta boshlash tugmasi
... if st.button("Hisobni nolga tushirish (Qayta boshlash)"):
...     st.session_state.score = 0
...     st.session_state.total = 0
...     yangi_savol()
