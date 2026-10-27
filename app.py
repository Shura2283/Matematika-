import streamlit as st
import random
import pandas as pd
from io import BytesIO
from datetime import datetime

# Sahifa sozlamalari
st.set_page_config(page_title="Bilimlar Trenajori", page_icon="🎓", layout="centered")

# Ko'k, yashil, sariq va qizil ranglar aralashmasi (gradient fon) va aniq jadvallar
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d324d 0%, #1e5239 30%, #7d6b14 70%, #5e1914 100%);
            background-attachment: fixed;
            color: #FFFFFF;
        }
        header {visibility: hidden;}
        
        div[data-testid="stForm"], div[data-testid="stMetric"], .author-card {
            background-color: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 14px !important;
            padding: 16px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
        }
        
        div[data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #CBD5E1 !important;
            font-size: 1rem !important;
        }
        
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            color: #FFFFFF !important;
            background-color: rgba(30, 41, 59, 0.95) !important;
            border: 1px solid #64748B !important;
            border-radius: 8px !important;
        }
        
        .author-badge {
            display: inline-block;
            background: rgba(0, 0, 0, 0.6);
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.95rem;
            color: #F1F5F9;
            border: 1px solid rgba(255, 255, 255, 0.25);
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Yon menyu (Sidebar) orqali fanni tanlash
st.sidebar.title("📚 Bo'limlar menyusi")
fan_tanlovi = st.sidebar.radio("Fanni tanlang:", ["🧮 Matematika", "🇬🇧 Ingliz tili"])

st.sidebar.markdown("---")
st.sidebar.info("✨ **Tuzuvchi:**\nQuljanova Shukurjon Zaribovna")

# =========================================================================
# 1-BO'LIM: MATEMATIKA TRENAJORI
# =========================================================================
if fan_tanlovi == "🧮 Matematika":
    if "math_step" not in st.session_state:
        st.session_state.math_step = "login"
        st.session_state.math_student_name = ""
        st.session_state.math_student_class = ""
        st.session_state.math_chosen_op = "Aralash (+, -, *, /)"
        st.session_state.math_score = 0
        st.session_state.math_total = 0
        st.session_state.math_last_result = None

    def math_yangi_savol():
        tanlov = st.session_state.math_chosen_op
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
            st.session_state.math_num1 = boluvchi * bolinma
            st.session_state.math_num2 = boluvchi
        elif op == "*":
            st.session_state.math_num1 = random.randint(2, 10)
            st.session_state.math_num2 = random.randint(2, 10)
        elif op == "-":
            a = random.randint(5, 50)
            b = random.randint(1, 50)
            st.session_state.math_num1 = max(a, b)
            st.session_state.math_num2 = min(a, b)
        else:
            st.session_state.math_num1 = random.randint(5, 50)
            st.session_state.math_num2 = random.randint(5, 50)
            
        st.session_state.math_operation = op

    if st.session_state.math_step == "login":
        st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
        st.title("🧮 Matematika Trenajori")
        st.write("Testni boshlashdan oldin ma'lumotlaringizni to'ldiring:")

        with st.form("math_login_form"):
            ism_familiya = st.text_input("Familiya va Ismingiz:", placeholder="Masalan: Karimov Ali")
            sinf = st.text_input("Sinfingiz:", placeholder="Masalan: 5-A")
            amal_tanlovi = st.selectbox(
                "Amal turini tanlang:",
                ["Aralash (+, -, *, /)", "Qo'shish (+)", "Ayirish (-)", "Ko'paytirish (*)", "Bo'lish (/)"]
            )
            boshlash = st.form_submit_button("Testni boshlash 🚀")

            if boshlash:
                if ism_familiya.strip() and sinf.strip():
                    st.session_state.math_student_name = ism_familiya.strip()
                    st.session_state.math_student_class = sinf.strip()
                    st.session_state.math_chosen_op = amal_tanlovi
                    st.session_state.math_step = "test"
                    math_yangi_savol()
                    st.rerun()
                else:
                    st.error("Iltimos, ma'lumotlarni to'liq kiriting!")

    elif st.session_state.math_step == "test":
        st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
        st.subheader(f"👤 O'quvchi: {st.session_state.math_student_name} | Sinf: {st.session_state.math_student_class}")
        st.caption(f"Amal turi: **{st.session_state.math_chosen_op}**")
        
        n1 = st.session_state.math_num1
        n2 = st.session_state.math_num2
        op = st.session_state.math_operation

        if op == "+":
            togri_javob = n1 + n2
        elif op == "-":
            togri_javob = n1 - n2
        elif op == "*":
            togri_javob = n1 * n2
        else:
            togri_javob = n1 // n2

        col1, col2 = st.columns(2)
        col1.metric("Misol tartibi", f"{st.session_state.math_total + 1} / 25")
        col2.metric("To'g'ri javoblar", f"{st.session_state.math_score} ta")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.math_last_result:
            status, msg = st.session_state.math_last_result
            if status == "success":
                st.success(msg)
            else:
                st.error(msg)

        display_op = "÷" if op == "/" else ("×" if op == "*" else op)
        st.subheader(f"Misolni yeching: **{n1} {display_op} {n2} = ?**")

        with st.form("math_test_form", clear_on_submit=True):
            foydalanuvchi_javobi = st.number_input("Javobingiz:", step=1, value=None, placeholder="Son kiriting...")
            yuborish = st.form_submit_button("Tasdiqlash")

            if yuborish:
                if foydalanuvchi_javobi is not None:
                    st.session_state.math_total += 1
                    if int(foydalanuvchi_javobi) == togri_javob:
                        st.session_state.math_score += 1
                        st.session_state.math_last_result = ("success", f"To'g'ri! 🎉 ({n1} {display_op} {n2} = {togri_javob})")
                    else:
                        st.session_state.math_last_result = ("error", f"Noto'g'ri! ❌ To'g'ri javob: {togri_javob} edi")

                    if st.session_state.math_total >= 25:
                        st.session_state.math_step = "result"
                    else:
                        math_yangi_savol()
                    st.rerun()
                else:
                    st.warning("Iltimos, avval javobni yozing!")

    elif st.session_state.math_step == "result":
        togri = st.session_state.math_score
        xato = 25 - togri
        ball = togri * 4

        st.balloons()
        st.success("🎉 **Matematika testi muvaffaqiyatli yakunlandi!**")
        
        st.markdown(f"""
            <div class="author-card" style="margin-bottom: 20px;">
                <h3>📊 Natijalar xulosasi</h3>
                <p><b>O'quvchi:</b> {st.session_state.math_student_name}</p>
                <p><b>Sinf:</b> {st.session_state.math_student_class}</p>
                <p><b>Fan:</b> Matematika ({st.session_state.math_chosen_op})</p>
                <p><b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("To'g'ri", f"{togri} ta")
        col2.metric("Xato", f"{xato} ta")
        col3.metric("To'plangan ball", f"{ball} / 100")

        hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
        natija_data = {
            "Familiya va Ism": [st.session_state.math_student_name],
            "Sinf": [st.session_state.math_student_class],
            "Fan": ["Matematika"],
            "Mavzu / Amal": [st.session_state.math_chosen_op],
            "To'g'ri javoblar": [togri],
            "Xato javoblar": [xato],
            "To'plangan ball": [ball],
            "Maksimal ball": [100],
            "Sana va vaqt": [hozirgi_vaqt],
            "Tuzuvchi": ["Quljanova Shukurjon Zaribovna"]
        }
        df = pd.DataFrame(natija_data)
        st.dataframe(df, use_container_width=True)

        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Matematika_Natija')
        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📥 Natijani Excel formatida yuklab olish",
            data=excel_data,
            file_name=f"{st.session_state.math_student_name}_matematika.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")
        if st.button("Qayta boshlash 🔄"):
            st.session_state.math_step = "login"
            st.session_state.math_score = 0
            st.session_state.math_total = 0
            st.session_state.math_last_result = None
            st.rerun()

# =========================================================================
# 2-BO'LIM: INGLIZ TILI (10 TA MAVZU)
# =========================================================================
else:
    # 10 ta mavzu va har bir mavzuga mos savollar bazasi
    ENGLISH_TOPICS = {
        "1. Verb 'To be' (am, is, are)": [
            {"q": "I ___ a student.", "options": ["am", "is", "are", "be"], "a": "am"},
            {"q": "She ___ very kind.", "options": ["am", "is", "are", "were"], "a": "is"},
            {"q": "They ___ playing football.", "options": ["is", "am", "are", "be"], "a": "are"},
            {"q": "We ___ from Uzbekistan.", "options": ["am", "are", "is", "art"], "a": "are"},
            {"q": "It ___ a sunny day.", "options": ["are", "am", "is", "be"], "a": "is"}
        ],
        "2. Pronouns (Olmoshlar)": [
            {"q": "This is Ali. ___ is my best friend.", "options": ["She", "He", "It", "They"], "a": "He"},
            {"q": "Look at Malika. ___ is singing well.", "options": ["He", "She", "It", "We"], "a": "She"},
            {"q": "Give ___ that book, please.", "options": ["I", "me", "he", "she"], "a": "me"},
            {"q": "This car belongs to us. It is ___ car.", "options": ["our", "my", "your", "their"], "a": "our"},
            {"q": "The cat is washing ___ face.", "options": ["his", "her", "its", "it"], "a": "its"}
        ],
        "3. Present Simple (Hozirgi oddiy zamon)": [
            {"q": "He ___ to school every day.", "options": ["go", "goes", "going", "went"], "a": "goes"},
            {"q": "They ___ like coffee.", "options": ["doesn't", "don't", "not", "isn't"], "a": "don't"},
            {"q": "___ you speak English?", "options": ["Do", "Does", "Is", "Are"], "a": "Do"},
            {"q": "She usually ___ up at 7 o'clock.", "options": ["wake", "wakes", "waking", "woke"], "a": "wakes"},
            {"q": "The sun ___ in the east.", "options": ["rises", "rise", "rising", "rose"], "a": "rises"}
        ],
        "4. Articles (A / An / The)": [
            {"q": "She wants to eat ___ apple.", "options": ["a", "an", "the", "-"], "a": "an"},
            {"q": "I have ___ new car.", "options": ["a", "an", "the", "-"], "a": "a"},
            {"q": "___ moon shines brightly at night.", "options": ["A", "An", "The", "-"], "a": "The"},
            {"q": "He is ___ honest boy.", "options": ["a", "an", "the", "-"], "a": "an"},
            {"q": "Tashkent is ___ capital of Uzbekistan.", "options": ["a", "an", "the", "-"], "a": "the"}
        ],
        "5. Plural Nouns (Ko'plik qo'shimchalari)": [
            {"q": "One child, two ___.", "options": ["childs", "children", "childrens", "childes"], "a": "children"},
            {"q": "One box, three ___.", "options": ["boxs", "boxes", "boxies", "boxen"], "a": "boxes"},
            {"q": "One city, many ___.", "options": ["citys", "cities", "cityes", "city"], "a": "cities"},
            {"q": "One tooth, four ___.", "options": ["tooths", "teeth", "toothes", "teeths"], "a": "teeth"},
            {"q": "One man, five ___.", "options": ["mans", "men", "mens", "manes"], "a": "men"}
        ],
        "6. Prepositions of Place (in / on / at)": [
            {"q": "The book is ___ the table.", "options": ["in", "on", "at", "under"], "a": "on"},
            {"q": "There is milk ___ the fridge.", "options": ["on", "in", "at", "to"], "a": "in"},
            {"q": "I am waiting ___ the bus stop.", "options": ["on", "at", "in", "into"], "a": "at"},
            {"q": "The picture is hanging ___ the wall.", "options": ["in", "on", "at", "by"], "a": "on"},
            {"q": "We live ___ Uzbekistan.", "options": ["at", "on", "in", "from"], "a": "in"}
        ],
        "7. Adjectives & Opposites (Sifatlar)": [
            {"q": "What is the opposite of 'Big'?", "options": ["Fast", "Small", "Tall", "Heavy"], "a": "Small"},
            {"q": "What is the opposite of 'Hot'?", "options": ["Cold", "Warm", "Bright", "Dark"], "a": "Cold"},
            {"q": "What is the opposite of 'Fast'?", "options": ["Quick", "Slow", "Hard", "Easy"], "a": "Slow"},
            {"q": "An elephant is very ___.", "options": ["heavy", "light", "thin", "short"], "a": "heavy"},
            {"q": "Ice is ___.", "options": ["warm", "hot", "cold", "soft"], "a": "cold"}
        ],
        "8. Numbers & Time (Raqamlar va vaqt)": [
            {"q": "What number is 'Forty-five'?", "options": ["54", "45", "405", "15"], "a": "45"},
            {"q": "How do you say 8:30?", "options": ["Half past eight", "Eight o'clock", "Quarter to eight", "Half to eight"], "a": "Half past eight"},
            {"q": "How many days are there in a week?", "options": ["Five", "Six", "Seven", "Ten"], "a": "Seven"},
            {"q": "How do you say 12:00?", "options": ["Twelve past", "Twelve o'clock", "Half past twelve", "Midday only"], "a": "Twelve o'clock"},
            {"q": "How many months are in a year?", "options": ["10", "11", "12", "14"], "a": "12"}
        ],
        "9. Daily Routine (Kun tartibi so'zlari)": [
            {"q": "I ___ my teeth in the morning.", "options": ["wash", "brush", "clean", "comb"], "a": "brush"},
            {"q": "We ___ breakfast at 8:00 AM.", "options": ["have", "do", "make", "cook"], "a": "have"},
            {"q": "Students ___ homework in the evening.", "options": ["make", "do", "write", "play"], "a": "do"},
            {"q": "I ___ to bed at 10:00 PM.", "options": ["sleep", "go", "enter", "leave"], "a": "go"},
            {"q": "She ___ a shower every day.", "options": ["takes", "does", "goes", "drinks"], "a": "takes"}
        ],
        "10. School Vocabulary (Maktab lug'ati)": [
            {"q": "You use this to erase pencil marks:", "options": ["Ruler", "Eraser", "Pen", "Notebook"], "a": "Eraser"},
            {"q": "The person who teaches in a school:", "options": ["Doctor", "Teacher", "Engineer", "Driver"], "a": "Teacher"},
            {"q": "You carry your school books in a ___.", "options": ["Pencil case", "Backpack", "Folder", "Desk"], "a": "Backpack"},
            {"q": "A book where you write notes:", "options": ["Textbook", "Notebook", "Dictionary", "Novel"], "a": "Notebook"},
            {"q": "A place in school where you read books quietly:", "options": ["Gym", "Canteen", "Library", "Yard"], "a": "Library"}
        ]
    }

    if "eng_step" not in st.session_state:
        st.session_state.eng_step = "login"
        st.session_state.eng_student_name = ""
        st.session_state.eng_student_class = ""
        st.session_state.eng_topic = list(ENGLISH_TOPICS.keys())[0]
        st.session_state.eng_score = 0
        st.session_state.eng_current_idx = 0
        st.session_state.eng_questions = []

    if st.session_state.eng_step == "login":
        st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
        st.title("🇬🇧 English Grammar & Vocabulary")
        st.write("Ingliz tili testini boshlashdan oldin ma'lumotlarni to'ldiring:")

        with st.form("eng_login_form"):
            ism_familiya = st.text_input("Familiya va Ismingiz:", placeholder="Masalan: Karimova Dilnoza")
            sinf = st.text_input("Sinfingiz:", placeholder="Masalan: 6-B")
            mavzu = st.selectbox("Test topshiriladigan mavzuni tanlang:", list(ENGLISH_TOPICS.keys()))
            boshlash = st.form_submit_button("Testni boshlash 🚀")

            if boshlash:
                if ism_familiya.strip() and sinf.strip():
                    st.session_state.eng_student_name = ism_familiya.strip()
                    st.session_state.eng_student_class = sinf.strip()
                    st.session_state.eng_topic = mavzu
                    st.session_state.eng_score = 0
                    st.session_state.eng_current_idx = 0
                    # Mavzudagi savollarni aralashtirib olish
                    savollar = ENGLISH_TOPICS[mavzu].copy()
                    random.shuffle(savollar)
                    st.session_state.eng_questions = savollar
                    st.session_state.eng_step = "test"
                    st.rerun()
                else:
                    st.error("Iltimos, ism va sinfingizni kiriting!")

    elif st.session_state.eng_step == "test":
        st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
        st.subheader(f"👤 O'quvchi: {st.session_state.eng_student_name} | Sinf: {st.session_state.eng_student_class}")
        st.caption(f"Mavzu: **{st.session_state.eng_topic}**")

        q_list = st.session_state.eng_questions
        idx = st.session_state.eng_current_idx
        current_q = q_list[idx]

        col1, col2 = st.columns(2)
        col1.metric("Savol tartibi", f"{idx + 1} / {len(q_list)}")
        col2.metric("To'g'ri javoblar", f"{st.session_state.eng_score} ta")

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(f"Question {idx + 1}: **{current_q['q']}**")

        with st.form("eng_test_form"):
            tanlangan_javob = st.radio("Javob variantini tanlang:", current_q["options"])
            yuborish = st.form_submit_button("Tasdiqlash ➡️")

            if yuborish:
                if tanlangan_javob == current_q["a"]:
                    st.session_state.eng_score += 1
                
                if idx + 1 >= len(q_list):
                    st.session_state.eng_step = "result"
                else:
                    st.session_state.eng_current_idx += 1
                st.rerun()

    elif st.session_state.eng_step == "result":
        q_soni = len(st.session_state.eng_questions)
        togri = st.session_state.eng_score
        xato = q_soni - togri
        ball = int((togri / q_soni) * 100)

        st.balloons()
        st.success("🎉 **English Test Completed! (Test yakunlandi)**")

        st.markdown(f"""
            <div class="author-card" style="margin-bottom: 20px;">
                <h3>📊 Natijalar xulosasi</h3>
                <p><b>O'quvchi:</b> {st.session_state.eng_student_name}</p>
                <p><b>Sinf:</b> {st.session_state.eng_student_class}</p>
                <p><b>Fan:</b> Ingliz tili</p>
                <p><b>Mavzu:</b> {st.session_state.eng_topic}</p>
                <p><b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("To'g'ri javoblar", f"{togri} ta")
        col2.metric("Xato javoblar", f"{xato} ta")
        col3.metric("To'plangan ball", f"{ball} / 100")

        hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
        natija_data = {
            "Familiya va Ism": [st.session_state.eng_student_name],
            "Sinf": [st.session_state.eng_student_class],
            "Fan": ["Ingliz tili"],
            "Mavzu": [st.session_state.eng_topic],
            "To'g'ri javoblar": [togri],
            "Xato javoblar": [xato],
            "To'plangan ball": [ball],
            "Maksimal ball": [100],
            "Sana va vaqt": [hozirgi_vaqt],
            "Tuzuvchi": ["Quljanova Shukurjon Zaribovna"]
        }
        df = pd.DataFrame(natija_data)
        st.dataframe(df, use_container_width=True)

        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='English_Natija')
        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📥 Natijani Excel formatida yuklab olish",
            data=excel_data,
            file_name=f"{st.session_state.eng_student_name}_english.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")
        if st.button("Qaytadan boshlash 🔄"):
            st.session_state.eng_step = "login"
            st.session_state.eng_score = 0
            st.session_state.eng_current_idx = 0
            st.rerun()
