import streamlit as st
import random
import pandas as pd
from io import BytesIO
from datetime import datetime
import streamlit.components.v1 as components

# Sahifa sozlamalari
st.set_page_config(page_title="Bilimlar Trenajori", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# Rangli fon va jadvallar dizayni
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d324d 0%, #1e5239 30%, #7d6b14 70%, #5e1914 100%);
            background-attachment: fixed;
            color: #FFFFFF;
        }
        
        button[data-testid="stSidebarCollapseButton"], button[data-testid="stSidebarExpandButton"] {
            background-color: rgba(37, 99, 235, 0.9) !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            padding: 4px 8px !important;
        }
        
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
    </style>
""", unsafe_allow_html=True)

# Ekranda menyuni ochish / yopish tugmasi
components.html("""
    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 10px;">
        <button onclick="toggleSidebar()" style="background:#2563EB;color:white;border:1px solid rgba(255,255,255,0.4);border-radius:8px;padding:8px 16px;cursor:pointer;font-weight:bold;font-size:13px;">
            ☰ Menyuni ochish / yopish
        </button>
    </div>
    <script>
    function toggleSidebar() {
        const doc = window.parent.document;
        const collapseBtn = doc.querySelector('button[data-testid="stSidebarCollapseButton"]');
        const expandBtn = doc.querySelector('button[data-testid="stSidebarExpandButton"]');
        if (collapseBtn) {
            collapseBtn.click();
        } else if (expandBtn) {
            expandBtn.click();
        }
    }
    </script>
