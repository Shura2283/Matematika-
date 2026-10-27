import streamlit as st
import random

st.set_page_config(page_title="Matematika Trenajori", page_icon="🧮", layout="centered")

st.title("🧮 Matematika Trenajori")
st.write("25 ta misol yeching va to'plagan ballingizni biling (Har bir to'g'ri javob: 4 ball)!")

# Holatlarni (session state) saqlash
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(1, 20)
    st.session_state.num2 = random.randint(1, 20)
    st.session_state.operation = random.choice(["+", "-", "*"])
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.last_result = None

def yangi_savol():
    st.session_state.num1 = random.randint(1, 20)
    st.session_state.num2 = random.randint(1, 20)
    st.session_state.operation = random.choice(["+", "-", "*"])

def qayta_boshlash():
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.last_result = None
    yangi_savol()

# 25 ta misol to'lganini tekshirish
if st.session_state.total >= 25:
    togri = st.session_state.score
    xato = 25 - togri
    ball = togri * 4

    st.success("🎉 **Test yakunlandi!**")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("To'g'ri javoblar", f"{togri} ta")
    col2.metric("Xato javoblar", f"{xato} ta")
    col3.metric("To'plangan ball", f"{ball} / 100")

    if ball >= 86:
        st.balloons()
        st.info("A'lo natija! Barakalla! 🌟")
    elif ball >= 70:
        st.info("Yaxshi natija! 👍")
    else:
        st.warning("Yana mashq qilish tavsiya etiladi! 💪")

    if st.button("Qaytadan boshlash 🔄"):
        qayta_boshlash()
        st.rerun()

else:
    # Hali 25 ta bo'lmagan holatda trenajor davom etadi
    n1 = st.session_state.num1
    n2 = st.session_state.num2
    op = st.session_state.operation

    if op == "+":
        togri_javob = n1 + n2
    elif op == "-":
        togri_javob = n1 - n2
    else:
        togri_javob = n1 * n2

    # Hozirgi statistika
    col1, col2 = st.columns(2)
    col1.metric("Misol raqami", f"{st.session_state.total + 1} / 25")
    col2.metric("Joriy to'g'ri javoblar", f"{st.session_state.score}")

    st.markdown("---")

    # Oldingi berilgan javob natijasini ko'rsatish
    if st.session_state.last_result:
        status, msg = st.session_state.last_result
        if status == "success":
            st.success(msg)
        else:
            st.error(msg)

    st.subheader(f"Misolni yeching: **{n1} {op} {n2} = ?**")

    with st.form("javob_formasi", clear_on_submit=True):
        foydalanuvchi_javobi = st.number_input("Javobingizni kiriting:", step=1, value=None, placeholder="Son kiriting...")
        yuborish = st.form_submit_button("Javobni tasdiqlash")

        if yuborish:
            if foydalanuvchi_javobi is not None:
                st.session_state.total += 1
                if int(foydalanuvchi_javobi) == togri_javob:
                    st.session_state.score += 1
                    st.session_state.last_result = ("success", f"To'g'ri! 🎉 ({n1} {op} {n2} = {togri_javob})")
                else:
                    st.session_state.last_result = ("error", f"Noto'g'ri! ❌ To'g'ri javob: {togri_javob} edi")
                
                yangi_savol()
                st.rerun()
            else:
                st.warning("Iltimos, avval javobni yozing!")

    if st.button("Testni boshidan boshlash"):
        qayta_boshlash()
        st.rerun()
