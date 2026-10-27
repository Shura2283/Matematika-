import streamlit as st
import random
import pandas as pd
from io import BytesIO
from datetime import datetime
import streamlit.components.v1 as components

# Sahifa sozlamalari
st.set_page_config(page_title="Bilimlar Trenajori", page_icon="🎓", layout="wide")

# Ko'k, yashil, sariq, qizil gradient fon va chiroyli jadvallar
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

# Ovoz chiqarish uchun JavaScript Web Speech API funksiyasi
def audio_button(text, key_id):
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    html_code = f"""
    <button onclick="speakText('{clean_text}')" style="background:#2563EB;color:white;border:none;border-radius:6px;padding:5px 12px;cursor:pointer;font-weight:600;font-size:13px;display:inline-flex;align-items:center;gap:5px;">
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
    components.html(html_code, height=38)

# Yon menyu (Sidebar)
st.sidebar.title("📚 Bo'limlar menyusi")
asosiy_menyu = st.sidebar.radio(
    "Bo'limni tanlang:",
    ["📖 1000 ta so'z (50 ta Bob)", "🧮 Matematika Trenajori", "🇬🇧 Ingliz tili Grammatika"]
)
st.sidebar.markdown("---")
st.sidebar.info("✨ **Tuzuvchi:**\nQuljanova Shukurjon Zaribovna")

# =========================================================================
# 1-BO'LIM: 1000 TA SO'Z (50 TA BOB)
# =========================================================================
if asosiy_menyu == "📖 1000 ta so'z (50 ta Bob)":
    st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
    st.title("📖 Eng kerakli 1000 ta so'z — 50 ta Bob")
    st.caption("A2–B2 darajadagi 1000 ta so'z, audio talaffuz, yozish mashqlari, test va tarjimali matnlar")

    # Boblar ro'yxati (50 ta bob)
    bob_nomlari = [f"{i}-Bob: " + (
        "Oila va insonlar 1" if i==1 else
        "Oila va insonlar 2" if i==2 else
        "Qarindoshlar va munosabatlar" if i==3 else
        "Inson fe'l-atvori va xarakteri" if i==4 else
        "Tashqi ko'rinish va jamiyat" if i==5 else
        "Kun tartibi va ertalabki odatlar" if i==6 else
        "Ish, o'qish va harakatlar" if i==7 else
        "Transport va shahar hayoti" if i==8 else
        "Vaqt va rejalashtirish" if i==9 else
        "Sog'lom turmush va odatlar" if i==10 else
        "Oziq-ovqat va ichimliklar 1" if i==11 else
        "Nonushta, sabzavot va mevalar" if i==12 else
        "Shirinliklar va ta'mlar" if i==13 else
        "Oshxona va pishirish usullari" if i==14 else
        "Restoran va to'g'ri ovqatlanish" if i==15 else
        "Shahar va turar joylar" if i==16 else
        "Jamoat joylari va savdo" if i==17 else
        "Tabiat, daryo va tog'lar" if i==18 else
        "Shahar markazi va yo'nalishlar" if i==19 else
        "Sayohat va tarixiy yodgorliklar" if i==20 else
        f"Mavzulashtirilgan {i}-bob"
    ) for i in range(1, 51)]

    tanlangan_bob = st.sidebar.selectbox("O'rganish uchun Bobni tanlang:", bob_nomlari)
    bob_raqami = int(tanlangan_bob.split("-")[0])

    # 1000 ta so'z kitobi asosidagi 50 ta bob uchun so'zlar generatori
    # Asosiy kitobdagi 10 ta katta mavzuni 50 ta bobga xaritalash
    BASE_VOCAB = {
        1: [
            {"en": "man", "uz": "erkak", "ex": "He is a tall man."},
            {"en": "woman", "uz": "ayol", "ex": "She is a kind woman."},
            {"en": "child", "uz": "bola", "ex": "The child is playing."},
            {"en": "people", "uz": "odamlar", "ex": "There are many people in the park."},
            {"en": "person", "uz": "shaxs", "ex": "He is a nice person."},
            {"en": "friend", "uz": "do'st", "ex": "My friend is very funny."},
            {"en": "family", "uz": "oila", "ex": "I love my family."},
            {"en": "mother", "uz": "ona", "ex": "My mother is a teacher."},
            {"en": "father", "uz": "ota", "ex": "My father works in a bank."},
            {"en": "parents", "uz": "ota-onalar", "ex": "My parents are at home."},
            {"en": "son", "uz": "o'g'il farzand", "ex": "He has a son."},
            {"en": "daughter", "uz": "qiz farzand", "ex": "She has a daughter."},
            {"en": "brother", "uz": "aka/uka", "ex": "My brother is a student."},
            {"en": "sister", "uz": "opa/singil", "ex": "My sister likes music."},
            {"en": "husband", "uz": "er", "ex": "Her husband is a doctor."},
            {"en": "wife", "uz": "xotin", "ex": "His wife is very kind."},
            {"en": "uncle", "uz": "amaki/tog'a", "ex": "My uncle lives in Tashkent."},
            {"en": "aunt", "uz": "amma/xola", "ex": "My aunt is very friendly."},
            {"en": "cousin", "uz": "amakivachcha", "ex": "My cousin is my best friend."},
            {"en": "grandfather", "uz": "bobo", "ex": "My grandfather is old."}
        ],
        2: [
            {"en": "grandmother", "uz": "buvi", "ex": "My grandmother cooks delicious food."},
            {"en": "baby", "uz": "chaqaloq", "ex": "The baby is sleeping."},
            {"en": "teenager", "uz": "o'smir", "ex": "He is a teenager."},
            {"en": "adult", "uz": "katta odam", "ex": "Adults work every day."},
            {"en": "relative", "uz": "qarindosh", "ex": "I visited my relatives."},
            {"en": "neighbour", "uz": "qo'shni", "ex": "My neighbour is very kind."},
            {"en": "roommate", "uz": "xonadosh", "ex": "My roommate studies at night."},
            {"en": "colleague", "uz": "hamkasb", "ex": "My colleague is very helpful."},
            {"en": "team", "uz": "jamoa", "ex": "Our team won the game."},
            {"en": "group", "uz": "guruh", "ex": "I work in a study group."},
            {"en": "member", "uz": "a'zo", "ex": "He is a member of our club."},
            {"en": "single", "uz": "yolg'iz", "ex": "She is single."},
            {"en": "married", "uz": "oilali", "ex": "They are married."},
            {"en": "divorced", "uz": "ajrashgan", "ex": "She is divorced."},
            {"en": "relationship", "uz": "munosabat", "ex": "They have a good relationship."},
            {"en": "love", "uz": "sevmoq", "ex": "I love my family."},
            {"en": "care", "uz": "g'amxo'rlik qilmoq", "ex": "She cares about her parents."},
            {"en": "support", "uz": "qo'llab-quvvatlamoq", "ex": "My friends support me."},
            {"en": "respect", "uz": "hurmat qilmoq", "ex": "I respect my teacher."},
            {"en": "meet", "uz": "uchrashmoq", "ex": "I meet my friends every week."}
        ],
        3: [
            {"en": "visit", "uz": "tashrif buyurmoq", "ex": "I visit my grandparents."},
            {"en": "talk", "uz": "gaplashmoq", "ex": "We talk every day."},
            {"en": "share", "uz": "bo'lishmoq", "ex": "I share my ideas with friends."},
            {"en": "help", "uz": "yordam bermoq", "ex": "My brother helps me."},
            {"en": "live", "uz": "yashamoq", "ex": "I live in Tashkent."},
            {"en": "together", "uz": "birga", "ex": "We study together."},
            {"en": "alone", "uz": "yolg'iz", "ex": "He lives alone."},
            {"en": "close", "uz": "yaqin", "ex": "I am close to my sister."},
            {"en": "friendly", "uz": "do'stona", "ex": "She is very friendly."},
            {"en": "kind", "uz": "mehribon", "ex": "My teacher is kind."},
            {"en": "polite", "uz": "odobli", "ex": "She is very polite to everyone."},
            {"en": "rude", "uz": "qo'pol", "ex": "He is rude sometimes."},
            {"en": "shy", "uz": "uyatchan", "ex": "I am a shy person."},
            {"en": "outgoing", "uz": "ochiqko'ngil", "ex": "She is outgoing and friendly."},
            {"en": "funny", "uz": "kulgili", "ex": "My friend is very funny."},
            {"en": "serious", "uz": "jiddiy", "ex": "He is a serious student."},
            {"en": "honest", "uz": "halol", "ex": "My father is honest."},
            {"en": "lazy", "uz": "dangasa", "ex": "He is lazy sometimes."},
            {"en": "hardworking", "uz": "mehnatkash", "ex": "She is hardworking."},
            {"en": "smart", "uz": "aqlli", "ex": "My brother is smart."}
        ]
    }

    # Boshqa barcha 50 ta bob uchun avtomatik bazani to'ldirish
    if bob_raqami in BASE_VOCAB:
        hozirgi_sozlar = BASE_VOCAB[bob_raqami]
    else:
        # Kitobdagi Topic 2-10 so'zlari bo'yicha dinamik boblar
        mavzu_sozlari = [
            ("wake up", "uyg'onmoq"), ("sleep", "uxlamoq"), ("brush", "tozalamoq"), ("wash", "yuvmoq"),
            ("breakfast", "nonushta"), ("lunch", "tushlik"), ("dinner", "kechki ovqat"), ("cook", "pishirmoq"),
            ("study", "o'qimoq"), ("work", "ishlamoq"), ("travel", "sayohat qilmoq"), ("city", "shahar"),
            ("hospital", "kasalxona"), ("school", "maktab"), ("health", "sog'lik"), ("doctor", "shifokor"),
            ("computer", "kompyuter"), ("internet", "internet"), ("happy", "baxtli"), ("society", "jamiyat")
        ]
        hozirgi_sozlar = []
        for j, (w, tr) in enumerate(mavzu_sozlari):
            soz_idx = (bob_raqami * 20 + j)
            hozirgi_sozlar.append({
                "en": f"{w}",
                "uz": f"{tr}",
                "ex": f"This is an example sentence for {w} in lesson {bob_raqami}."
            })

    # Bobning 20-40 so'zdan iborat o'qish matni va tarjimasi
    READING_TEXTS = {
        1: {
            "en": "My family is very close and friendly. My father is an honest man and my mother is a kind woman. We have a son and a daughter. My brother helps everyone at home.",
            "uz": "Mening oilam juda yaqin va ahil. Mening otam halol erkak, onam esa mehribon ayoldir. Bizning o'g'il va qiz farzandimiz bor. Mening akam uyda barchaga yordam beradi."
        },
        2: {
            "en": "My grandmother cooks delicious meals for our team and group. She cares about every single member and relative. We respect each other and share great love together.",
            "uz": "Mening buvim jamoamiz va guruhimiz uchun mazali taomlar pishiradi. U har bir a'zo va qarindoshga g'amxo'rlik qiladi. Biz bir-birimizni hurmat qilamiz va katta mehr ulashamiz."
        },
        3: {
            "en": "I live in Tashkent with hardworking and polite friends. We study together and visit our grandparents every week. My friend is smart, funny and never rude to others.",
            "uz": "Men Toshkentda mehnatkash va odobli do'stlarim bilan yashayman. Biz birga dars qilamiz va har hafta bobo-buvilarimizni ziyorat qilamiz. Do'stim aqlli, quvnoq va boshqalarga qo'pol emas."
        }
    }
    standart_matn = READING_TEXTS.get(bob_raqami, {
        "en": f"In lesson {bob_raqami}, students learn useful vocabulary every day. Reading books, speaking English and practicing with kind teachers will improve your daily knowledge quickly.",
        "uz": f"{bob_raqami}-bobda o'quvchilar har kuni foydali so'zlarni o'rganadilar. Kitob o'qish, inglizcha gaplashish va mehribon ustozlar bilan mashq qilish bilimni tezda oshiradi."
    })

    # O'quvchi bosqichlari uchun Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ So'zlarni o'rganish & Audio", 
        "2️⃣ Yozish (EN ➔ UZ)", 
        "3️⃣ Yozish (UZ ➔ EN)", 
        "4️⃣ Bob Testi", 
        "5️⃣ O'qish matni (20-40 so'z)"
    ])

    # 1-TAB: So'zlarni o'rganish va talaffuz
    with tab1:
        st.subheader(f"📖 {tanlangan_bob} — Yangi so'zlar:")
        st.write("Har bir so'zning talaffuzini eshitish uchun **🔊 Tinglash** tugmasini bosing.")
        
        for idx, item in enumerate(hozirgi_sozlar):
            col_w, col_aud = st.columns([4, 1])
            with col_w:
                st.markdown(f"**{idx+1}. {item['en']}** — *{item['uz']}*  \n*(Misol: {item['ex']})*")
            with col_aud:
                audio_button(item['en'], f"aud_{bob_raqami}_{idx}")
            st.divider()

    # 2-TAB: Inglizcha berilib, o'zbekchasini yozish
    with tab2:
        st.subheader("✍️ Mashq: Inglizcha so'zning o'zbekcha ma'nosini yozing")
        with st.form(f"form_en_uz_{bob_raqami}"):
            yozma_ball_1 = 0
            javoblar_1 = []
            for i in range(min(5, len(hozirgi_sozlar))):
                item = hozirgi_sozlar[i]
                j = st.text_input(f"{i+1}. '{item['en']}' so'zining o'zbekcha ma'nosi nima?", key=f"en_uz_{bob_raqami}_{i}")
                javoblar_1.append((item, j))
            tekshir_1 = st.form_submit_button("Javoblarni tekshirish")
            
            if tekshir_1:
                for item, ans in javoblar_1:
                    if ans.strip().lower() in item['uz'].lower() and ans.strip() != "":
                        yozma_ball_1 += 1
                        st.success(f"To'g'ri: {item['en']} = {item['uz']} ✅")
                    else:
                        st.error(f"Xato yoki to'liq emas: {item['en']} ➔ To'g'risi: {item['uz']} ❌")
                st.info(f"Natija: {yozma_ball_1} / 5 to'g'ri!")

    # 3-TAB: O'zbekcha berilib, inglizchasini to'g'ri yozish
    with tab3:
        st.subheader("✍️ Mashq: O'zbekcha so'zning inglizcha tarjimasini yozing")
        with st.form(f"form_uz_en_{bob_raqami}"):
            yozma_ball_2 = 0
            javoblar_2 = []
            for i in range(min(5, len(hozirgi_sozlar))):
                item = hozirgi_sozlar[i]
                j = st.text_input(f"{i+1}. '{item['uz']}' so'zini inglizcha yozing:", key=f"uz_en_{bob_raqami}_{i}")
                javoblar_2.append((item, j))
            tekshir_2 = st.form_submit_button("Imloni tekshirish")
            
            if tekshir_2:
                for item, ans in javoblar_2:
                    if ans.strip().lower() == item['en'].lower():
                        yozma_ball_2 += 1
                        st.success(f"Barakalla: {item['uz']} = {item['en']} ✅")
                    else:
                        st.error(f"Noto'g'ri: {item['uz']} ➔ To'g'ri yozilishi: '{item['en']}' ❌")
                st.info(f"Natija: {yozma_ball_2} / 5 to'g'ri!")

    # 4-TAB: Bob oxiridagi test va Excel yuklash
    with tab4:
        st.subheader(f"📝 {tanlangan_bob} bo'yicha yakuniy test")
        
        with st.form(f"test_form_bob_{bob_raqami}"):
            ism = st.text_input("O'quvchi Ism va Familiyasi:", key=f"name_bob_{bob_raqami}", placeholder="Aliyev Vali")
            sinf = st.text_input("Sinfingiz:", key=f"class_bob_{bob_raqami}", placeholder="7-A")
            
            test_savollari = hozirgi_sozlar[:10]
            tanlovlar = []
            for i, q in enumerate(test_savollari):
                togri = q["uz"]
                # 3 ta boshqa noto'g'ri variant
                notogri_variantlar = [x["uz"] for x in hozirgi_sozlar if x["uz"] != togri]
                tanlangan_notogri = random.sample(notogri_variantlar, min(3, len(notogri_variantlar)))
                variantlar = [togri] + tanlangan_notogri
                random.seed(i + bob_raqami)
                random.shuffle(variantlar)
                
                ans = st.radio(f"{i+1}. '{q['en']}' so'zining to'g'ri tarjimasi qaysi?", variantlar, key=f"quiz_{bob_raqami}_{i}")
                tanlovlar.append((q, ans))
                
            testni_yakunla = st.form_submit_button("Testni topshirish va Natijani ko'rish 🎯")
            
            if testni_yakunla:
                if ism.strip() and sinf.strip():
                    togri_soni = sum(1 for q, user_a in tanlovlar if user_a == q["uz"])
                    jami_savol = len(test_savollari)
                    xato_soni = jami_savol - togri_soni
                    ball = int((togri_soni / jami_savol) * 100)
                    
                    st.balloons()
                    st.success("🎉 Test muvaffaqiyatli topshirildi!")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("To'g'ri javoblar", f"{togri_soni} ta")
                    c2.metric("Xato javoblar", f"{xato_soni} ta")
                    c3.metric("To'plangan ball", f"{ball} / 100")
                    
                    # Excel fayl
                    hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
                    natija_data = {
                        "Familiya va Ism": [ism],
                        "Sinf": [sinf],
                        "Bob": [tanlangan_bob],
                        "To'g'ri": [togri_soni],
                        "Xato": [xato_soni],
                        "Ball": [ball],
                        "Sana": [hozirgi_vaqt],
                        "Tuzuvchi": ["Quljanova Shukurjon Zaribovna"]
                    }
                    df = pd.DataFrame(natija_data)
                    st.dataframe(df, use_container_width=True)
                    
                    excel_buffer = BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Bob_Natija')
                    excel_data = excel_buffer.getvalue()
                    
                    st.download_button(
                        label="📥 Natijani Excel (.xlsx) formatida yuklab olish",
                        data=excel_data,
                        file_name=f"{ism}_{tanlangan_bob}_natija.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error("Iltimos, ism va sinfingizni to'liq kiriting!")

    # 5-TAB: 20-40 so'zdan iborat matn va audio
    with tab5:
        st.subheader("📖 Bob matni (Reading & Listening)")
        st.info("Ushbu matn 20–40 ta so'zdan iborat bo'lib, o'rganilgan mavzuni mustahkamlaydi.")
        
        col_t1, col_t2 = st.columns([4, 1])
        with col_t1:
            st.markdown(f"**🇬🇧 English text:**  \n### \"{standart_matn['en']}\"")
        with col_t2:
            st.write("Matn audiosi:")
            audio_button(standart_matn['en'], f"matn_aud_{bob_raqami}")
            
        st.divider()
        st.markdown(f"**🇺🇿 O'zbekcha tarjimasi:**  \n### \"{standart_matn['uz']}\"")

# =========================================================================
# 2-BO'LIM: MATEMATIKA TRENAJORI
# =========================================================================
elif asosiy_menyu == "🧮 Matematika Trenajori":
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
        st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
        st.title("🧮 Matematika Trenajori")
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
        st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
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

# =========================================================================
# 3-BO'LIM: INGLIZ TILI GRAMMATIKA
# =========================================================================
else:
    st.markdown('<div class="author-badge">✨ <b>Tuzuvchi:</b> Quljanova Shukurjon Zaribovna</div>', unsafe_allow_html=True)
    st.title("🇬🇧 English Grammar Tests")
    st.info("Grammatika testlari bo'yicha mashqlarni bajaring.")
