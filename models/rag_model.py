import os
# Streamlit importunu sildik! Burası sadece mantık.
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class RAGChatbotModel:
    def __init__(self, pdf_path):
        
        # 1. PDF Yükleme
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {pdf_path}")
            
        loader = PyPDFLoader(pdf_path)
        data = loader.load()

        # 2. Metni Parçalama
        # chunk_overlap=200 yaptık ki cümleler kopmasın, anlam bütünlüğü sürsün.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(data)

        # 3. Embedding ve Vektör Veritabanı
        # Embedding modelini tanımlıyoruz
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
        # Verileri vektöre çevirip ChromaDB'ye kaydediyoruz
        # (Bu işlem sadece 1 kez yapılır, hafızada tutulur)
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=embeddings
        )
        
        # Retriever (Arama Motoru) Ayarı
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 3}
        )

        # 4. LLM (Yapay Zeka) Tanımlama
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite", 
            temperature=0.3, 
            max_tokens=500
        )

        # 5. Prompt ve Zincir (Chain) Kurulumu
        system_prompt = (
            "You are a helpful customer support assistant for an electronics store called TeknoMarket. "
            "Use the provided document excerpts to answer user questions about store policies, order status, returns, technical support, and other related topics. "
            "If a user asks about something not covered in the documents, politely inform them that you cannot provide information on that topic. "
            "Always respond in Turkish."
            "\n\n"
            "Context: {context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])

        # Zincirleri birleştiriyoruz
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, document_chain)

    def predict(self, query):
        response = self.rag_chain.invoke({"input": query})
        return response["answer"]