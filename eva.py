import os
import sys
import pandas as pd
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# API Anahtarlarını yükle
load_dotenv()

# Yol ayarı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.rag_model import RAGChatbotModel

# 1. HAKEM (JÜRİ) OLUŞTURMA - GÜNCELLENDİ 🛠️
# request_timeout=120 -> 120 saniye (2 dakika) bekle, pes etme.
# max_retries=3 -> Hata alırsan 3 kere tekrar dene.
yargic_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    request_timeout=120,
    max_retries=3
)
yargic_embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 2. SENİN MODELİNİ YÜKLEME
print("🤖 Senin RAG Modelin Yükleniyor...")
rag_bot = RAGChatbotModel("data/magaza_rehberi.pdf")

# 3. TEST VERİ SETİ
# --- eva.py dosyasındaki 3. BÖLÜM ---

# 3. TEST VERİ SETİ (Senin attığın PDF içeriğine BİREBİR uyumlu)
test_sorulari = [
    "Kargo ücreti ne kadar, ücretsiz kargo limiti var mı?",
    "Hangi ürünlerin iadesi kabul edilmez?",
    "Siparişler ne zaman kargoya verilir?",
]

# Gerçek Cevaplar (Ground Truth - PDF'ten kopyalandı)
gercek_cevaplar = [
    "1000 TL ve uzeri alisverislerde kargo ucretsizdir. Alti siparislerde sabit 59 TL ucret alinir.",
    "Hijyen kurallari geregi kulaklik, dis fircasi ve kisisel bakim urunlerinde iade kabul edilmemektedir. Ayrica yazilim urunleri ve dijital kodlar iade edilemez.",
    "Hafta ici saat 16:00'ya kadar verilen siparisler ayni gun kargoya verilir. Cumartesi saat 11:00'a kadar verilenler ayni gun cikar. Pazar gunu kargo cikisi yoktur."
]

# --- Kodun geri kalanı aynı kalsın ---

print("🚀 Sınav Başlıyor! Sorular modele soruluyor...")

# 4. SORULARI MODELE SORMA
answers = []
contexts = []

for soru in test_sorulari:
    try:
        response = rag_bot.rag_chain.invoke({"input": soru})
        answers.append(response["answer"])
        retrieved_docs = [doc.page_content for doc in response["context"]]
        contexts.append(retrieved_docs)
    except Exception as e:
        print(f"HATA: {soru} sorusunda hata oluştu: {e}")
        answers.append("Cevap alınamadı")
        contexts.append([""])

# 5. VERİYİ HAZIRLAMA
data_dict = {
    "question": test_sorulari,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": gercek_cevaplar
}

dataset = Dataset.from_dict(data_dict)

print("📊 Puanlar Hesaplanıyor (Sabırlı olun, timeout önlemi alındı)...")

# 6. DEĞERLENDİRME
try:
    sonuclar = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_recall,
        ],
        llm=yargic_llm,
        embeddings=yargic_embeddings
    )

    # 7. RAPORLAMA - GÜNCELLENDİ 🛠️
    print("\n🎯 --- DOĞRULUK RAPORU --- 🎯")
    df_sonuc = sonuclar.to_pandas()
    
    # Sütun seçerken hata verirse tüm tabloyu bas (Crash olmasın)
    try:
        print(df_sonuc[["question", "faithfulness", "answer_relevancy", "context_recall"]])
    except KeyError:
        print("⚠️ Tablo formatı farklı görünüyor, tüm tablo basılıyor:")
        print(df_sonuc)

    df_sonuc.to_excel("rag_dogruluk_raporu.xlsx", index=False)
    print("\n✅ Rapor 'rag_dogruluk_raporu.xlsx' olarak kaydedildi!")

except Exception as e:
    print(f"\n❌ Değerlendirme sırasında kritik hata: {e}")
    print("İpucu: Eğer yine Timeout alırsan internet bağlantını kontrol et veya VPN varsa kapat.")