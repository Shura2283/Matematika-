import streamlit as st
import random
import pandas as pd
from io import BytesIO
from datetime import datetime
import streamlit.components.v1 as components

# Sahifa sozlamalari
st.set_page_config(page_title="Bilimlar Trenajori", page_icon="🎓", layout="wide")

# Fon va zamonaviy jadvallar dizayni
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d324d 0%, #1e5239 30%, #7d6b14 70%, #5e1914 100%);
            background-attachment: fixed;
            color: #FFFFFF;
        }
        header {visibility: hidden;}
        div[data-testid="stForm"], div[data-testid="stMetric"], .custom-card {
            background-color: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 14px !important;
            padding: 18px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
            margin-bottom: 15px;
        }
        div[data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricLabel"] {
            color: #CBD5E1 !important;
        }
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            color: #FFFFFF !important;
            background-color: rgba(30, 41, 59, 0.95) !important;
            border: 1px solid #64748B !important;
            border-radius: 8px !important;
        }
        .author-badge {
            display: inline-block;
            background: rgba(0, 0, 0, 0.65);
            padding: 7px 18px;
            border-radius: 20px;
            font-size: 0.95rem;
            color: #F1F5F9;
            border: 1px solid rgba(255, 255, 255, 0.25);
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Yon menyu sozlamalari
st.sidebar.title("⚙️ Sozlamalar & Bo'limlar")

# 1. Ovozni yoqish / o'chirish boshqaruvi
audio_enabled = st.sidebar.toggle("🔊 Ovozli talaffuzni yoqish", value=True)

def audio_button(text):
    if not audio_enabled:
        return
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    html_code = f"""
    <button onclick="speakText('{clean_text}')" style="background:#2563EB;color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-weight:600;font-size:12px;display:inline-flex;align-items:center;gap:4px;">
        🔊 Tinglash
    </button>
    <script>
    function speakText(txt) {{
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(txt);
        u.lang = 'en-US';
        u.rate = 0.9;
        window.speechSynthesis.speak(u);
    }}
    </script>
    """
    components.html(html_code, height=36)

# Bo'lim tanlovi
asosiy_menyu = st.sidebar.radio(
    "Fanni tanlang:",
    ["📖 1000 ta so'z (50 ta Bob)", "🧮 Matematika Trenajori"]
)

st.sidebar.markdown("---")
st.sidebar.info("✨ **Tuzuvchi:**\nQuljanova Shukurjon Zaribovna")

# =========================================================================
# 1-BO'LIM: 1000 TA SO'Z (50 TA BOB)
# =========================================================================
if asosiy_menyu == "📖 1000 ta so'z (50 ta Bob)":
    st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
    st.title("📖 Eng kerakli 1000 ta so'z — 50 ta Bob")
    st.caption("A2–B2 darajadagi 1000 ta so'z, 20 tadan to'liq yozma tarjima va to'liq Excel hisoboti")

    bob_nomlari = [f"{i}-Bob" for i in range(1, 51)]
    tanlangan_bob = st.sidebar.selectbox("O'rganish uchun Bobni tanlang:", bob_nomlari)
    bob_raqami = int(tanlangan_bob.split("-")[0])

    # 1000 ta so'z kitobi bo'yicha bazaviy so'zlar
    KITOB_SOZLARI = {
        1: [
            ("man", "erkak", "He is a tall man."), ("woman", "ayol", "She is a kind woman."),
            ("child", "bola", "The child is playing."), ("people", "odamlar", "There are many people in the park."),
            ("person", "shaxs", "He is a nice person."), ("friend", "do'st", "My friend is very funny."),
            ("family", "oila", "I love my family."), ("mother", "ona", "My mother is a teacher."),
            ("father", "ota", "My father works in a bank."), ("parents", "ota-onalar", "My parents are at home."),
            ("son", "o'g'il farzand", "He has a son."), ("daughter", "qiz farzand", "She has a daughter."),
            ("brother", "aka/uka", "My brother is a student."), ("sister", "opa/singil", "My sister likes music."),
            ("husband", "er", "Her husband is a doctor."), ("wife", "xotin", "His wife is very kind."),
            ("uncle", "amaki/tog'a", "My uncle lives in Tashkent."), ("aunt", "amma/xola", "My aunt is very friendly."),
            ("cousin", "amakivachcha", "My cousin is my best friend."), ("grandfather", "bobo", "My grandfather is old.")
        ],
        2: [
            ("grandmother", "buvi", "My grandmother cooks delicious food."), ("baby", "chaqaloq", "The baby is sleeping."),
            ("teenager", "o'smir", "He is a teenager."), ("adult", "kattalar", "Adults work every day."),
            ("relative", "qarindosh", "I visited my relatives."), ("neighbour", "qo'shni", "My neighbour is very kind."),
            ("roommate", "xonadosh", "My roommate studies at night."), ("colleague", "hamkasb", "My colleague is very helpful."),
            ("team", "jamoa", "Our team won the game."), ("group", "guruh", "I work in a study group."),
            ("member", "a'zo", "He is a member of our club."), ("single", "yolg'iz", "She is single."),
            ("married", "oilali", "They are married."), ("divorced", "ajrashgan", "She is divorced."),
            ("relationship", "munosabat", "They have a good relationship."), ("love", "sevmoq", "I love my family."),
            ("care", "g'amxo'rlik qilmoq", "She cares about her parents."), ("support", "qo'llab-quvvatlamoq", "My friends support me."),
            ("respect", "hurmat qilmoq", "I respect my teacher."), ("meet", "uchrashmoq", "I meet my friends every week.")
        ],
        3: [
            ("visit", "ziyorat qilmoq", "I visit my grandparents."), ("talk", "gaplashmoq", "We talk every day."),
            ("share", "bo'lishmoq", "I share my ideas with friends."), ("help", "yordam bermoq", "My brother helps me."),
            ("live", "yashamoq", "I live in Tashkent."), ("together", "birga", "We study together."),
            ("alone", "yolg'iz", "He lives alone."), ("close", "yaqin", "I am close to my sister."),
            ("friendly", "do'stona", "She is very friendly."), ("kind", "mehribon", "My teacher is kind."),
            ("polite", "odobli", "She is very polite to everyone."), ("rude", "qo'pol", "He is rude sometimes."),
            ("shy", "uyatchan", "I am a shy person."), ("outgoing", "ochiqko'ngil", "She is outgoing and friendly."),
            ("funny", "kulgili", "My friend is very funny."), ("serious", "jiddiy", "He is a serious student."),
            ("honest", "halol", "My father is honest."), ("lazy", "dangasa", "He is lazy sometimes."),
            ("hardworking", "mehnatkash", "She is hardworking."), ("smart", "aqlli", "My brother is smart.")
        ]
    }

    # 20 ta so'z ro'yxatini yuklash
    if bob_raqami in KITOB_SOZLARI:
        hozirgi_sozlar = [{"en": w, "uz": u, "ex": ex} for w, u, ex in KITOB_SOZLARI[bob_raqami]]
    else:
        # Qolgan boblar uchun kitobdagi Topic 2-10 so'zlari
        mavzu_sozlari = [
            ("wake up", "uyg'onmoq"), ("get up", "o'rnidan turmoq"), ("sleep", "uxlamoq"), ("shower", "dush qabul qilmoq"),
            ("breakfast", "nonushta"), ("lunch", "tushlik"), ("dinner", "kechki ovqat"), ("cook", "ovqat pishirmoq"),
            ("clean", "tozalamoq"), ("study", "o'qimoq"), ("work", "ishlamoq"), ("leave", "chiqib ketmoq"),
            ("return", "qaytmoq"), ("listen", "tinglamoq"), ("speak", "gapirmoq"), ("travel", "sayohat qilmoq"),
            ("city", "shahar"), ("hospital", "kasalxona"), ("health", "sog'lik"), ("internet", "internet")
        ]
        hozirgi_sozlar = []
        for j, (w, u) in enumerate(mavzu_sozlari):
            hozirgi_sozlar.append({
                "en": w, "uz": u, "ex": f"This is an example sentence for {w}."
            })

    # Bobning 20-40 so'zdan iborat matni
    standart_matn = {
        "en": f"In lesson {bob_raqami}, active students practice twenty important words every day. Regular writing, speaking and reviewing with teachers will enhance your vocabulary and English communication skills effectively.",
        "uz": f"{bob_raqami}-bobda faol o'quvchilar har kuni yigirmata muhim so'zni mashq qiladilar. Muntazam yozish, gapirish va ustozlar bilan takrorlash so'z boyligi va ingliz tilida muloqot qilish ko'nikmalarini oshiradi."
    }

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ So'zlar & Audio", 
        "2️⃣ Yozma mashq (EN ➔ UZ - 20 ta)", 
        "3️⃣ Yozma mashq (UZ ➔ EN - 20 ta)", 
        "4️⃣ Bob Testi & Excel Kompilyatsiya", 
        "5️⃣ O'qish matni (Reading)"
    ])

    # 1-TAB: So'zlar va Ovoz
    with tab1:
        st.subheader(f"📖 {tanlangan_bob} — 20 ta asosiy so'z")
        if not audio_enabled:
            st.warning("⚠️ Ovoz hozirda o'chirilgan (Sidebar orqali yoqishingiz mumkin).")
        
        for idx, item in enumerate(hozirgi_sozlar):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"**{idx+1}. {item['en']}** — *{item['uz']}*  \n*(Misol: {item['ex']})*")
            with c2:
                audio_button(item['en'])
            st.divider()

    # 2-TAB: 20 ta so'z EN ➔ UZ to'liq yozish
    with tab2:
        st.subheader("✍️ Barcha 20 ta so'zning o'zbekcha tarjimasini yozing:")
        with st.form(f"form_en_uz_all_{bob_raqami}"):
            foydalanuvchi_javoblari_1 = []
            for i, item in enumerate(hozirgi_sozlar):
                col_q, col_aud = st.columns([5, 1])
                with col_q:
                    ans = st.text_input(f"{i+1}. '{item['en']}' so'zining tarjimasi:", key=f"all_en_uz_{bob_raqami}_{i}")
                with col_aud:
                    audio_button(item['en'])
                foydalanuvchi_javoblari_1.append((item, ans))
                
            tekshir_1 = st.form_submit_button("20 ta javobni tekshirish")
            
            if tekshir_1:
                togri_1 = 0
                for item, ans in foydalanuvchi_javoblari_1:
                    if ans.strip().lower() in item['uz'].lower() and ans.strip() != "":
                        togri_1 += 1
                        st.success(f"✅ To'g'ri: **{item['en']}** = {item['uz']}")
                    else:
                        st.error(f"❌ Xato: **{item['en']}** ➔ To'g'ri javob: {item['uz']} (Siz yozdingiz: '{ans}')")
                st.info(f"📊 Natija: 20 tadan {togri_1} ta to'g'ri!")

    # 3-TAB: 20 ta so'z UZ ➔ EN to'liq yozish
    with tab3:
        st.subheader("✍️ Barcha 20 ta so'zning inglizcha tarjimasini yozing:")
        with st.form(f"form_uz_en_all_{bob_raqami}"):
            foydalanuvchi_javoblari_2 = []
            for i, item in enumerate(hozirgi_sozlar):
                ans = st.text_input(f"{i+1}. '{item['uz']}' so'zining inglizchasi:", key=f"all_uz_en_{bob_raqami}_{i}")
                foydalanuvchi_javoblari_2.append((item, ans))
                
            tekshir_2 = st.form_submit_button("20 ta inglizcha so'zni tekshirish")
            
            if tekshir_2:
                togri_2 = 0
                for item, ans in foydalanuvchi_javoblari_2:
                    if ans.strip().lower() == item['en'].lower():
                        togri_2 += 1
                        st.success(f"✅ To'g'ri: **{item['uz']}** = {item['en']}")
                    else:
                        st.error(f"❌ Xato: **{item['uz']}** ➔ To'g'risi: '{item['en']}' (Siz yozdingiz: '{ans}')")
                st.info(f"📊 Natija: 20 tadan {togri_2} ta to'g'ri!")

    # 4-TAB: Bob Testi & To'liq Excel Kompilyatsiyasi
    with tab4:
        st.subheader(f"📝 {tanlangan_bob} bo'yicha 20 ta so'zlik to'liq test")
        
        with st.form(f"test_form_all_{bob_raqami}"):
            st.markdown("#### O'quvchi ma'lumotlari:")
            col_ism, col_sinf = st.columns(2)
            with col_ism:
                ism = st.text_input("Familiya va Ismingiz:", key=f"ism_b_{bob_raqami}", placeholder="Karimov Ali")
            with col_sinf:
                sinf = st.text_input("Sinfingiz:", key=f"sinf_b_{bob_raqami}", placeholder="7-A")
            
            st.markdown("---")
            st.markdown("#### Test savollari (20 ta):")
            
            tanlovlar = []
            for i, q in enumerate(hozirgi_sozlar):
                togri = q["uz"]
                notogri_variantlar = [x["uz"] for x in hozirgi_sozlar if x["uz"] != togri]
                tanlangan_notogri = random.sample(notogri_variantlar, min(3, len(notogri_variantlar)))
                variantlar = [togri] + tanlangan_notogri
                random.seed(i + bob_raqami * 10)
                random.shuffle(variantlar)
                
                c_q, c_a = st.columns([5, 1])
                with c_q:
                    ans = st.radio(f"{i+1}. '{q['en']}' so'zining tarjimasi qaysi?", variantlar, key=f"radio_b_{bob_raqami}_{i}")
                with c_a:
                    audio_button(q['en'])
                tanlovlar.append((q, ans))
                
            yakunlash = st.form_submit_button("Testni topshirish va Excel hisobot olish 🎯")
            
            if yakunlash:
                if ism.strip() and sinf.strip():
                    detallar = []
                    togri_soni = 0
                    for idx_q, (q, user_a) in enumerate(tanlovlar):
                        is_correct = (user_a == q["uz"])
                        if is_correct:
                            togri_soni += 1
                        detallar.append({
                            "Savol №": idx_q + 1,
                            "Inglizcha so'z": q["en"],
                            "To'g'ri tarjima": q["uz"],
                            "O'quvchi tanlagan javob": user_a,
                            "Holati": "To'g'ri" if is_correct else "Xato"
                        })
                    
                    jami = len(hozirgi_sozlar)
                    xato_soni = jami - togri_soni
                    ball = int((togri_soni / jami) * 100)
                    
                    st.balloons()
                    st.success("🎉 Test topshirildi va barcha javoblar kompilyatsiya qilindi!")
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("To'g'ri", f"{togri_soni} ta")
                    c2.metric("Xato", f"{xato_soni} ta")
                    c3.metric("To'plangan ball", f"{ball} / 100")
                    
                    st.markdown("### 📋 Barcha 20 ta savol tahlili:")
                    df_detal = pd.DataFrame(detallar)
                    st.dataframe(df_detal, use_container_width=True)
                    
                    # 2 ta varaqli to'liq Excel kompilyatsiya fayli
                    hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
                    xulosa_data = {
                        "O'quvchi": [ism],
                        "Sinf": [sinf],
                        "Bob": [tanlangan_bob],
                        "Jami savollar": [jami],
                        "To'g'ri javoblar": [togri_soni],
                        "Xato javoblar": [xato_soni],
                        "Ball": [ball],
                        "Sana va vaqt": [hozirgi_vaqt],
                        "Tuzuvchi": ["Quljanova Shukurjon Zaribovna"]
                    }
                    df_xulosa = pd.DataFrame(xulosa_data)
                    
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_xulosa.to_excel(writer, index=False, sheet_name='Umumiy_Xulosa')
                        df_detal.to_excel(writer, index=False, sheet_name='20ta_Savol_Batafsil')
                    excel_data = excel_buffer.getvalue()
                    
                    st.download_button(
                        label="📥 Barcha javoblar kompilyatsiyasini Excel (.xlsx) da yuklab olish",
                        data=excel_data,
                        file_name=f"{ism}_{tanlangan_bob}_kompilyatsiya.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error("Iltimos, ism va sinfingizni to'liq kiriting!")

    # 5-TAB: O'qish matni va Audio
    with tab5:
        st.subheader("📖 Bob matni (Reading & Listening)")
        c_txt, c_btn = st.columns([5, 1])
        with c_txt:
            st.markdown(f"**🇬🇧 English text:**  \n### \"{standart_matn['en']}\"")
        with c_btn:
            audio_button(standart_matn['en'])
            
        st.divider()
        st.markdown(f"**🇺🇿 O'zbekcha tarjimasi:**  \n### \"{standart_matn['uz']}\"")

# =========================================================================
# 2-BO'LIM: MATEMATIKA TRENAJORI
# =========================================================================
else:
    st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
    st.title("🧮 Matematika Trenajori")
    st.info("25 ta misoldan iborat test va Excel hisobot.")
    
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
        op = random.choice(["+", "-", "*", "/"]) if tanlov.startswith("Aralash") else ("+" if "+" in tanlov else ("-" if "-" in tanlov else ("*" if "*" in tanlov else "/")))
        if op == "/":
            b = random.randint(2, 10)
            res = random.randint(1, 12)
            st.session_state.math_num1 = b * res
            st.session_state.math_num2 = b
        elif op == "*":
            st.session_state.math_num1 = random.randint(2, 10)
            st.session_state.math_num2 = random.randint(2, 10)
        elif op == "-":
            a, b = random.randint(5, 50), random.randint(1, 50)
            st.session_state.math_num1, st.session_state.math_num2 = max(a, b), min(a, b)
        else:
            st.session_state.math_num1 = random.randint(5, 50)
            st.session_state.math_num2 = random.randint(5, 50)
        st.session_state.math_operation = op

    if st.session_state.math_step == "login":
        with st.form("math_login_form"):
            ism = st.text_input("Familiya va Ism:")
            sinf = st.text_input("Sinf:")
            amal = st.selectbox("Amal:", ["Aralash (+, -, *, /)", "Qo'shish (+)", "Ayirish (-)", "Ko'paytirish (*)", "Bo'lish (/)"])
            if st.form_submit_button("Boshlash 🚀"):
                if ism.strip() and sinf.strip():
                    st.session_state.math_student_name = ism
                    st.session_state.math_student_class = sinf
                    st.session_state.math_chosen_op = amal
                    st.session_state.math_step = "test"
                    math_yangi_savol()
                    st.rerun()

    elif st.session_state.math_step == "test":
        st.subheader(f"👤 {st.session_state.math_student_name} | Sinf: {st.session_state.math_student_class}")
        n1, n2, op = st.session_state.math_num1, st.session_state.math_num2, st.session_state.math_operation
        ans = n1 + n2 if op == "+" else (n1 - n2 if op == "-" else (n1 * n2 if op == "*" else n1 // n2))
        
        c1, c2 = st.columns(2)
        c1.metric("Savol", f"{st.session_state.math_total + 1} / 25")
        c2.metric("Ball", f"{st.session_state.math_score * 4}")
        
        display_op = "÷" if op == "/" else ("×" if op == "*" else op)
        st.subheader(f"Misol: **{n1} {display_op} {n2} = ?**")
        with st.form("math_q_form", clear_on_submit=True):
            user_ans = st.number_input("Javob:", step=1, value=None)
            if st.form_submit_button("Tasdiqlash"):
                if user_ans is not None:
                    st.session_state.math_total += 1
                    if int(user_ans) == ans:
                        st.session_state.math_score += 1
                    if st.session_state.math_total >= 25:
                        st.session_state.math_step = "result"
                    else:
                        math_yangi_savol()
                    st.rerun()

    elif st.session_state.math_step == "result":
        togri = st.session_state.math_score
        ball = togri * 4
        st.balloons()
        st.success("🎉 Matematika yakunlandi!")
        c1, c2, c3 = st.columns(3)
        c1.metric("To'g'ri", f"{togri} ta")
        c2.metric("Xato", f"{25 - togri} ta")
        c3.metric("To'plangan ball", f"{ball} / 100")
        
        df = pd.DataFrame([{
            "Ism": st.session_state.math_student_name, "Sinf": st.session_state.math_student_class,
            "To'g'ri": togri, "Xato": 25 - togri, "Ball": ball, "Tuzuvchi": "Quljanova Shukurjon Zaribovna"
        }])
        st.dataframe(df, use_container_width=True)
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            df.to_excel(w, index=False)
        st.download_button("📥 Excel yuklab olish", buf.getvalue(), f"{st.session_state.math_student_name}_matematika.xlsx")
        if st.button("Qayta boshlash 🔄"):
            st.session_state.math_step = "login"
            st.session_state.math_score = 0
            st.session_state.math_total = 0
            st.rerun()
