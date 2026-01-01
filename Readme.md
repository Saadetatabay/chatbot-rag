# 🛒 TeknoMarket AI Asistanı 


## 📌 Proje Hakkında

Bu proje, bir e-ticaret mağazası (**TeknoMarket**) için geliştirilmiş   akıllı bir sanal asistandır.

Sistem; **Makine Öğrenmesi** yöntemleri ile **modern Üretken Yapay Zeka (Generative AI / RAG)** teknolojilerini birleştirerek hem **hızlı**, hem de **bağlama duyarlı ve doğru** yanıtlar üretmeyi amaçlar.

---

## 🚀 Öne Çıkan Özellikler

* **Hibrit Karar Mekanizması**  
  Basit niyetler (Intent) için klasik ML modelleri, karmaşık ve bilgi gerektiren sorular için LLM tabanlı RAG sistemi kullanılır.

* **Gerçek Zamanlı Sipariş Sorgulama**  
  Kullanıcı *"102 nolu siparişim nerede?"* gibi sorular sorduğunda Excel tabanlı veritabanından anlık bilgi çekilir.

* **RAG (Retrieval-Augmented Generation)**  
  İade, kargo ve garanti politikaları gibi bilgiler PDF dokümanlardan öğrenilerek cevaplanır.

* **Optimize Edilmiş Performans**  
  Streamlit cache mekanizması sayesinde modeller yalnızca bir kez yüklenir.

---

## 🧠 Sistem Mimarisi ve Akış

Sistem, kullanıcıdan gelen mesajı analiz etmek için **3 aşamalı bir Router (Yönlendirici)** yapısı kullanır:

graph TD
    A[Kullanıcı Mesajı]
    A --> B{Intent Analizi (Scikit-Learn)}

    B -- Selamlama / Veda --> C[Hazır Cevap (Rule-Based)]

    B -- Sipariş Sorgulama --> D{Sipariş No Var mı? (Regex)}
    D -- Evet --> E[Excel'den Sipariş Durumu (Pandas)]
    D -- Hayır --> F[Kullanıcıdan Sipariş No İste]

    B -- Bilgi Sorusu --> G[RAG Sistemi (Gemini + PDF)]
    G --> H[Vektör Arama + Cevap Üretimi]

    C --> I[Kullanıcıya Yanıt]
    E --> I
    F --> I
    H --> I


## 🗃️ Kullanılan Veri Setleri

Projede göreve özel **3 farklı veri kaynağı** kullanılmıştır:

### 1️⃣ Intent Veri Seti (`dataset.xlsx`)

* **Boyut:** ~1200 satır  \
* **Amaç:** Niyet sınıflandırma (Selamlama, Sipariş Sorgulama, Veda vb.)  \
* **Model:** Scikit-Learn – Multinomial Naive Bayes

### 2️⃣ Bilgi Tabanı (`magaza_rehberi.pdf`)

* **İçerik:** İade koşulları, kargo ücretleri, garanti prosedürleri  \
* **Amaç:** RAG sistemi için bilgi kaynağı

### 3️⃣ Sipariş Veritabanı (`siparisler.xlsx`)

* **İçerik:** Sipariş numaraları, ürün bilgileri ve kargo durumları  \
* **Amaç:** İşlemsel sorgulara anlık yanıt üretmek

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Gereksinimleri Yükleyin

```bash
pip install -r requirement.txt
```

### 2. API Anahtarını Ayarlayın

Proje kök dizininde `.env` dosyası oluşturun:

```env
GOOGLE_API_KEY=senin_api_anahtarin_buraya
```

### 3. Uygulamayı Başlatın

```bash
streamlit run main.py
```

---

## 📊 Model Seçimi ve Performans Analizi

### 🔹 Intent Modeli (Scikit-Learn)

* **Algoritma:** Multinomial Naive Bayes  \
* **Vektörleme:** CountVectorizer  \
* **Tercih Nedeni:**

  * Çok hızlıdır
  * Düşük donanım maliyeti
  * Basit niyetler için LLM maliyeti oluşturmaz

### 🔹 RAG Modeli (Google Gemini)

* **LLM:** `gemini-2.5-flash-lite` (opsiyonel: Pro)  \
* **Embedding:** `models/gemini-embedding-001`  \
* **Tercih Nedeni:**

  * Güçlü Türkçe dil desteği
  * Yüksek doğruluk
  * Düşük token maliyeti

---

## 📈 RAGAS Performans Raporu

Sistemin dokümana bağlılığı ve cevap doğruluğu **RAGAS Framework** ile ölçülmüştür:

| Metrik           | Skor | Açıklama                                               |
| ---------------- | ---- | ------------------------------------------------------ |
| Context Recall   | 1.00 | PDF içindeki doğru paragraf %100 başarıyla bulunmuştur |
| Faithfulness     | 0.98 | Model, PDF dışına çıkmadan cevap üretmiştir            |
| Answer Relevancy | 0.85 | Cevaplar kullanıcı sorusuyla yüksek oranda alakalıdır  |

---

## 📂 Proje Dosya Yapısı

```
📂 chatbot-proje/
│
├── main.py            # Streamlit ana uygulama & router mantığı
├── eva.py             # RAGAS test ve değerlendirme kodu
├── requirements.txt   # Gerekli kütüphaneler
├── README.md          # Proje dokümantasyonu
│
├── data/
│   ├── dataset.xlsx        # Intent veri seti
│   ├── magaza_rehberi.pdf  # RAG bilgi kaynağı
│   └── siparisler.xlsx     # Sipariş veritabanı
│
└── models/
    ├── rag_model.py        # RAG (LangChain) kodları
    └── simple_model.py    # Scikit-Learn intent modeli
```

---
