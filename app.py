import streamlit as st
import subprocess
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="BS PRO | Gaming Speed", layout="centered", page_icon="🎮")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #FF0000, #8B0000);
        color: white; border-radius: 12px; height: 3.5em; width: 100%;
        font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 BS ENGINE")
    code = st.text_input("كود التفعيل", type="password")
    if st.button("تفعيل الدخول ✨"):
        valid_codes = ["BS-7710", "BS-8820", "BS-9930", "PRO-TIK-1", "PRO-TIK-2", "VIP-MASTER", "BS-SPEED-1", "BS-SPEED-2", "GOLD-USER", "PREMIUM-BS"]
        if code in valid_codes:
            st.session_state["authenticated"] = True
            st.rerun()
        else: st.error("❌ كود غير صحيح")
    st.stop()

# --- المحرك (سرعة طبيعية + ألوان Apex) ---
st.title("🚀 BS PRO - السرعة الطبيعية")
st.caption("ألوان Apex الحيوية + 60FPS + سرعة اللعب الأصلية")

uploaded_file = st.file_uploader("ارفع فيديو اللعبة", type=["mp4", "mov"])

if uploaded_file:
    if st.button("🪄 معالجة الفيديو بالسرعة الطبيعية"):
        input_p = "gaming_in.mp4"
        output_p = "BS_RealSpeed_Gaming.mp4"
        
        # تنظيف الملفات
        if os.path.exists(input_p): os.remove(input_p)
        if os.path.exists(output_p): os.remove(output_p)

        with open(input_p, "wb") as f:
            f.write(uploaded_file.getbuffer())

        bar = st.progress(0)
        status = st.empty()
        
        # الفلتر المطور:
        # 1. minterpolate: تجعل الحركة "زبدة" وسلسة جداً مع الحفاظ على السرعة الطبيعية (1.0).
        # 2. eq: ضبط الألوان لتكون مشبعة وعميقة مثل الصورة التي أرسلتها (Saturation 1.5).
        # 3. unsharp: لزيادة حدة تفاصيل الأسلحة والخريطة.
        
        filter_settings = "minterpolate=fps=60:mi_mode=mci,eq=brightness=0.01:saturation=1.5:contrast=1.15,unsharp=5:5:1.5:5:5:0.0"
        
        cmd = [
            'ffmpeg', '-y', '-i', input_p,
            '-vf', filter_settings, 
            '-c:v', 'libx264', 
            '-crf', '17',           # جودة عالية جداً
            '-preset', 'ultrafast', 
            '-pix_fmt', 'yuv420p',
            output_p
        ]
        
        try:
            status.info("⚙️ جاري حقن الألوان وتحسين السلاسة...")
            bar.progress(50)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                bar.progress(100)
                status.success("✅ المقطع جاهز بالسرعة الطبيعية!")
                with open(output_p, "rb") as f:
                    st.download_button("📥 تحميل الفيديو المعدل", f, "BS_Gaming_60FPS.mp4")
                os.remove(input_p)
            else:
                st.error("السيرفر لم يتحمل حجم الملف. حاول بمقطع أصغر.")
        except Exception as e:
            st.error("حدث خطأ في الذاكرة.")

st.markdown("---")
st.markdown("<center><a href='https://www.tiktok.com/@BoostifySt0re' style='color:#FF0000; text-decoration:none;'>BoostifySt0re TikTok</a></center>", unsafe_allow_html=True)
