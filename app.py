import streamlit as st
import random
import pandas as pd
from io import BytesIO
from datetime import datetime

# Sahifa sozlamalari
st.set_page_config(page_title="Matematika Trenajori", page_icon="🧮", layout="centered")

# Qora fon va mos dizayn uchun CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        header {visibility: hidden;}
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            color: #FFFFFF !important;
            background-color: #262730 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Holatlarni (session_state) boshlang'ich sozlash
if "step" not in st.session_state:
    st.session_state.step = "login"  # "login" -> "test" -> "result"
    st.session_state.student_name = ""
    st.session_state.student_class = ""
    st.session_state.chosen_op = "Aralash (+, -, *, /)"
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.last_result = None

# Savol tuzish funksiyasi
def yangi_savol():
    tanlov = st.session_state.chosen_op
    
    if tanlov == "Qo'shish (+)":
        op = "+"
    elif tanlov == "Ayirish (-)":
        op = "-"
    elif tanlov == "Ko'paytirish (*)":
        op = "*"
    elif tanlov == "Bo'lish (/)":
        op = "/"
    else:
        op = random.choice(["+", "-", "*", "/"])
        
    # Bo'lish amali butun son chiqishi uchun maxsus mantiq
    if op == "/":
        boluvchi = random.randint(2, 10)
        bolinma = random.randint(1, 12)
        bolinuvchi = boluvchi * bolinma
        st.session_state.num1 = bolinuvchi
        st.session_state.num2 = boluvchi
    elif op == "*":
        st.session_state.num1 = random.randint(2, 10)
        st.session_state.num2 = random.randint(2, 10)
    elif op == "-":
        a = random.randint(5, 50)
        b = random.randint(1, 50)
        st.session_state.num1 = max(a, b)
        st.session_state.num2 = min(a, b)
    else:  # "+"
        st.session_state.num1 = random.randint(5, 50)
        st.session_state.num2 = random.randint(5, 50)
        
    st.session_state.operation = op

# ================= 1-BOSQICH: MA'LUMOT VA AMALNI TANLASH =================
if st.session_state.step == "login":
    st.title("🧮 Matematika Trenajori")
    st.subheader("Testni boshlashdan oldin ma'lumotlarni kiriting:")

    with st.form("login_form"):
        ism_familiya = st.text_input("Familiya va Ismingiz:", placeholder="Masalan: Karimov Ali")
        sinf = st.text_input("Sinfingiz:", placeholder="Masalan: 5-A")
        
        amal_tanlovi = st.selectbox(
            "Mashq qilish uchun amal turini tanlang:",
            [
                "Aralash (+, -, *, /)",
                "Qo'shish (+)",
                "Ayirish (-)",
                "Ko'paytirish (*)",
                "Bo'lish (/)"
            ]
        )
        
        boshlash = st.form_submit_button("Testni boshlash 🚀")

        if boshlash:
            if ism_familiya.strip() and sinf.strip():
                st.session_state.student_name = ism_familiya.strip()
                st.session_state.student_class = sinf.strip()
                st.session_state.chosen_op = amal_tanlovi
                st.session_state.step = "test"
                yangi_savol()
                st.rerun()
            else:
                st.error("Iltimos, ism-familiyangiz va sinfingizni to'liq kiriting!")

# ================= 2-BOSQICH: 25 TA MISOL TESTI =================
elif st.session_state.step == "test":
    st.subheader(f"O'quvchi: {st.session_state.student_name} | Sinf: {st.session_state.student_class}")
    st.caption(f"Tanlangan bo'lim: **{st.session_state.chosen_op}**")
    
    n1 = st.session_state.num1
    n2 = st.session_state.num2
    op = st.session_state.operation

    if op == "+":
        togri_javob = n1 + n2
    elif op == "-":
        togri_javob = n1 - n2
    elif op == "*":
        togri_javob = n1 * n2
    else:
        togri_javob = n1 // n2

    col1, col2 = st.columns(2)
    col1.metric("Misol raqami", f"{st.session_state.total + 1} / 25")
    col2.metric("Joriy to'g'ri javoblar", f"{st.session_state.score}")

    st.markdown("---")

    if st.session_state.last_result:
        status, msg = st.session_state.last_result
        if status == "success":
            st.success(msg)
        else:
            st.error(msg)

    # Belgini chiroyli ko'rsatish
    display_op = "÷" if op == "/" else ("×" if op == "*" else op)
    st.subheader(f"Misolni yeching: **{n1} {display_op} {n2} = ?**")

    with st.form("test_form", clear_on_submit=True):
        foydalanuvchi_javobi = st.number_input("Javobingiz:", step=1, value=None, placeholder="Son kiriting...")
        yuborish = st.form_submit_button("Tasdiqlash")

        if yuborish:
            if foydalanuvchi_javobi is not None:
                st.session_state.total += 1
                if int(foydalanuvchi_javobi) == togri_javob:
                    st.session_state.score += 1
                    st.session_state.last_result = ("success", f"To'g'ri! 🎉 ({n1} {display_op} {n2} = {togri_javob})")
                else:
                    st.session_state.last_result = ("error", f"Noto'g'ri! ❌ To'g'ri javob: {togri_javob} edi")

                if st.session_state.total >= 25:
                    st.session_state.step = "result"
                else:
                    yangi_savol()
                st.rerun()
            else:
                st.warning("Iltimos, avval javobni yozing!")

# ================= 3-BOSQICH: NATIJA VA EXCEL YUKLASH =================
elif st.session_state.step == "result":
    togri = st.session_state.score
    xato = 25 - togri
    ball = togri * 4

    st.balloons()
    st.success("🎉 **Test muvaffaqiyatli yakunlandi!**")
    
    st.write(f"**O'quvchi:** {st.session_state.student_name}")
    st.write(f"**Sinf:** {st.session_state.student_class}")
    st.write(f"**Yo'nalish:** {st.session_state.chosen_op}")

    col1, col2, col3 = st.columns(3)
    col1.metric("To'g'ri", f"{togri} ta")
    col2.metric("Xato", f"{xato} ta")
    col3.metric("To'plangan ball", f"{ball} / 100")

    hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
    natija_data = {
        "Familiya va Ism": [st.session_state.student_name],
        "Sinf": [st.session_state.student_class],
        "Amal turi": [st.session_state.chosen_op],
        "To'g'ri javoblar": [togri],
        "Xato javoblar": [xato],
        "To'plangan ball": [ball],
        "Maksimal ball": [100],
        "Sana va vaqt": [hozirgi_vaqt]
    }
    df = pd.DataFrame(natija_data)

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Natijalar')
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="📥 Natijani Excel (.xlsx) formatida yuklab olish",
        data=excel_data,
        file_name=f"{st.session_state.student_name}_natija.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")
    if st.button("Boshqa o'quvchi uchun qayta boshlash 🔄"):
        st.session_state.step = "login"
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.last_result = None
        st.rerun()
