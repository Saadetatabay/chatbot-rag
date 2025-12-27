import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class SimpleChatbotModel:
    def __init__ (self):
        self.model = None
    
    def train(self, file_path):
        data = pd.read_excel(file_path)
        x = data["text"]
        y = data["intent"]
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())
        self.model.fit(x, y)
        print("model eğitildi")

    def predict(self, text):
        if self.model == None:
            raise Exception("Model eğitilmemiş. Lütfen önce train() metodunu çağırın.")
        return self.model.predict([text])[0]
    
if __name__ == "__main__":
    bot = SimpleChatbotModel()
    # Data klasöründeki excel dosyanın yolunu doğru verdiğine emin ol
    bot.train("../data/dataset.xlsx") 
    
    # Test edelim
    ornek_cumle = "Siparişim nerede kaldı gelmedi"
    tahmin = bot.predict(ornek_cumle)
    print(f"Cümle: {ornek_cumle}")
    print(f"Tahmin: {tahmin}")