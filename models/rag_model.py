import os
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

my_loader = PyPDFLoader("/home/satabay/chatbot-rag/chatbot-rag/data/magaza_rehberi.pdf")
my_data = my_loader.load()
print(len(my_data))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0)
texts = text_splitter.split_documents(my_data)
print(f"Toplam parça sayısı: {len(texts)}")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = Chroma.from_documents(
    documents=texts,
    embedding=embeddings)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.3)
system_prompt = (
    "You are a helpful customer support assistant for an electronics store called TeknoMarket."
    "Use the provided document excerpts to answer user questions about store policies, order status, returns, technical support, and other related topics."
    "If a user asks about something not covered in the documents, politely inform them that you cannot provide information on that topic."
    "Always respond in Turkish."
    "\n\n"
    "{context}"
)