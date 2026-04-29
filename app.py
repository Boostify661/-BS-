import streamlit as st
import subprocess
import os
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="BS PRO | High Quality", layout="centered", page_icon="🚀")

# تصميم أنيق وخفيف
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; border-radius: 12px; height: 3.5em; width: 100%;
        font-weight: bold; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.01); box-shadow: 0 4px 15px rgba(0,212,255,0.3); }
    .stProgress > div > div > div > div { background-color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام الأكواد (10 أكواد) ---
if "codes_db" not in st.session_state:
    st.session_state["codes_db"] = {
        "BS-7710": None, "BS-8820": None, "BS-9930": None,
        "PRO-TIK-1": None, "PRO-TIK-2": None, "VIP-MASTER": None,
        "BS-SPEED-1": None, "BS-SPEED-2": None, "GOLD-USER": None, "PREMIUM-BS": None
    }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- 3. بوابة الدخول ---
if not st.session_state["authenticated"]:
    st.title("🔐 دخول المحرك")
    code_input = st.text_input("كود التفعيل الخاص بك", type="password")
    if st.button("تفعيل الدخول ✨"):
        dev = st.context.headers.get("User-Agent")
        if code_input in st.session_state["codes_db"]:
            if st.session_state["codes_db"][code_input] in [None, dev]:
                st.session_state["codes_db"][code_input] = dev
                st.session_state["authenticated"] = True
                st.rerun()
            else: st.error("⚠️ هذا الكود مفعّل على جهاز آخر")
        else: st.error("❌ كود غير صحيح")
    st.stop()

# --- 4. المحرك الاحترافي ---
st.title("🚀 محرك BS للسرعة والجودة")
st.caption("إصدار V3.0 - نظام معالجة الإطارات المباشر")

uploaded_file = st.file_uploader("ارفع مقطعك هنا (MP4/MOV)", type=["mp4", "mov"])

if uploaded_file:
    size_mb = uploaded_file.size / (1024*1024)
    st.info(f"📁 حجم الملف: {size_mb:.1f} MB")
    
    if st.button("🚀 بدء المعالجة الاحترافية"):
        input_p = "input_video.mp4"
        output_p = "BS_60FPS_HD.mp4"
        
        # تنظيف الملفات القديمة
        for f in [input_p, output_p]:
            if os.path.exists(f): os.remove(f)

        with open(input_p, "wb") as f:
            f.write(uploaded_file.getbuffer())

        bar = st.progress(0)
        status = st.empty()
        
        # أمر FFmpeg المطور (توازن الجودة والرام)
        cmd = [
            'ffmpeg', '-y', '-i', input_p,
            '-vf', "setpts=2.0*PTS",    # تبطيء الفيديو
            '-r', '60',                 # 60 إطار
            '-c:v', 'libx264', 
            '-crf', '20',               # جودة عالية جداً (صافي)
            '-preset', 'ultrafast',     # سرعة قصوى لتوفير الرام
            '-pix_fmt', 'yuv420p',
            '-tune', 'zerolatency',     # معالجة مباشرة بدون تراكم في الرام
            '-movflags', '+faststart',
            output_p
        ]
        
        try:
            status.info("⚙️ جاري ضخ الجودة... يرجى عدم إغلاق الصفحة")
            bar.progress(30)
            
            # تشغيل المعالجة
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                bar.progress(100)
                status.success("✅ اكتملت المعالجة بنجاح!")
                st.balloons()
                
                with open(output_p, "rb") as f:
                    st.download_button(
                        label="📥 تحميل الفيديو المعدل",
                        data=f,
                        file_name="BS_Pro_60FPS.mp4",
                        mime="video/mp4"
                    )
                # حذف الملف الأصلي لتوفير مساحة السيرفر
                os.remove(input_p)
            else:
                st.error("فشل السيرفر في تحمل حجم الملف الكبير. حاول بمقطع أقصر.")
        except Exception as e:
            st.error("حدث خطأ تقني في الذاكرة.")

# --- 5. التذييل (حسابك) ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: #161b22; border-radius: 10px;">
        <a href="https://www.tiktok.com/@BoostifySt0re" target="_blank" style="text-decoration: none; color: white;">
            <strong>📱 تابعنا على تيك توك: BoostifySt0re</strong>
        </a>
    </div>
    """, unsafe_allow_html=True)
