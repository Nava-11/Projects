from __future__ import print_function
import os.path
import pickle
import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from textblob import TextBlob
from base64 import urlsafe_b64decode

# Scopes: read-only for Gmail and Calendar
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

def get_authenticated_services():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    calendar_service = build('calendar', 'v3', credentials=creds)
    gmail_service = build('gmail', 'v1', credentials=creds)
    return calendar_service, gmail_service

def fetch_calendar_summary(calendar_service):
    events_result = calendar_service.events().list(
        calendarId='primary', maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    summary = "\nUpcoming Events:\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary += f"- {start}: {event.get('summary', 'No Title')}\n"
    return summary

def fetch_monthly_email_summary(gmail_service):
    query = 'newer_than:30d'
    results = gmail_service.users().messages().list(userId='me', q=query, maxResults=20).execute()
    messages = results.get('messages', [])

    email_bodies = []
    for msg in messages:
        txt = gmail_service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt.get("payload", {})
        parts = payload.get("parts", [])
        if parts:
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    data = part['body'].get('data')
                    if data:
                        body = urlsafe_b64decode(data + '==').decode("utf-8", errors='ignore')
                        email_bodies.append(body)
        else:
            data = payload.get('body', {}).get('data')
            if data:
                body = urlsafe_b64decode(data + '==').decode("utf-8", errors='ignore')
                email_bodies.append(body)

    summary = "\n📬 Monthly Email Summary:\n"
    for body in email_bodies[:5]:
        blob = TextBlob(body)
        clean_text = ' '.join(body.split())[:150]
        summary += f"- Sentiment: {blob.sentiment.polarity:.2f} | Snippet: {clean_text}...\n"
    return summary

def fetch_email_summary(gmail_service):
    results = gmail_service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    email_bodies = []
    for msg in messages:
        txt = gmail_service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt.get("payload", {})
        parts = payload.get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part['body'].get('data')
                if data:
                    body = urlsafe_b64decode(data).decode("utf-8")
                    email_bodies.append(body)

    summary = "\nRecent Emails Summary:\n"
    for body in email_bodies[:5]:
        blob = TextBlob(body)
        summary += f"- Sentiment: {blob.sentiment.polarity:.2f} | Summary: {body[:100].replace('\n', ' ')}...\n"
    return summary

def summarize_email_stress(gmail_service):
    results = gmail_service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])

    stress_scores = []
    for msg in messages:
        txt = gmail_service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = txt.get("payload", {})
        parts = payload.get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part['body'].get('data')
                if data:
                    body = urlsafe_b64decode(data).decode("utf-8")
                    blob = TextBlob(body)
                    stress_scores.append(blob.sentiment.polarity)

    avg_stress = sum(stress_scores)/len(stress_scores) if stress_scores else 0
    return f"📊 Email Stress Level: {avg_stress:.2f}"

def predict_burnout(email_summary, calendar_summary):
    combined = email_summary + calendar_summary
    blob = TextBlob(combined)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return "⚠️ High stress indicators detected. Consider taking breaks."
    elif polarity < 0.2:
        return "🟡 Medium workload. Stay balanced and monitor productivity."
    else:
        return "✅ You're doing well. Keep it up!"

def answer_reflective_question():
    question = input("\n🧠 Ask a reflective question (e.g., What did I learn this month?): ")
    return f"You asked: '{question}'. That's a great reflection!"

def add_new_goal():
    goal = input("\n🎯 Enter a new goal you'd like to track: ")
    return f"New goal added: '{goal}'"

def interactive_menu():
    print("\n📌 Welcome to LifeStream AI")
    print("1. Summarize Emails")
    print("2. Summarize Calendar Events")
    print("3. Combined Life Summary (Emails + Calendar)")
    print("4. Predictive Wellness Assistant")
    print("5. Monthly Email Summary")
    print("6. Summarize Email Stress")
    print("7. Predict Next Week’s Stress/Burnout")
    print("8. Answer Reflective Question")
    print("9. Add a New Goal")
    print("10. Exit")
    return input("\nEnter your choice: ")

if __name__ == '__main__':
    calendar_service, gmail_service = get_authenticated_services()

    while True:
        choice = interactive_menu()

        if choice == '1':
            print(fetch_email_summary(gmail_service))
        elif choice == '2':
            print(fetch_calendar_summary(calendar_service))
        elif choice == '3':
            calsum = fetch_calendar_summary(calendar_service)
            emailsum = fetch_email_summary(gmail_service)
            print(calsum + emailsum)
        elif choice == '4':
            calsum = fetch_calendar_summary(calendar_service)
            emailsum = fetch_email_summary(gmail_service)
            print("\n🤖 Predictive Wellness Result:")
            print(predict_burnout(emailsum, calsum))
        elif choice == '5':
            print(fetch_monthly_email_summary(gmail_service))
        elif choice == '6':
            print(summarize_email_stress(gmail_service))
        elif choice == '7':
            calsum = fetch_calendar_summary(calendar_service)
            emailsum = fetch_email_summary(gmail_service)
            print(predict_burnout(emailsum, calsum))
        elif choice == '8':
            print(answer_reflective_question())
        elif choice == '9':
            print(add_new_goal())
        elif choice == '10':
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")
