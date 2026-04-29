import streamlit as st
import subprocess
import os
import time

# 1. إعدادات خفيفة جداً للهوية
st.set_page_config(page_title="BS Light Engine", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #222, #444);
        color: white; border-radius: 10px; height: 3em; width: 100%;
    }
    .stProgress > div > div > div > div { background-color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

# 2. الأكواد (قائمة مخففة)
if "codes_db" not in st.session_state:
    st.session_state["codes_db"] = {
        "BS-7710": None, "BS-8820": None, "BS-9930": None,
        "PRO-TIK-1": None, "PRO-TIK-2": None, "VIP-MASTER": None,
        "BS-SPEED-1": None, "BS-SPEED-2": None, "GOLD-USER": None, "PREMIUM-BS": None
    }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. نظام الدخول
if not st.session_state["authenticated"]:
    st.title("🔐 دخول BS")
    code_input = st.text_input("كود التفعيل", type="password")
    if st.button("دخول"):
        dev = st.context.headers.get("User-Agent")
        if code_input in st.session_state["codes_db"]:
            if st.session_state["codes_db"][code_input] in [None, dev]:
                st.session_state["codes_db"][code_input] = dev
                st.session_state["authenticated"] = True
                st.rerun()
            else: st.error("الجهاز مسجل مسبقاً")
        else: st.error("كود خطأ")
    st.stop()

# 4. محرك المعالجة الخفيف
st.title("🚀 BS Video Light")
st.caption("تم تحسين هذه النسخة للملفات الكبيرة")

uploaded_file = st.file_uploader("ارفع الفيديو هنا", type=["mp4", "mov"])

if uploaded_file:
    st.write(f"📁 تم اختيار مقطع بحجم: {uploaded_file.size / (1024*1024):.1f} MB")
    
    if st.button("بدء المعالجة السريعة"):
        input_path = "i.mp4"
        output_path = "o.mp4"
        
        # مسح أي ملفات قديمة لزيادة المساحة
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        bar = st.progress(0)
        msg = st.empty()
        
        # أمر معالجة "اقتصادي" جداً للرام
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', "setpts=2.0*PTS", '-r', '30', # خففنا الفريمات لـ 30 لضمان عدم الانهيار
            '-c:v', 'libx264', '-crf', '28',    # جودة مقبولة بضغط عالي
            '-preset', 'ultrafast',             # أقل استهلاك للرام
            '-pix_fmt', 'yuv420p',
            '-maxrate', '1M', '-bufsize', '2M', # سقف استهلاك الذاكرة
            output_path
        ]
        
        try:
            msg.info("⚙️ جاري المعالجة النظيفة...")
            bar.progress(50)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                bar.progress(100)
                st.success("✅ جاهز للتحميل!")
                with open(output_path, "rb") as f:
                    st.download_button("📥 تحميل الفيديو", f, "BS_Result.mp4")
                
                # تنظيف فوري بعد انتهاء العملية
                os.remove(input_path)
            else:
                st.error("السيرفر لم يتحمل حجم الملف. حاول بمقطع أصغر قليلاً.")
        except Exception as e:
            st.error("فشل في الذاكرة.")

st.markdown("---")
st.write(f"[TikTok: BoostifySt0re](https://www.tiktok.com/@BoostifySt0re)")
