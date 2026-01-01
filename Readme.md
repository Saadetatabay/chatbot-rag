🛒 TeknoMarket AI Asistanı (Hybrid RAG Chatbot)Ders: Chatbot GeliştirmeÖğrenci: Sadet Yüksel AtabayTarih: Ocak 2026📌 Proje HakkındaBu proje, bir e-ticaret mağazası (TeknoMarket) için geliştirilmiş Hibrit Mimariye (Hybrid Architecture) sahip akıllı bir sanal asistandır.Proje, geleneksel Makine Öğrenmesi (NLP) yöntemleri ile modern Üretken Yapay Zeka (Generative AI / RAG) teknolojilerini birleştirerek hem hızlı hem de akıllı yanıtlar üretmeyi hedefler.🚀 Öne Çıkan ÖzelliklerHibrit Karar Mekanizması: Basit niyetler (Intent) için ML, karmaşık sorular için LLM kullanılır.Gerçek Zamanlı Sipariş Sorgulama: Kullanıcı "102 nolu siparişim nerede?" dediğinde Excel veritabanından anlık durum çeker.RAG (Retrieval-Augmented Generation): Mağaza politikaları (İade, Kargo vb.) PDF dokümanından öğrenilerek cevaplanır.Optimize Edilmiş Performans: Streamlit cache mekanizması ile model sadece bir kez yüklenir.🧠 Sistem Mimarisi ve AkışSistem, kullanıcıdan gelen mesajı analiz etmek için 3 aşamalı bir Yönlendirici (Router) yapısı kullanır:Kod snippet'igraph TD
    A[Kullanıcı Mesajı] --> B{Intent Analizi (Scikit-Learn)}
    B -- "Selamlama / Veda" --> C[Hazır Cevap (Rule-Based)]
    B -- "Sipariş Sorgulama" --> D{Regex ile ID Var mı?}
    D -- Evet --> E[Excel'den Sipariş Durumu Getir (Pandas)]
    D -- Hayır --> F[Kullanıcıdan No İste]
    B -- "Bilgi Sorusu (Diğer)" --> G[RAG Sistemi (Gemini + PDF)]
    G --> H[Vektör Arama & Cevap Üretimi]
    C & E & F & H --> I[Kullanıcıya Yanıt]
🗃️ Kullanılan Veri SetleriProjede göreve özgü 3 farklı veri kaynağı kullanılmıştır:Intent Veri Seti (dataset.xlsx):Boyut: ~1200 Satır.Amaç: Niyet Sınıflandırma (Selamlama, Sipariş Sorma, Veda vb.).Model: Scikit-Learn (Naive Bayes).Bilgi Tabanı (magaza_rehberi.pdf):İçerik: İade koşulları, kargo ücretleri, garanti prosedürleri.Amaç: RAG sistemi için kaynak doküman.Sipariş Veritabanı (siparisler.xlsx):İçerik: Müşteri sipariş numaraları, ürünler ve kargo durumları.Amaç: İşlemsel sorgulara yanıt vermek.🛠️ Kurulum ve ÇalıştırmaProjeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.1. Gereksinimleri YükleyinBashpip install streamlit pandas scikit-learn langchain-google-genai chromadb openpyxl
2. API Anahtarını AyarlayınProje kök dizininde .env dosyası oluşturun ve Google Gemini API anahtarınızı ekleyin:Kod snippet'iGOOGLE_API_KEY=senin_api_anahtarin_buraya
3. Uygulamayı BaşlatınBashstreamlit run main.py
📊 Model Seçimi ve Performans AnaliziProjede iki ana yapay zeka yaklaşımı karşılaştırılmış ve entegre edilmiştir.1. Intent Modeli (Scikit-Learn)Algoritma: Multinomial Naive Bayes (CountVectorizer ile).Neden Seçildi? Metin sınıflandırmada çok hızlıdır ve işlemciyi yormaz. Selamlama gibi basit işler için LLM maliyeti yaratmaz.2. RAG Modeli (Google Gemini)LLM: gemini-1.5-flash (veya Pro).Embedding: models/gemini-embedding-001.Neden Seçildi? Türkçe dil desteği çok güçlüdür ve token maliyeti/performans oranı yüksektir.📈 RAGAS Performans RaporuSistemin dokümana sadakati ve doğru bilgiyi bulma başarısı RAGAS Framework ile test edilmiştir.MetrikSkorAçıklamaContext Recall1.00Sistem, sorulan sorular için PDF'teki doğru paragrafı %100 başarıyla bulmuştur.Faithfulness0.98Model, PDF dışına çıkmadan ve halüsinasyon görmeden cevap üretmiştir.Answer Relevancy0.85Üretilen cevaplar kullanıcı sorusuyla doğrudan alakalıdır.📂 Proje Dosya Yapısı📂 chatbot-proje/
│
├── 📜 main.py                # Ana uygulama (Streamlit + Router Mantığı)
├── 📜 eva.py                 # RAGAS Test ve Değerlendirme Kodu
├── 📜 requirements.txt       # Kütüphaneler
├── 📜 README.md              # Proje Dokümantasyonu
│
├── 📂 data/
│   ├── 📄 dataset.xlsx       # 1200 satırlık Intent verisi
│   ├── 📄 magaza_rehberi.pdf # RAG için PDF
│   └── 📄 siparisler.xlsx    # Sipariş veritabanı
│
└── 📂 models/
    ├── 📜 rag_model.py       # RAG (LangChain) Kodları
    └── 📜 simple_model.py    # Scikit-Learn Model Kodları
👤 İletişimGeliştirici: Sadet Yüksel AtabayDers: Chatbot Geliştirme (2025-2026 Güz Dönemi)