# LifeStream AI – Personal Wellness & Life Summary Assistant

LifeStream AI is an intelligent personal assistant that analyzes your **Google Calendar** and **Gmail** data to generate wellness-focused insights. It uses NLP to summarize emails, detect emotional tone, predict burnout, and help you reflect on your goals.

---

## 🔍 Features

- 📬 Summarize Emails with Sentiment Analysis
- 📅 Summarize Upcoming Calendar Events
- 📊 Predict Burnout or Stress Based on Tone
- 🧠 Reflective Q&A + Goal Tracker
- 📈 Monthly Email Summary with Tone Trends

---

## 🚀 How It Works

LifeStream AI connects securely to your Google account using OAuth 2.0 and fetches your recent Gmail messages and Calendar events. It then applies NLP (via TextBlob) to analyze emotional tone and summarize data for improved life insights.

---

## 📦 Requirements / Dependencies

Make sure you have **Python 3.10+** installed.

Install the required packages using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib textblob
```

Additionally, install the NLTK corpora needed by TextBlob:

```bash
python -m textblob.download_corpora
```

---

## 🔐 Google API Setup (OAuth 2.0 Authorization)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable the following APIs:
   - Gmail API
   - Google Calendar API
4. Go to **APIs & Services > OAuth Consent Screen**
   - Choose user type: **External**
   - Add test users (your Gmail)
   - Add scopes:
     - `.../auth/calendar.readonly`
     - `.../auth/gmail.readonly`
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
     - `openid`
5. Go to **Credentials > Create Credentials > OAuth Client ID**
   - Choose: **Desktop Application**
   - Download the `credentials.json` file into your project folder

---

## 🛠️ How to Run

1. Clone this repository:

```bash
git clone https://github.com/your-username/lifestream-ai.git
cd lifestream-ai
```

2. Place your downloaded `credentials.json` file in the project directory.

3. Run the app:

```bash
python auth_calender_gmail.py
```

4. A browser window will open for you to sign in with Google and authorize access.

5. After that, you'll see a menu like:

```
1. Summarize Emails
2. Summarize Calendar Events
3. Combined Life Summary (Emails + Calendar)
4. Predictive Wellness Assistant
5. Monthly Email Summary
6. Summarize Email Stress
7. Predict Next Week’s Stress/Burnout
8. Answer Reflective Question
9. Add a New Goal
10. Exit
```

---

## ✨ Future Features (Coming Soon)

- 🧠 Thought Tracker (Daily Mental Diary Summarizer)
- 📊 Mood Journal with Emotional Intelligence Timeline
- 🌐 Web Dashboard (Streamlit)
- 🤖 AI Agents for Proactive Goal Monitoring

---

## 📄 License
MIT License

---

## 🙌 Contributions
Feel free to fork the project and raise a pull request!
