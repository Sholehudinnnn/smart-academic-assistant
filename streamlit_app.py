
import streamlit as st
from retriever import search_faq

st.set_page_config(
    page_title="Smart Academic Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Smart Academic Assistant")
st.caption("Asisten akademik untuk membantu mahasiswa.")

question = st.text_input("Masukkan pertanyaan akademik")

if st.button("Cari Jawaban"):
    if question.strip():
        try:
            result = search_faq(question.strip())
            st.subheader("Jawaban")
            st.write(result["answer"])

            results = result.get("results", [])
            if results:
                with st.expander("Referensi terkait"):
                    st.write(results)

        except Exception:
            st.error(
                "Terjadi kesalahan saat mencari jawaban. "
                "Periksa log aplikasi untuk detailnya."
            )
    else:
        st.warning("Masukkan pertanyaan terlebih dahulu.")
