import os
import sys
import streamlit as st
import pandas as pd
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.rag_model import RAGChatbotModel
from models.simple_model import SimpleChatbotModel

st.title("📚 RAG Chatbot with Google Generative AI")
@st.cache_resource #fonksiyonun sadece bir kez çalışmasını sağlar

def load_models():
    simple_model = SimpleChatbotModel()
    simple_model.train("data/dataset.xlsx")
    rag_model = RAGChatbotModel("data/magaza_rehberi.pdf")
    data_frame = pd.read_excel("data/siparisler.xlsx")
    data_frame["Siparis_No"] = data_frame["Siparis_No"].astype(str)
    return simple_model, rag_model, data_frame

simple,rag,df=load_models()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt=st.chat_input("Ask a question ")
if prompt :
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    tahmin=simple.predict(prompt)
    if tahmin == "selamlama":
        tahmin="Merhaba! Size nasıl yardımcı olabilirim?"
    elif tahmin == "siparis_sorgula":
        nums = re.findall(r'\d+', prompt)
        if len(nums) > 0:
            siparis_no = nums[0]
            siparis=df[df["Siparis_No"]==siparis_no]
            if not siparis.empty:
                durum=siparis.iloc[0]["Durum"]
                urun=siparis.iloc[0]["Urun"]
                tahmin=f"Sipariş numarası {siparis_no} olan {urun} ürünü için güncel durum: {durum}."
            else:
                tahmin=f"Üzgünüm, sipariş numarası {siparis_no} ile ilgili bir kayıt bulamadım. Lütfen sipariş numaranızı kontrol edin."
        else:
            tahmin="Lütfen sipariş numaranızı belirtin."
    else:
        tahmin=rag.predict(prompt)
    with st.chat_message("assistant"):
        st.write(tahmin)
    st.session_state.messages.append({"role": "assistant", "content": tahmin}) 
