
import streamlit as st
from retriever import search_faq

st.set_page_config(
    page_title="Smart Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #2864dc;
    --primary-dark: #1749b5;
    --primary-light: #edf3ff;
    --background: #f5f7fc;
    --text: #192640;
    --muted: #7d8aa3;
    --border: #e6eaf2;
}

.stApp {
    background: var(--background);
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

.block-container {
    max-width: 1250px;
    padding: 2rem 2.5rem;
}

[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h2 {
    color: var(--text);
    font-size: 15px;
    font-weight: 800;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 30px;
}

.brand-icon {
    background: linear-gradient(145deg,#3678f6,#204fc4);
    color: white;
    border-radius: 13px;
    padding: 12px;
    font-size: 22px;
}

.brand-name {
    color: var(--text);
    font-size: 13px;
    font-weight: 800;
}

.brand-sub {
    color: var(--muted);
    font-size: 9px;
    letter-spacing: 1px;
}

.section-label {
    color: #98a3b6;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin: 25px 0 10px;
}

.hero {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
}

.tag {
    display: inline-block;
    background: var(--primary-light);
    color: var(--primary);
    border: 1px solid #e0eaff;
    padding: 8px 11px;
    border-radius: 7px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .5px;
}

.hero h1 {
    font-size: clamp(25px, 3vw, 35px);
    line-height: 1.4;
    letter-spacing: -1px;
    margin: 16px 0 10px;
    color: var(--text);
    font-weight: 800;
}

.hero h1 span {
    color: var(--primary);
}

.hero p {
    color: #77859c;
    font-size: 13px;
    line-height: 1.9;
    max-width: 650px;
}

.hero-icon {
    font-size: 65px;
    background: #e7efff;
    border-radius: 28px;
    padding: 24px;
}

.status {
    color: #718099;
    font-size: 11px;
    margin: 18px 0;
}

.chat-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 0;
    box-shadow: 0 8px 25px rgba(30,54,100,.05);
    overflow: hidden;
}

.chat-heading {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px 23px;
    border-bottom: 1px solid var(--border);
}

.bot-icon {
    background: linear-gradient(145deg,#3777f1,#2253c1);
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-size: 18px;
}

.chat-heading strong {
    color: var(--text);
    font-size: 13px;
}

.chat-heading small {
    color: var(--muted);
    font-size: 11px;
}

.online {
    margin-left: auto;
    color: #16865d;
    background: #effbf5;
    padding: 8px 11px;
    border-radius: 8px;
    font-size: 11px;
}

.answer-card {
    background: white;
    border: 1px solid var(--border);
    padding: 20px;
    border-radius: 13px;
    margin: 10px 0 18px;
    line-height: 1.8;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid var(--border);
    background: white;
    color: #40516d;
    min-height: 42px;
    font-weight: 600;
}

div.stButton > button:hover {
    border-color: var(--primary);
    color: var(--primary);
    background: var(--primary-light);
}

div[data-testid="stChatInput"] {
    border-color: #dce5f5;
}

@media(max-width:700px) {
    .block-container {
        padding: 1rem;
    }
    .hero-icon {
        display: none;
    }
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🎓</div>
        <div>
            <div class="brand-name">SMART ACADEMIC</div>
            <div class="brand-sub">UNIVERSITY ASSISTANT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋  Percakapan Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="section-label">MENU UTAMA</div>',
                unsafe_allow_html=True)
    st.markdown("💬  Chat Assistant")
    st.link_button(
        "🔗  Link Pipeline",
        "https://colab.research.google.com/",
        use_container_width=True
    )

    st.markdown('<div class="section-label">BANTUAN</div>',
                unsafe_allow_html=True)
    st.info(
        "Tanyakan jadwal kuliah, administrasi, kalender akademik, "
        "dan layanan mahasiswa."
    )

    st.caption("🟢 Smart Academic Assistant © 2026")

st.markdown("""
<div class="hero">
  <div>
    <div class="tag">✦ AI-POWERED ACADEMIC SERVICE</div>
    <h1>Halo, Mahasiswa!<br>Ada yang bisa <span>saya bantu?</span></h1>
    <p>Temukan informasi akademik dengan lebih mudah.
    Tanyakan kebutuhanmu dan dapatkan jawaban berdasarkan
    informasi yang tersedia.</p>
  </div>
  <div class="hero-icon">🎓</div>
</div>
<div class="status">🟢 Academic Assistant siap membantu
&nbsp;&nbsp; · &nbsp;&nbsp; 🛡️ Academic Workspace</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chat-card">
  <div class="chat-heading">
    <div class="bot-icon">🤖</div>
    <div><strong>Academic AI Assistant</strong><br>
    <small>Asisten informasi akademik</small></div>
    <div class="online">● Online</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("#### 👋 Selamat datang di Smart Academic Assistant")
st.write(
    "Saya siap membantu menjawab pertanyaan seputar informasi akademik."
)

st.markdown("**PERTANYAAN POPULER**")
questions = [
    "Bagaimana cara melihat jadwal kuliah?",
    "Bagaimana cara mengisi KRS?",
    "Kapan pembayaran UKT dilakukan?",
    "Di mana melihat kalender akademik?"
]

cols = st.columns(2)
for i, q in enumerate(questions):
    if cols[i % 2].button(q, key=f"popular_{i}", use_container_width=True):
        st.session_state.question_input = q
        st.session_state.auto_submit = True
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Tulis pertanyaan akademikmu...")

if st.session_state.pop("auto_submit", False):
    question = st.session_state.pop("question_input", "")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Mencari informasi akademik..."):
            try:
                result = search_faq(question.strip())
                answer = result["answer"]
                st.markdown(answer)

                results = result.get("results", [])
                if results:
                    with st.expander("📚 Referensi terkait"):
                        st.write(results)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception:
                st.error("Terjadi kesalahan saat mencari jawaban.")
