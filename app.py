import streamlit as st
import subprocess
import os
import shutil
import time

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="BS PRO | Video Engine", layout="centered", page_icon="🚀")

# CSS لتصميم احترافي (Dark Mode + التعديلات الجديدة)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; border-radius: 15px; border: none;
        height: 3.5em; font-weight: bold; width: 100%;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(0,212,255,0.4); }
    .stTextInput>div>div>input { border-radius: 12px; background-color: #161b22; color: white; border: 1px solid #30363d; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #007bff , #00d4ff); }
    
    /* تنسيق قسم التيك توك */
    .tiktok-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        background-color: #161b22;
        border-radius: 15px;
        margin-top: 30px;
        text-decoration: none;
        transition: 0.3s;
    }
    .tiktok-footer:hover { background-color: #1f242d; }
    .tiktok-footer img { width: 30px; margin-left: 10px; }
    .tiktok-footer span { color: white; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. نظام الأكواد وقفل الجهاز ---
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
    st.markdown("<h1 style='text-align: center;'>🔐 BS PRO ENGINE</h1>", unsafe_allow_html=True)
    st.write("---")
    st.info("مرحباً بك! يرجى إدخال كود التفعيل المخصص لجهازك.")
    
    code_input = st.text_input("كود التفعيل", type="password", placeholder="أدخل الكود هنا...")
    
    if st.button("تفعيل الاشتراك ✨"):
        device_id = st.context.headers.get("User-Agent")
        if code_input in st.session_state["codes_db"]:
            if st.session_state["codes_db"][code_input] is None or st.session_state["codes_db"][code_input] == device_id:
                st.session_state["codes_db"][code_input] = device_id
                st.session_state["authenticated"] = True
                st.success("تم التفعيل بنجاح!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("⚠️ هذا الكود مفعّل مسبقاً على جهاز آخر!")
        else:
            st.error("❌ الكود غير صحيح.")
    st.stop()

# --- 4. واجهة البرنامج الرئيسية ---
st.markdown("<h1 style='text-align: center;'>🚀 محرك BS الاحترافي</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("👤 حسابك")
    st.success("الحالة: متصل ✅")
    if st.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

uploaded_file = st.file_uploader("قم برفع مقطع الفيديو", type=["mp4", "mov"])

if uploaded_file:
    st.write(f"✅ تم اختيار: `{uploaded_file.name}`")
    
    if st.button("🚀 ابدأ المعالجة السحرية"):
        input_path = "temp_in.mp4"
        output_path = "BS_PRO_VIDEO.mp4"
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        progress_bar = st.progress(0)
        status = st.empty()
        
        for p in range(1, 41):
            time.sleep(0.05)
            progress_bar.progress(p)
            status.text(f"🔍 تحليل الإطارات... {p}%")

        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', "setpts=2.0*PTS", '-r', '60',
            '-c:v', 'libx264', '-crf', '18', '-preset', 'superfast',
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', output_path
        ]
        
        try:
            with st.spinner("⚙️ جاري المعالجة..."):
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    progress_bar.progress(100)
                    status.text("✅ اكتملت المعالجة!")
                    st.video(output_path)
                    with open(output_path, "rb") as f:
                        st.download_button("📥 تحميل الفيديو", f, "BS_Pro_60FPS.mp4")
                    st.balloons()
        except Exception as e:
            st.error(f"خطأ: {e}")

# --- 5. قسم التيك توك (إضافة حسابك في الأسفل) ---
st.markdown("---")
st.markdown(f"""
    <a href="https://www.tiktok.com/@BoostifySt0re" target="_blank" class="tiktok-footer">
        <img src="https://cdn-icons-png.flaticon.com/512/3046/3046121.png" alt="TikTok">
        <span>BoostifySt0re على تيك توك</span>
    </a>
    <p style='text-align: center; color: #8b949e; margin-top: 10px;'>جميع الحقوق محفوظة لمتجر BS © 2026</p>
    """, unsafe_allow_html=True)
