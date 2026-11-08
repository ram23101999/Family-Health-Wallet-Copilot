from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

HEALTH_POLICY_FAQ = [
    ("How does the Dynamic Health Card work?", 
     "The Dynamic Health Card provides instant digital access to your family's prepaid health funds and coverage status at onboarded hospitals."),
    
    ("How to recharge the Prepaid Health Wallet?", 
     "You can top up your Health Wallet via UPI, Netbanking, or Debit/Credit cards through the wallet dashboard instantly."),
     
    ("Is there any pre-authorization needed for hospital admission?", 
     "Emergency admissions do not require prior authorization if your Health Card is Active and adequate wallet balance/coverage is present."),
     
    ("Can multiple family members share one wallet balance?", 
     "Yes, the Family Health Wallet is centralized. All registered family members can draw from the main pooled health balance or member-allocated limits."),
     
    ("What expenses are covered under the wallet?", 
     "Outpatient (OPD) consultations, diagnostic lab tests, pharmacy purchases, and hospital inpatient admissions at network hospitals."),
     
    ("How do claims work for network hospitals?", 
     "Network hospitals verify the Dynamic Health Card, deduct eligible medical expenses directly from your health wallet, enabling cashless treatment.")
]

class HealthRAGEngine:
    def __init__(self):
        self.questions = [q for q, a in HEALTH_POLICY_FAQ]
        self.answers = [a for q, a in HEALTH_POLICY_FAQ]
        self.vectorizer = TfidfVectorizer().fit(self.questions)
        self.question_vectors = self.vectorizer.transform(self.questions)

    def retrieve_answer(self, query, threshold=0.15):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.question_vectors)[0]
        max_idx = similarities.argmax()
        if similarities[max_idx] >= threshold:
            return self.answers[max_idx], round(float(similarities[max_idx]), 2)
        else:
            return "No exact policy information found. Please contact your Health Wallet Support Representative or Hospital Helpdesk.", 0.0

rag_instance = HealthRAGEngine()

def retrieve_answer(query):
    return rag_instance.retrieve_answer(query)
