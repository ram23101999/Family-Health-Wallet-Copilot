# Family Health Wallet – Intelligence & Management Copilot

**Designed & Developed By S. Ramkumar** [cite: 2.1]

இது **Family Health Wallet** திட்டத்திற்கான AI/ML Copilot & Dashboard prototype ஆகும். [cite: 2.2]
ஒரே குடும்பத்திற்கான Prepaid Health Wallet, Card Management, Medical Claims / Health Risk Prediction, மற்றும் RAG-based Medical/Policy Query Assistant ஆகியவற்றை ஒருங்கிணைக்கிறது. [cite: 2.2]

---

## 🌟 முக்கிய அம்சங்கள் (Key Features)

1. **🏥 Health Card & Family Member Profiles** [cite: 2.2]
   - குடும்ப உறுப்பினர்கள் (Family Members) விவரங்களை நிர்வகித்தல். [cite: 2.2]
   - Dynamic Health Card ID (QR-ready) மற்றும் Active/Inactive Status. [cite: 2.2]

2. **💳 Prepaid Health Wallet & Transactions Tracking** [cite: 2.2]
   - Wallet Recharge மற்றும் hospital/pharmacy medical bill expenses பதிவேற்றம். [cite: 2.2]
   - ரியல்-டைம் பேலன்ஸ் மற்றும் செலவு பகுப்பாய்வு (Financial Transparency). [cite: 2.2]

3. **🤖 Health Risk & High Claim Probability Predictor (ML Model)**
   - Random Forest ML மாடல் மூலம் குடும்ப உறுப்பினரின் வயது, முந்தைய மருத்துவ செலவுகள், சிகிச்சை வரலாறு அடிப்படையில் Health Claim / Risk Status கணிப்பது.

4. **❓ Healthcare & Policy RAG Assistant (Knowledge Base)**
   - Health card eligibility, emergency hospital admission, wallet recharge rules, claims process போன்ற கேள்விகளுக்கு TF-IDF Vector & Cosine Similarity 기반 துல்லியமான பதில்கள்.

5. **🗄️ Database Integration (MySQL / Demo Fallback)** [cite: 2.2]
   - Database இணைக்கப்படாத நிலையிலும் Streamlit Demo Mode-ல் சீராக இயங்கும்.

---

## 🚀 இயக்குவது எப்படி (How to Run)

### 1. Requirements Install செய்யவும்:
```bash
pip install -r requirements.txt
```

### 2. Streamlit App இயங்க வைக்க:
```bash
streamlit run app.py
```
