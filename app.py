import streamlit as st
import pandas as pd
import time
from datetime import date

# إعدادات الصفحة (يجب أن تكون في أول سطر)
st.set_page_config(page_title="برنامج تأهيل الركبة الشامل", page_icon="🦵", layout="wide")

# ==========================================
# 1. إعداد قاعدة البيانات المؤقتة لحفظ التقدم
# ==========================================
if 'progress_data' not in st.session_state:
    st.session_state.progress_data = pd.DataFrame(columns=['Date', 'Pain_Level', 'Completed'])

if 'days_completed' not in st.session_state:
    st.session_state.days_completed = 0

total_days = 42 # 6 أسابيع

# دالة التنبيه الصوتي
def play_sound():
    audio_html = """
    <audio autoplay>
    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ==========================================
# 2. القائمة الجانبية (Sidebar)
# ==========================================
st.sidebar.title("🦵 تأهيل الركبة")
menu = st.sidebar.radio("اختر الصفحة:", ["🏋️‍♂️ التمارين اليومية", "📊 لوحة متابعة التعافي"])

# بيانات التمارين مع روابط للصور المتحركة (GIFs)
exercises = {
    "1. الانقباض الثابت (Quad Sets)": {
        "desc": "اضغط بركبتك لأسفل بقوة على منشفة لشد العضلة الأمامية للفخذ دون تحريك المفصل. هذا التمرين آمن جداً للغضروف.",
        "reps": "10 تكرارات",
        "hold_time": 10,
        "gif": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG1mNnFwZzNnM2p6M2N5ZnpwYno4dnhxdXJvMXQ3Z2RteHJyeDZpZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKW6HwUoG2Q8TII/giphy.gif" # مثال لصورة متحركة
    },
    "2. رفع الساق المستقيمة (Straight Leg Raise)": {
        "desc": "استلقِ وافرد ركبتك المصابة تماماً (أصابع القدم لأعلى)، ثم ارفعها لمستوى الركبة الأخرى المثنية.",
        "reps": "3 مجموعات × 10 تكرارات",
        "hold_time": 5,
        "gif": "https://media.giphy.com/media/l41Ys1fQky5raqvMQ/giphy.gif" 
    },
    "3. تمرين الكوبري (Glute Bridge)": {
        "desc": "استلقِ واثنِ ركبتيك. ارفع حوضك لأعلى حتى يشكل جسمك خطاً مستقيماً، مع شد الأرداف بقوة.",
        "reps": "3 مجموعات × 10 تكرارات",
        "hold_time": 3,
        "gif": "https://media.giphy.com/media/xT8qBvH1pAhtfKVepq/giphy.gif"
    },
    "4. تمرين المحارة الجانبي (Clamshells)": {
        "desc": "نم على جانبك واثنِ ركبتيك معاً. ارفع ركبتك العلوية لأعلى دون تحريك الحوض للوراء.",
        "reps": "3 مجموعات × 10 تكرارات لكل ساق",
        "hold_time": 3,
        "gif": "https://media.giphy.com/media/3o7btT1T9dpzYWeU2Q/giphy.gif"
    }
}

# ==========================================
# 3. صفحة التمارين
# ==========================================
if menu == "🏋️‍♂️ التمارين اليومية":
    st.title("جلسة التمارين اليومية")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_exercise = st.selectbox("📌 اختر التمرين لنبدأ:", list(exercises.keys()))
        exercise_data = exercises[selected_exercise]
        
        st.info(exercise_data["desc"])
        st.write(f"**العدد المطلوب:** {exercise_data['reps']}")
        
        # المؤقت الزمني
        if st.button(f"⏱️ ابدأ عد {exercise_data['hold_time']} ثوانٍ للثبات"):
            timer_placeholder = st.empty()
            for i in range(exercise_data["hold_time"], 0, -1):
                timer_placeholder.header(f"⏳ {i}")
                time.sleep(1)
            timer_placeholder.success("✅ ممتاز! استرخِ ثم كرر.")
            play_sound()

    with col2:
        # عرض الصورة المتحركة للتمرين
        st.image(exercise_data["gif"], caption="شكل توضيحي للتمرين", use_container_width=True)

    st.markdown("---")
    st.subheader("تسجيل إتمام اليوم")
    pain_level = st.slider("كيف تقيم مستوى الألم في ركبتك اليوم قبل التمرين؟ (0 = بدون ألم، 10 = ألم شديد)", 0, 10, 5)
    
    if st.button("✅ لقد أتممت جميع تمارين اليوم!"):
        today_date = date.today().strftime("%Y-%m-%d")
        new_data = pd.DataFrame({'Date': [today_date], 'Pain_Level': [pain_level], 'Completed': [True]})
        st.session_state.progress_data = pd.concat([st.session_state.progress_data, new_data], ignore_index=True)
        
        if st.session_state.days_completed < total_days:
            st.session_state.days_completed += 1
            st.balloons()
            st.success("عاش! تم حفظ بيانات اليوم بنجاح في لوحة المتابعة.")
        else:
            st.success("ألف مبروك! لقد أنهيت البرنامج العلاجي بالكامل.")

# ==========================================
# 4. صفحة لوحة البيانات (Dashboard)
# ==========================================
elif menu == "📊 لوحة متابعة التعافي":
    st.title("لوحة تحليل البيانات ومتابعة التعافي")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="الأيام المنجزة", value=f"{st.session_state.days_completed} / {total_days}")
    with col_b:
        progress_percent = int((st.session_state.days_completed / total_days) * 100)
        st.metric(label="نسبة إتمام البرنامج", value=f"{progress_percent}%")
    
    st.progress(st.session_state.days_completed / total_days)
    st.markdown("---")
    
    st.subheader("📉 منحنى الألم على مدار الأيام")
    if not st.session_state.progress_data.empty:
        # رسم بياني تفاعلي يوضح تغير مستوى الألم
        chart_data = st.session_state.progress_data.set_index('Date')['Pain_Level']
        st.line_chart(chart_data)
        st.write("الجدول الزمني للبيانات:")
        st.dataframe(st.session_state.progress_data)
    else:
        st.warning("لم تقم بتسجيل أي تمارين بعد. ابدأ التمرين اليوم لرؤية الرسم البياني!")
