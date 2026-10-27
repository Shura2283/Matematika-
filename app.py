import streamlit as st
import random
import pandas as pd
from io import BytesIO
from datetime import datetime

# Sahifa sozlamalari
st.set_page_config(page_title="Matematika Trenajori", page_icon="🧮", layout="centered")

# Ko'k, yashil, sariq va qizil ranglar aralashmasi (gradient fon) va aniq jadvallar dizayni
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d324d 0%, #1e5239 30%, #7d6b14 70%, #5e1914 100%);
            background-attachment: fixed;
            color: #FFFFFF;
        }
        header {visibility: hidden;}
        
        /* Matnlar va jadvallar aniq ko'rinishi uchun shaffof bloklar */
        div[data-testid="stForm"], div[data-testid="stMetric"], .author-card, .result-card {
            background-color: rgba(15, 23, 42, 0.78) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 14px !important;
            padding: 16px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45) !important;
        }
        
        /* Metric bloklar ichidagi yozuvlar */
        div[data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #CBD5E1 !important;
            font-size: 1rem !important;
        }
        
        /* Inputlar (kiritish maydonlari) */
        .stTextInput input, .stNumberInput input {
            color: #FFFFFF !important;
            background-color: rgba(30, 41, 59, 0.9) !important;
            border: 1px solid #64748B !important;
            border-radius: 8px !important;
        }
        
        /* Muallif yozuvi uslubi */
        .author-badge {
            display: inline-block;
            background: rgba(0, 0, 0, 0.55);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.95rem;
            color: #F1F5F9;
            border: 1px solid rgba(255, 255, 255, 0.25);
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Holatlarni (session_state) boshlang'ich sozlash
if "step" not in st.session_state:
    st.session_state.step = "login"
    st.session_state.student_name = ""
    st.session_state.student_class = ""
    st.session_state.chosen_op = "Aralash (+, -, *, /)"
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.last_result = None

# Savol generatsiya qilish
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
        
    if op == "/":
        boluvchi = random.randint(2, 10)
        bolinma = random.randint(1, 12)
        st.session_state.num1 = boluvchi * bolinma
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

# ================= 1-BOSQICH: MA'LUMOT VA AMAL TANLASH =================
if st.session_state.step == "login":
    st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
    st.title("🧮 Matematika Trenajori")
    st.write("Testni boshlashdan oldin ma'lumotlaringizni to'ldiring:")

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

# ================= 2-BOSQICH: TEST JARAYONI =================
elif st.session_state.step == "test":
    st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
    st.subheader(f"👤 O'quvchi: {st.session_state.student_name} | Sinf: {st.session_state.student_class}")
    st.caption(f"Amal turi: **{st.session_state.chosen_op}**")
    
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

    # Aniq jadval ko'rinishidagi statistika
    col1, col2 = st.columns(2)
    col1.metric("Misol tartibi", f"{st.session_state.total + 1} / 25")
    col2.metric("To'g'ri javoblar", f"{st.session_state.score} ta")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.last_result:
        status, msg = st.session_state.last_result
        if status == "success":
            st.success(msg)
        else:
            st.error(msg)

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

# ================= 3-BOSQICH: NATIJA VA EXCEL JADVALI =================
elif st.session_state.step == "result":
    togri = st.session_state.score
    xato = 25 - togri
    ball = togri * 4

    st.balloons()
    st.success("🎉 **Test muvaffaqiyatli yakunlandi!**")
    
    st.markdown(f"""
        <div class="author-card" style="margin-bottom: 20px;">
            <h3>📊 Natijalar xulosasi</h3>
            <p><b>O'quvchi:</b> {st.session_state.student_name}</p>
            <p><b>Sinf:</b> {st.session_state.student_class}</p>
            <p><b>Yo'nalish:</b> {st.session_state.chosen_op}</p>
            <p><b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("To'g'ri", f"{togri} ta")
    col2.metric("Xato", f"{xato} ta")
    col3.metric("To'plangan ball", f"{ball} / 100")

    st.markdown("<br>", unsafe_allow_html=True)

    hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
    natija_data = {
        "Familiya va Ism": [st.session_state.student_name],
        "Sinf": [st.session_state.student_class],
        "Amal turi": [st.session_state.chosen_op],
        "To'g'ri javoblar": [togri],
        "Xato javoblar": [xato],
        "To'plangan ball": [ball],
        "Maksimal ball": [100],
        "Sana va vaqt": [hozirgi_vaqt],
        "Tuzuvchi": ["Quljanova Shukurjon Zaribovna"]
    }
    df = pd.DataFrame(natija_data)

    st.subheader("📋 Natija jadvali:")
    st.dataframe(df, use_container_width=True)

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
