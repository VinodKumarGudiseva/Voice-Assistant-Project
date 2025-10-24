from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows frontend to connect (pip install flask-cors)
import datetime
import wikipedia
import pywhatkit
import webbrowser
import requests
import json
import os
import random
import urllib.parse

# ==========================
# CONFIGURATION
# ==========================
OPENWEATHER_API_KEY = "65b2e5d3e8bee4973459f62ed365a818"
NEWS_API_KEY = "e850cad7b7444dcaa6c2005bf0907016"
WAKE_WORD = "stark"  # Not used in backend; handled by frontend

# ==========================
# FLASK APP SETUP
# ==========================
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for the frontend

# ==========================
# PERSONALITY / SMALL TALK (From your original code)
# ==========================
greetings = [
    "Hello! How are you today?",
    "Hi there! Ready to get things done?",
    "Hey! What can I do for you?"
]

farewells = [
    "Goodbye! Have a great day!",
    "See you later! Stay awesome.",
    "Bye! I’ll be here if you need me."
]

jokes = [
    "Why did the computer go to the doctor? Because it caught a virus!",
    "Why was the computer cold? It left its Windows open!",
    "Why did the smartphone need glasses? It lost its contacts!"
]

small_talk = {
    "how are you": ["I am doing great, thank you!", "Feeling awesome today!"],
    "what's your name": ["I am your personal assistant.", "You can call me Assistant."],
    "tell me a joke": jokes,
    "hello": greetings
}

def handle_small_talk(query):
    for key in small_talk:
        if key in query:
            return random.choice(small_talk[key])
    return None

# ==========================
# COMMAND FUNCTIONS (From your original code)
# ==========================
def tell_time():
    return datetime.datetime.now().strftime("The time is %H:%M:%S")

def tell_date():
    return datetime.datetime.now().strftime("Today is %A, %B %d, %Y")

def search_wikipedia(query):
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except:
        return "Sorry, I couldn't find anything on Wikipedia."

def search_wikipedia_page(query):
    query = query.replace("search", "").replace("for", "").replace("on wikipedia", "").strip()
    encoded_query = urllib.parse.quote(query.replace(" ", "_"))
    url = f"https://en.wikipedia.org/wiki/{encoded_query}"
    webbrowser.open(url)
    return f"Searching Wikipedia for {query}"

def open_website(url):
    webbrowser.open(url)

def play_youtube(video):
    pywhatkit.playonyt(video)

def search_youtube(query):
    query = query.replace("search", "").replace("on youtube", "").strip()
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching YouTube for {query}"

def play_local_music(file_path):
    os.startfile(file_path)

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"Current temperature in {city} is {temp}°C with {desc}"
    else:
        return "City not found."

def get_news(api_key, num_articles=5):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url).json()
    if response.get("articles"):
        articles = response["articles"][:num_articles]
        news_str = ""
        for i, article in enumerate(articles, 1):
            news_str += f"{i}. {article['title']}\n"
        return news_str
    return "No news available."

def add_reminder(reminder, file="reminders.json"):
    try:
        if os.path.exists(file):
            with open(file, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.append(reminder)
        with open(file, "w") as f:
            json.dump(data, f)
        return "Reminder added!"
    except Exception as e:
        return f"Error: {str(e)}"

def list_reminders(file="reminders.json"):
    try:
        if os.path.exists(file):
            with open(file, "r") as f:
                data = json.load(f)
            if data:
                return "\n".join([f"{i+1}. {r}" for i, r in enumerate(data)])
        return "No reminders found."
    except Exception as e:
        return f"Error: {str(e)}"

def open_whatsapp():
    open_website("https://web.whatsapp.com")
    return "Opening WhatsApp"

def open_flipkart():
    open_website("https://www.flipkart.com")
    return "Opening Flipkart"

def open_gmail():
    open_website("https://mail.google.com")
    return "Opening Gmail"

def open_instagram():
    open_website("https://www.instagram.com")
    return "Opening Instagram"

def open_linkedin():
    open_website("https://www.linkedin.com")
    return "Opening LinkedIn"

def open_google_maps():
    open_website("https://maps.google.com")
    return "Opening Google Maps"

def search_google(query):
    query = query.replace("search", "").replace("on google", "").strip()
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching Google for {query}"

def open_mx_player():
    open_website("https://www.mxplayer.in")
    return "Opening MX Player"

# ==========================
# API ENDPOINT
# ==========================
@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query', '').lower()
    
    # Small talk / personality
    response = handle_small_talk(query)
    if response:
        return jsonify({'response': response})
    
    # Normal commands
    if "time" in query:
        response = tell_time()
    elif "date" in query:
        response = tell_date()
    elif "wikipedia" in query:
        response = search_wikipedia(query)
    elif "search" in query and "wikipedia" in query:
        response = search_wikipedia_page(query)
    elif "youtube" in query:
        video = query.replace("play", "").replace("on youtube", "")
        response = f"Playing {video} on YouTube"
        play_youtube(video)
    elif "search" in query and "youtube" in query:
        response = search_youtube(query)
    elif "open google" in query:
        response = "Opening Google"
        open_website("https://www.google.com")
    elif "search" in query and "google" in query:
        response = search_google(query)
    elif "open whatsapp" in query:
        response = open_whatsapp()
    elif "open flipkart" in query:
        response = open_flipkart()
    elif "open gmail" in query:
        response = open_gmail()
    elif "open instagram" in query:
        response = open_instagram()
    elif "open linkedin" in query:
        response = open_linkedin()
    elif "open google maps" in query:
        response = open_google_maps()
    elif "open mx player" in query:
        response = open_mx_player()
    elif "weather" in query:
        city = query.replace("weather in", "").strip()
        response = get_weather(city, OPENWEATHER_API_KEY)
    elif "news" in query:
        news = get_news(NEWS_API_KEY)
        response = "Here are the top news headlines:\n" + news
    elif "add reminder" in query:
        # For simplicity, assume reminder text is in query; in real use, frontend could prompt
        reminder = query.replace("add reminder", "").strip()
        response = add_reminder(reminder)
    elif "list reminders" in query:
        response = list_reminders()
    elif "exit" in query or "quit" in query:
        response = random.choice(farewells)
    else:
        response = "I can't do that yet."
    
    return jsonify({'response': response})

# ==========================
# RUN APPLICATION
# ==========================
if __name__ == "__main__":
    print("Starting Voice Assistant Backend on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)  # Accessible from any device on network