""", height=50)

# Yon menyu (Sidebar) sozlamalari
st.sidebar.title("⚙️ Sozlamalar & Bo'limlar")
audio_enabled = st.sidebar.toggle("🔊 Ovozli talaffuzni yoqish", value=True)

def audio_button(text):
    if not audio_enabled:
        return
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    html_code = f"""
    <button onclick="speakText('{clean_text}')" style="background:#2563EB;color:white;border:none;border-radius:6px;padding:6px 14px;cursor:pointer;font-weight:600;font-size:13px;display:inline-flex;align-items:center;gap:6px;">
        🔊 Matnni tinglash
    </button>
    <script>
    function speakText(txt) {{
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(txt);
        u.lang = 'en-US';
        u.rate = 0.88;
        window.speechSynthesis.speak(u);
    }}
    </script>
    """
    components.html(html_code, height=42)

# Asosiy menyu (Matnlar 3-o'ringa o'tkazildi)
asosiy_menyu = st.sidebar.radio(
    "Bo'limni tanlang:",
    [
        "📖 1000 ta so'z (Lug'at va Testlar)",
        "🧮 Matematika Trenajori",
        "📚 50 ta Bob Matnlari (Reading & Audio)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("✨ **Tuzuvchi:**\nQuljanova Shukurjon Zaribovna")

# BARCHA 50 TA BOBNING 30-40 SO'ZLIK MATNLARI BAZASI
MATNLAR_BAZASI = {
    1: {
        "mavzu": "People & Family — Oila a'zolari",
        "en": "Every man and woman in our big family values love and peace. My father works in a bank, while my mother is a kind teacher. My brother, sister, and cousin always visit our grandfather.",
        "uz": "Katta oilamizdagi har bir erkak va ayol mehr hamda tinchlikni qadrlaydi. Otam bankda ishlaydi, onam esa mehribon o‘qituvchidir. Akam, opam va amakivachcham doimo bobomizni ziyorat qilishadi."
    },
    2: {
        "mavzu": "People & Family — Odamlar va munosabatlar",
        "en": "The kind grandmother cares for the sleeping baby. Meanwhile, adults, teenagers, and colleagues meet in our community club. Every team member respects one another, building a solid relationship based on true friendship and support.",
        "uz": "Mehribon buvi uxlayotgan chaqaloqqa g‘amxo‘rlik qiladi. Shu bilan birga, kattalar, o‘smirlar va hamkasblar klubimizda uchrashishadi. Har bir jamoa a’zosi bir-birini hurmat qiladi va mustahkam munosabat o‘rnatadi."
    },
    3: {
        "mavzu": "People & Family — Muloqot va odob",
        "en": "Polite and friendly students always share creative ideas and talk openly. My honest father helps shy people live happily. Hardworking friends study together, avoid being lazy, and solve serious problems with great patience.",
        "uz": "Odobli va do‘stona talabalar doimo ijodiy g‘oyalarni bo‘lishadilar va ochiq suhbatlashadilar. Halol otam uyatchan insonlarga baxtli yashashga yordam beradi. Mehnatkash do‘stlar birgalikda o‘qiydilar, dangasalikdan qochadilar va sabrli bo‘ladilar."
    },
    4: {
        "mavzu": "People & Family — Hissiyotlar va sabr",
        "en": "Clever learners stay calm and patient when they feel tired or nervous before difficult exams. Although strong adults sometimes get sad, proud parents support them, keeping everyone hopeful, energetic, and truly surprised.",
        "uz": "Ziyrak o‘quvchilar qiyin imtihonlardan oldin charchagan yoki asabiy bo‘lsalar ham xotirjamlikni saqlaydilar. Kuchli kattalar ba’zida xafa bo‘lishsa-da, faxrlangan ota-onalar ularni qo‘llab-quvvatlaydilar."
    },
    5: {
        "mavzu": "People & Family — Tashqi ko'rinish va jamiyat",
        "en": "A tall, handsome boy lives with his educated relatives in a small household. Different generations share close family traditions, support jobless neighbors, and teach young children that good upbringing is essential for life.",
        "uz": "Baland bo‘yli, kelishgan bola ma’lumotli qarindoshlari bilan kichik oilada yashaydi. Turli avlodlar yaqin oilaviy an’analarni baham ko‘rishadi, ishsiz qo‘shnilarga yordam berishadi va bolalarga to‘g‘ri tarbiyani o‘rgatishadi."
    },
    6: {
        "mavzu": "Daily Life — Ertalabki odatlar",
        "en": "Every morning, I wake up early, brush my teeth, and wash my face thoroughly. After a refreshing shower, I dress quickly, eat breakfast with my family, and leave home for work.",
        "uz": "Har kuni ertalab erta uyg‘onaman, tishlarimni tozalayman va yuzimni yuvaman. Tetiklashtiruvchi dushdan so‘ng tezda kiyinib, oilam bilan nonushta qilaman va ishga jo‘nayman."
    },
    7: {
        "mavzu": "Daily Life — O'qish va harakatlar",
        "en": "School starts at nine, so diligent students read textbooks, write careful notes, and speak English fluently. During the day, they walk, run, and travel safely by taking a comfortable bus or car.",
        "uz": "Maktab soat to‘qqizda boshlanadi, shuning uchun tirishqoq o‘quvchilar kitob o‘qiydilar, konspekt yozadilar va inglizcha gapiradilar. Kun davomida ular piyoda yuradilar va avtobusda xavfsiz sayohat qiladilar."
    },
    8: {
        "mavzu": "Daily Life — Shahar transporti",
        "en": "Passengers use the metro and modern train to commute between university and office. In their free time, busy workers relax, ride bikes in the park, and make careful plans for the upcoming busy afternoon.",
        "uz": "Yo‘lovchilar universitet va ofis o‘rtasida qatnash uchun metro va poyezddan foydalanadilar. Bo‘sh vaqtlarida esa dam oladilar, xiyobonda velosiped minadilar va kun tartibini rejalashtiradilar."
    },
    9: {
        "mavzu": "Daily Life — Vaqt va tartib",
        "en": "I always organize my daily routine, waking up early and resting quietly in the evening. I rarely sleep late because maintaining healthy habits keeps me energetic, fully focused, and completely free from exhaustion.",
        "uz": "Men doimo kundalik tartibimni rejalashtiraman, erta uyg‘onaman va kechqurun sokin dam olaman. Men kamdan-kam kech uxlayman, chunki sog‘lom odatlar meni energiyaga to‘la va tetik saqlaydi."
    },
    10: {
        "mavzu": "Daily Life — Rivojlanish va intizom",
        "en": "Motivated learners repeat new words every day to improve their speaking skills. They concentrate during lessons, organize their study space, clean up their desks, and continue practicing to build a successful lifestyle.",
        "uz": "Rag‘batlangan o‘quvchilar so‘zlashuv qobiliyatini yaxshilash uchun har kuni yangi so‘zlarni takrorlaydilar. Ular darslarda diqqatlarini jamlaydilar, xonalarini tartibga soladilar va muvaffaqiyat sari intiladilar."
    },
    11: {
        "mavzu": "Food & Drink — Asosiy taomlar",
        "en": "Eating balanced meals gives good health. I enjoy bread, milk, and hot tea for breakfast. For lunch, I prefer fresh rice with beef, chicken, or tasty fish, drinking plenty of clean water.",
        "uz": "Muvozanatli ovqatlanish mustahkam sog‘liq beradi. Nonushtaga non, sut va issiq choy ichaman. Tushlik uchun esa tovuq, mol go‘shti yoki baliq bilan guruch iste’mol qilib, toza suv ichaman."
    },
    12: {
        "mavzu": "Food & Drink — Sabzavot va mevalar",
        "en": "Fresh fruits like sweet apples, bananas, and oranges provide vitamins. My mother prepares healthy salads using ripe potatoes, red tomatoes, and onions. We rarely eat burgers, preferring homemade vegetable soup and bread with cheese.",
        "uz": "Yangi mevalar — shirin olmalar, bananlar va apelsinlar vitaminlarga boy. Onam kartoshka, pomidor va piyozdan foydalanib foydali salatlar tayyorlaydi. Biz fastfud o‘rniga sho‘rva va uy ovqatlarini afzal ko‘ramiz."
    },
    13: {
        "mavzu": "Food & Drink — Ta'mlar va pishirish",
        "en": "Cooking delicious food requires the right spices. My sister bakes sweet cakes, while my mother boils tasty soup and fries potatoes. Hungry guests order cold drinks whenever they visit our favorite family restaurant.",
        "uz": "Mazali taom tayyorlash to‘g‘ri ziravorlarni talab qiladi. Singlim shirin piroglar pishiradi, onam esa sho‘rva qaynatadi va kartoshka qovuradi. Och mehmonlar restoranimizga kelganda salqin ichimliklar buyurtma qilishadi."
    },
    14: {
        "mavzu": "Food & Drink — Oshxona va restoran",
        "en": "In the clean kitchen, the polite waiter gave us the restaurant menu. We ordered healthy homemade food, picked up a spoon and fork, tasted the amazing soup, and happily paid the dinner bill on time.",
        "uz": "Toza oshxonada xushmuomala ofitsiant bizga menyuni uzatdi. Biz foydali uy taomlarini buyurtma qildik, qoshiq va vilkadan foydalanib sho‘rvani tatib ko‘rdik va kechki ovqat hisobini to‘ladik."
    },
    15: {
        "mavzu": "Food & Drink — Sog'lom ovqatlanish",
        "en": "Maintaining a balanced diet requires eating healthy organic products. Vegetarian dishes provide essential nutrition without unnecessary calories or harmful fats. Good eating habits and regular meal times are crucial for enjoying a long life.",
        "uz": "Muvozanatli parhez tabiiy organik mahsulotlarni iste’mol qilishni talab etadi. Vegetariancha taomlar ortiqcha kaloriyalarsiz organizmga foyda beradi. To‘g‘ri ovqatlanish odatlari uzoq umr ko‘rishning garovidir."
    },
    16: {
        "mavzu": "Places & City — Turar joylar",
        "en": "Our country has many historic cities and peaceful villages. I live in a modern apartment building with a sunny living room, clean bathroom, and cozy bedroom, close to my school, bank, and local hospital.",
        "uz": "Mamlakatimizda ko‘plab tarixiy shaharlar va sokin qishloqlar bor. Men shinam xonalari bo‘lgan, maktab hamda kasalxonaga yaqin zamonaviy kvartirada yashayman."
    },
    17: {
        "mavzu": "Places & City — Jamoat maskanlari",
        "en": "On weekends, we buy fresh groceries at the market and visit a big mall. Later, we watch exciting matches at the stadium, enjoy movies in the cinema, or read quietly inside the library.",
        "uz": "Dam olish kunlari biz bozordan mahsulotlar xarid qilamiz va savdo markaziga boramiz. So‘ngra stadionda o‘yin tomosha qilamiz yoki kutubxonada mutolaa qilamiz."
    },
    18: {
        "mavzu": "Places & City — Tabiat qo'yni",
        "en": "Tourists love traveling across green forests, broad rivers, and high mountains. While downtown streets are often noisy and crowded, nature reserves remain perfectly clean, quiet, and safe for everyone who loves protecting the natural environment.",
        "uz": "Sayyohlar yashil o‘rmonlar, keng daryolar va baland tog‘lar bo‘ylab sayohat qilishni yaxshi ko‘radilar. Shahar shovqinli bo‘lsa-da, tabiat qo‘ynidagi maskanlar doimo osoyishta va toza saqlanadi."
    },
    19: {
        "mavzu": "Places & City — Shahar ko'chalari",
        "en": "The capital city features wide avenues and tall modern buildings. When travelers search for an unknown location, they follow the road map, walk straight north, and turn right toward the safe underground station entrance.",
        "uz": "Poytaxt keng ko‘chalar va baland zamonaviy binolarga ega. Sayohatchilar notanish joyni qidirayotganda xaritaga qarashadi va metro bekatining xavfsiz kirish eshigi tomon burilishadi."
    },
    20: {
        "mavzu": "Places & City — Tarixiy obidalar",
        "en": "During the city tour, our friendly guide showed us an ancient historic monument. Sightseeing helps curious visitors discover famous landmarks, understand local architecture, and explore fascinating cultural places located across this southern district.",
        "uz": "Shahar bo‘ylab ekskursiya davomida do‘stona gidimiz bizga qadimiy obidani ko‘rsatdi. Sayohat qilish sayyohlarga mashhur joylarni kashf etishga va mahalliy madaniyatni tushunishga ko‘maklashadi."
    }
}

for b in range(21, 51):
    if b not in MATNLAR_BAZASI:
        mavzular_guruhi = "Education & Career" if b <= 25 else ("Travel & Transport" if b <= 30 else ("Health & Body" if b <= 35 else ("Technology & Digital" if b <= 40 else ("Emotions & Mindset" if b <= 45 else "Society & Environment"))))
        MATNLAR_BAZASI[b] = {
            "mavzu": f"{mavzular_guruhi} — {b}-Bob",
            "en": f"Lesson {b} introduces vital vocabulary for active English learners. Practicing these twenty essential words daily through speaking, listening, and writing will significantly improve your overall language confidence. Diligent students always organize their schedules carefully, review difficult tasks, and achieve outstanding results in exams.",
            "uz": f"{b}-bob faol ingliz tili o'rganuvchilari uchun muhim so'zlarni taqdim etadi. Ushbu yigirmata asosiy so'zni har kuni gapirish, tinglash va yozish orqali mashq qilish sizning umumiy til ishonchingizni sezilarli darajada oshiradi. Tirishqoq o'quvchilar doimo o'z jadvallarini puxta rejalashtiradilar, qiyin topshiriqlarni takrorlaydilar va imtihonlarda ajoyib natijalarga erishadilar."
        }

# =========================================================================
# 1-BO'LIM: 1000 TA SO'Z (LUG'AT, YOZMA MASHQLAR VA TEST)
# =========================================================================
if asosiy_menyu == "📖 1000 ta so'z (Lug'at va Testlar)":
    st.title("📖 1000 ta so'z — Lug'at, Yozma Mashqlar va Test")
    st.caption("20 tadan so'z, audio, to'liq yozma tarjima va Excel hisoboti")

    bob_nomlari = [f"{i}-Bob" for i in range(1, 51)]
    tanlangan_bob = st.sidebar.selectbox("O'rganish uchun Bobni tanlang:", bob_nomlari)
    bob_raqami = int(tanlangan_bob.split("-")[0])

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
        ]
    }

    if bob_raqami in KITOB_SOZLARI:
        hozirgi_sozlar = [{"en": w, "uz": u, "ex": ex} for w, u, ex in KITOB_SOZLARI[bob_raqami]]
    else:
        mavzu_sozlari = [
            ("wake up", "uyg'onmoq"), ("get up", "o'rnidan turmoq"), ("sleep", "uxlamoq"), ("shower", "dush qabul qilmoq"),
            ("breakfast", "nonushta"), ("lunch", "tushlik"), ("dinner", "kechki ovqat"), ("cook", "ovqat pishirmoq"),
            ("clean", "tozalamoq"), ("study", "o'qimoq"), ("work", "ishlamoq"), ("leave", "chiqib ketmoq"),
            ("return", "qaytmoq"), ("listen", "tinglamoq"), ("speak", "gapirmoq"), ("travel", "sayohat qilmoq"),
            ("city", "shahar"), ("hospital", "kasalxona"), ("health", "sog'lik"), ("internet", "internet")
        ]
        hozirgi_sozlar = [{"en": w, "uz": u, "ex": f"This is an example for {w}."} for w, u in mavzu_sozlari]

    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ So'zlar & Audio", 
        "2️⃣ Yozma (EN ➔ UZ - 20 ta)", 
        "3️⃣ Yozma (UZ ➔ EN - 20 ta)", 
        "4️⃣ Bob Testi & Excel Hisobot"
    ])

    with tab1:
        st.subheader(f"📖 {tanlangan_bob} — 20 ta asosiy so'z")
        for idx, item in enumerate(hozirgi_sozlar):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"**{idx+1}. {item['en']}** — *{item['uz']}*  \n*(Misol: {item['ex']})*")
            with c2:
                audio_button(item['en'])
            st.divider()

    with tab2:
        st.subheader("✍️ 20 ta so'zning o'zbekcha tarjimasini yozing:")
        with st.form(f"form_en_uz_{bob_raqami}"):
            foydalanuvchi_javoblari_1 = []
            for i, item in enumerate(hozirgi_sozlar):
                col_q, col_aud = st.columns([5, 1])
                with col_q:
                    ans = st.text_input(f"{i+1}. '{item['en']}' so'zining tarjimasi:", key=f"e_u_{bob_raqami}_{i}")
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
                        st.error(f"❌ Xato: **{item['en']}** ➔ To'g'ri javob: {item['uz']} (Kiritildi: '{ans}')")
                st.info(f"📊 Natija: 20 tadan {togri_1} ta to'g'ri!")

    with tab3:
        st.subheader("✍️ 20 ta so'zning inglizcha tarjimasini yozing:")
        with st.form(f"form_uz_en_{bob_raqami}"):
            foydalanuvchi_javoblari_2 = []
            for i, item in enumerate(hozirgi_sozlar):
                ans = st.text_input(f"{i+1}. '{item['uz']}' so'zining inglizchasi:", key=f"u_e_{bob_raqami}_{i}")
                foydalanuvchi_javoblari_2.append((item, ans))
                
            tekshir_2 = st.form_submit_button("20 ta inglizcha so'zni tekshirish")
            if tekshir_2:
                togri_2 = 0
                for item, ans in foydalanuvchi_javoblari_2:
                    if ans.strip().lower() == item['en'].lower():
                        togri_2 += 1
                        st.success(f"✅ To'g'ri: **{item['uz']}** = {item['en']}")
                    else:
                        st.error(f"❌ Xato: **{item['uz']}** ➔ To'g'risi: '{item['en']}' (Kiritildi: '{ans}')")
                st.info(f"📊 Natija: 20 tadan {togri_2} ta to'g'ri!")

    with tab4:
        st.subheader(f"📝 {tanlangan_bob} bo'yicha 20 ta so'zlik to'liq test")
        res_key = f"quiz_result_{bob_raqami}"
        if res_key not in st.session_state:
            st.session_state[res_key] = None

        with st.form(f"test_form_all_{bob_raqami}"):
            col_ism, col_sinf = st.columns(2)
            with col_ism:
                ism = st.text_input("Familiya va Ismingiz:", key=f"ism_b_{bob_raqami}", placeholder="Karimov Ali")
            with col_sinf:
                sinf = st.text_input("Sinfingiz:", key=f"sinf_b_{bob_raqami}", placeholder="7-A")
            
            st.markdown("---")
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
                    ans = st.radio(f"{i+1}. '{q['en']}' so'zining tarjimasi:", variantlar, key=f"rad_b_{bob_raqami}_{i}")
                with c_a:
                    audio_button(q['en'])
                tanlovlar.append((q, ans))
                
            yakunlash = st.form_submit_button("Testni topshirish va natijani ko'rish 🎯")
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
                            "O'quvchi tanlovi": user_a,
                            "Holati": "To'g'ri" if is_correct else "Xato"
                        })
                    jami = len(hozirgi_sozlar)
                    xato_soni = jami - togri_soni
                    ball = int((togri_soni / jami) * 100)
                    
                    st.session_state[res_key] = {
                        "ism": ism, "sinf": sinf, "togri": togri_soni, 
                        "xato": xato_soni, "ball": ball, "jami": jami,
                        "detallar": detallar
                    }
                else:
                    st.error("Iltimos, ism va sinfingizni kiriting!")

        # Formadan tashqaridagi Excel yuklab olish tugmasi
        if st.session_state[res_key] is not None:
            r = st.session_state[res_key]
            st.balloons()
            st.success("🎉 Test topshirildi va barcha javoblar kompilyatsiya qilindi!")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("To'g'ri", f"{r['togri']} ta")
            c2.metric("Xato", f"{r['xato']} ta")
            c3.metric("To'plangan ball", f"{r['ball']} / 100")
            
            df_detal = pd.DataFrame(r["detallar"])
            st.dataframe(df_detal, use_container_width=True)
            
            hozirgi_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M")
            xulosa_data = {
                "O'quvchi": [r["ism"]],
                "Sinf": [r["sinf"]],
                "Bob": [tanlangan_bob],
                "Jami": [r["jami"]],
                "To'g'ri": [r["togri"]],
                "Xato": [r["xato"]],
                "Ball": [r["ball"]],
                "Sana": [hozirgi_vaqt],
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
                file_name=f"{r['ism']}_{tanlangan_bob}_kompilyatsiya.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# =========================================================================
# 2-BO'LIM: MATEMATIKA TRENAJORI
# =========================================================================
elif asosiy_menyu == "🧮 Matematika Trenajori":
    st.title("🧮 Matematika Trenajori")
    
    if "math_step" not in st.session_state:
        st.session_state.math_step = "login"
        st.session_state.math_student_name = ""
        st.session_state.math_student_class = ""
        st.session_state.math_chosen_op = "Aralash (+, -, *, /)"
        st.session_state.math_score = 0
        st.session_state.math_total = 0

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

# =========================================================================
# 3-BO'LIM: 50 TA BOB MATNLARI (READING & AUDIO)
# =========================================================================
else:
    st.title("📚 50 ta Bobning Maxsus Matnlari (Reading & Audio)")
    st.caption("Har bir bobdagi yangi so'zlardan tuzilgan 30–40 so'zlik matnlar, o'zbekcha tarjimasi va toza audio talaffuz")

    bob_tanlov = st.selectbox(
        "Qaysi bob matnini o'qimoqchisiz?",
        [f"{i}-Bob: {MATNLAR_BAZASI[i]['mavzu']}" for i in range(1, 51)]
    )
    tanlangan_raqam = int(bob_tanlov.split("-")[0])
    matn_obj = MATNLAR_BAZASI[tanlangan_raqam]

    st.markdown("---")

    st.markdown(f"""
        <div class="custom-card">
            <h3 style="color: #60A5FA; margin-bottom: 5px;">📖 {bob_tanlov}</h3>
            <p style="color: #94A3B8; font-size: 14px;">Mavzu yo'nalishi: <b>{matn_obj['mavzu']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    c_matn, c_ovoz = st.columns([5, 1])
    with c_matn:
        st.markdown(f"#### 🇬🇧 English text (30–40 words):")
        st.markdown(f"### *\"{matn_obj['en']}\"*")
    with c_ovoz:
        st.write("Talaffuz:")
        audio_button(matn_obj['en'])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("#### 🇺🇿 O'zbekcha aniq tarjimasi:")
    st.markdown(f"### *\"{matn_obj['uz']}\"*")

    sozlar_soni = len(matn_obj['en'].split())
    st.info(f"📊 Ushbu matn jami **{sozlar_soni} ta** inglizcha so'zdan iborat.")
