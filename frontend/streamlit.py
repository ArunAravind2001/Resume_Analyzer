import streamlit as st
import requests
import json
import time

# Optional: Lottie support. If streamlit_lottie isn't installed, we'll render Lottie via an <script> fallback.
try:
    from streamlit_lottie import st_lottie
    _HAS_STREAMLIT_LOTTIE = True
except Exception:
    _HAS_STREAMLIT_LOTTIE = False

# Helper to load lottie JSON from URL
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

# Fallback: render Lottie using lottie-web in an HTML component
def _render_lottie_html(lottie_json, height=200, key="lottie_fallback"):
    if not lottie_json:
        return
    import streamlit.components.v1 as components
    # Embed lottie-web via CDN and mount the animation
    html = f"""
    <div id="{key}" style="height:{height}px"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.14/lottie.min.js"></script>
    <script>
    const animData = {json.dumps(lottie_json)};
    const container = document.getElementById('{key}');
    const anim = lottie.loadAnimation({{
        container: container,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        animationData: animData
    }});
    </script>
    """
    components.html(html, height=height)

# ---------- App Config ----------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    :root{
        --bg:#f4f6f8;
        --card:#ffffff;
        --muted:#6b7280;
        --accent-1:linear-gradient(90deg,#667eea 0%,#764ba2 100%);
        --accent-2:#38a169;
        --danger:#e53e3e;
    }
    html, body, [class*="css"]  {
        background: var(--bg);
    }
    .app-header{
        background: linear-gradient(90deg,#5b6ffb 0%, #7b4bb3 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(96, 96, 128, 0.08);
        display:flex;
        gap:1rem;
        align-items:center;
    }
    .app-title{font-size:1.4rem; margin:0}
    .app-sub{color:rgba(255,255,255,0.9); margin:0; font-size:0.95rem}

    /* Card */
    .card{background:var(--card); padding:1rem; border-radius:12px; box-shadow: 0 6px 18px rgba(99,99,122,0.06);}
    .card:hover{transform:translateY(-4px); transition:all .25s ease}

    /* Skill badge */
    .skill-badge{display:inline-block; padding:6px 12px; margin:6px 6px 6px 0; border-radius:999px; background:#fff0f0; color: var(--danger); font-weight:600;}

    /* Project item */
    .project-item{padding:10px 12px; border-radius:10px; margin-bottom:8px; border-left:4px solid #c6f6d5; background:#fbfffb}

    /* Gauge container */
    .gauge-wrap{display:flex; align-items:center; gap:1rem}

    /* Circular gauge - SVG animation using stroke-dashoffset */
    .gauge{width:150px; height:150px;}
    .gauge-text{font-size:1.2rem; font-weight:700; text-align:center}

    /* Responsive tweaks */
    @media(max-width:640px){
        .app-header{flex-direction:column; text-align:center}
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input("API URL", value="http://127.0.0.1:8000/analyze/")
    debug_mode = st.checkbox("🐛 Debug Mode")
    is_mobile = st.checkbox("📱 Force Mobile Layout")
    st.markdown("---")
    st.markdown("Built with ❤️ — keep your backend as-is. This UI upgrades only presentation and UX.")

# ---------- Header with Lottie ----------
# ---------- Modern Gradient Header with Animation ----------

header_lottie = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json")

st.markdown("""
<style>
.header-container {
    background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    padding: 2rem 2.5rem;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    animation: fadeSlide 0.8s ease forwards;
}
.header-text h1 {
    font-size: clamp(1.8rem, 4vw, 2.6rem);
    color: white;
    margin-bottom: 0.6rem;
}
.header-text p {
    font-size: clamp(1rem, 2vw, 1.2rem);
    color: rgba(255,255,255,0.9);
    margin-bottom: 1rem;
}
.header-text button {
    background: white;
    color: #2575fc;
    font-weight: 600;
    padding: 0.6rem 1.4rem;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.header-text button:hover {
    background: #f0f4ff;
}
@keyframes fadeSlide {
    0% {opacity: 0; transform: translateY(-15px);}
    100% {opacity: 1; transform: translateY(0);}
}
@media(max-width: 768px) {
    .header-container { flex-direction: column; text-align: center; }
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    st.markdown("<div class='header-text'>", unsafe_allow_html=True)
    st.markdown("<h1>🎯 AI Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p>Instant resume-to-job matching with actionable suggestions to make you stand out.</p>", unsafe_allow_html=True)
    st.markdown("<button onclick='window.scrollTo({top: 500, behavior: \"smooth\"})'>🚀 Try It Now</button>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if _HAS_STREAMLIT_LOTTIE and header_lottie:
        st_lottie(header_lottie, height=200, key="header_anim")
    elif header_lottie:
        _render_lottie_html(header_lottie, height=200, key="header_fallback")
    else:
        st.image("https://via.placeholder.com/200", use_column_width=True)


# ---------- Input Area ----------
if is_mobile:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Upload Your Resume")
    resume_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
    st.markdown("### 📋 Job Description")
    job_desc = st.text_area("Job Description", height=140, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    left, right = st.columns([1, 1])
    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📄 Upload Your Resume")
        resume_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Job Description")
        job_desc = st.text_area("Job Description", height=180, label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- Helper: render animated circular gauge ----------
def render_circular_gauge(score: int, size: int = 150):
    if score < 0: score = 0
    if score > 100: score = 100
    radius = 60
    circumference = 2 * 3.141592653589793 * radius
    fill = score / 100.0
    offset = circumference * (1 - fill)
    if score >= 80:
        stroke, emoji = '#38a169', '🎉'
    elif score >= 60:
        stroke, emoji = '#ed8936', '👍'
    else:
        stroke, emoji = '#e53e3e', '⚠️'

    svg = f"""
    <div class='gauge-wrap'>
      <svg class='gauge' viewBox='0 0 150 150'>
        <circle r='{radius}' cx='75' cy='75' fill='none' stroke='#e6eaf0' stroke-width='12'/>
        <circle r='{radius}' cx='75' cy='75' fill='none' stroke='{stroke}' stroke-width='12' stroke-linecap='round'
            stroke-dasharray='{circumference}' stroke-dashoffset='{circumference}'>
        </circle>
      </svg>
      <div style='display:flex;flex-direction:column;align-items:flex-start'>
        <div class='gauge-text'>{emoji} <span style='font-size:1.6rem'>{score}%</span></div>
        <div style='color:var(--muted); font-size:0.95rem;'>Resume Match Score</div>
      </div>
    </div>
    <script>
    (function(){{
      const circ = document.querySelectorAll('svg.gauge circle')[1];
      if(!circ) return;
      const circumference = {circumference};
      const offset = {offset};
      setTimeout(()=>{{ circ.style.strokeDashoffset = offset; }}, 50);
    }})();
    </script>
    """
    st.markdown(svg, unsafe_allow_html=True)


# ---------- Analyze Button & Logic (kept nearly identical to your original) ----------
if st.button("🚀 Analyze Resume"):
    if resume_file and job_desc and job_desc.strip():
        try:
            resume_file.seek(0)
            files = {"file": (resume_file.name, resume_file.read(), "application/pdf")}
            data = {"description": job_desc}

            with st.spinner("🔍 Analyzing your resume... please wait"):
                # keep the same request behavior
                response = requests.post(api_url, files=files, data=data)

            if debug_mode:
                st.markdown('<div class="card" style="margin-top:1rem">', unsafe_allow_html=True)
                st.write(f"**Status Code:** {response.status_code}")
                try:
                    st.write(response.json())
                except Exception:
                    st.write(response.text[:1000])
                st.markdown('</div>', unsafe_allow_html=True)

            if response.status_code == 200:
                try:
                    resp = response.json()
                    # Maintain robust parsing from original
                    result = resp.get("analysis_result") or resp.get("result") or resp

                    if isinstance(result, str):
                        parsed = json.loads(result)
                    else:
                        parsed = result

                    if isinstance(parsed, dict):
                        if "analysis_result" in parsed:
                            parsed = parsed["analysis_result"]
                        elif "result" in parsed:
                            parsed = parsed["result"]

                    # key mapping compatibility
                    key_map = {
                        "match_score": "match_percentage",
                        "missing": "missing_skills",
                        "projects": "suggested_projects"
                    }
                    for old_key, new_key in key_map.items():
                        if old_key in parsed and new_key not in parsed:
                            parsed[new_key] = parsed.pop(old_key)

                    required_fields = ["match_percentage", "missing_skills", "suggested_projects"]
                    missing_fields = [f for f in required_fields if f not in parsed or parsed[f] is None]
                    if missing_fields:
                        st.warning(f"⚠️ Missing fields: {missing_fields}")
                        st.json(parsed)

                    st.markdown('---')
                    st.markdown("## 📊 Analysis Results")

                    try:
                        match_score_raw = parsed.get('match_percentage', 0)
                        match_score = int(str(match_score_raw).replace('%', '').strip())
                    except Exception:
                        match_score = 0

                    # Gauge + small explanation
                    left_col, right_col = st.columns([1, 2])
                    with left_col:
                        render_circular_gauge(match_score)
                    with right_col:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('### Quick Tips')
                        st.markdown('- Focus on the missing skills below to improve your match.')
                        st.markdown('- Try the suggested projects to demonstrate hands-on experience.')
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Missing skills and suggested projects in cards
                    ms = parsed.get('missing_skills', []) or []
                    sp = parsed.get('suggested_projects', []) or []

                    st.markdown('---')
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('### ❌ Missing Skills')
                        if ms:
                            for skill in ms:
                                skill_str = str(skill).strip()
                                if skill_str:
                                    st.markdown(f"<span class='skill-badge'>{skill_str}</span>", unsafe_allow_html=True)
                        else:
                            st.success('🎉 No missing skills found!')
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col_b:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('### 💡 Suggested Projects')
                        if sp:
                            for project in sp:
                                project_str = str(project).strip()
                                if project_str:
                                    st.markdown(f"<div class='project-item'>🔸 {project_str}</div>", unsafe_allow_html=True)
                        else:
                            st.info('✅ Your resume looks great!')
                        st.markdown('</div>', unsafe_allow_html=True)

                except json.JSONDecodeError:
                    st.error('❌ Could not parse JSON from API.')
                    if debug_mode:
                        st.text(response.text)
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            st.error('❌ Request timed out.')
        except requests.exceptions.ConnectionError:
            st.error('❌ Could not connect to API server.')
        except Exception as e:
            st.error(f'❌ Unexpected error: {str(e)}')
            if debug_mode:
                st.exception(e)
    else:
        st.warning('⚠️ Please upload a resume and enter a job description.')

# ---------- Footer ----------
st.markdown('---')
st.markdown("<div style='text-align:center; color:#666; padding:0.6rem;'>🤖 Powered by AI | UI: Upgraded Streamlit interface</div>", unsafe_allow_html=True)
