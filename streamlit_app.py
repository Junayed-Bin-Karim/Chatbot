import streamlit as st
import time
import random
import json
from datetime import datetime

# Mood-based responses - ChatGPT style
MOOD_RESPONSES = {
    "happy": {
        "greeting": [
            "হ্যালো! আপনার সাথে কথা বলে আমারও খুব ভালো লাগছে! 😊",
            "আসসালামু আলাইকুম! আজকে আপনার আচরণ দেখে মনে হচ্ছে খুব ভালো mood এ আছেন! 🌟",
            "হাই! আপনার আনন্দ আমাকেও প্রভাবিত করছে! ✨"
        ],
        "general": [
            "ওয়াও! এটি চমৎকার! আপনার positivity contagious! 🌈",
            "আপনার কথায় একটা বিশেষ energy আছে, আমি feel করতে পারছি! 💫",
            "এই optimistic attitude খুবই inspiring! 🎉"
        ],
        "problem": [
            "আপনার optimistic approach প্রশংসনীয়! এই attitude নিয়ে এhead যান! ",
            "সমস্যা থাকতেই পারে, কিন্তু আপনার positive mindset সব overcome করতে পারবে! 💪",
            "আপনার মতো positive person এর জন্য কোনো problemই বড় না! 🌟"
        ]
    },
    "sad": {
        "greeting": [
            "হ্যালো... আমি feel করতে পারছি আপনি আজ একটু down feel করছেন 🫂",
            "আসসালামু আলাইকুম... আমি আপনার পাশে আছি, always 💙",
            "হাই... কথা বলুন, আমি শুনছি 🌸"
        ],
        "general": [
            "আমি বুঝতে পারছি... sometimes life gives us tough moments 🌧️",
            "এই feelings valid... আপনার যা feel করছেন তা স্বাভাবিক 🫂",
            "কথাগুলো share করার জন্য ধন্যবাদ... আমি appreciate করছি 🌼"
        ],
        "problem": [
            "এই difficult time এ আমি আপনার সাথে আছি ",
            "Remember, dark clouds always pass... sunshine一 আসবে 🌈",
            "আপনি alone নন... আমরা together এই situation handle করতে পারি 🤝"
        ]
    },
    "angry": {
        "greeting": [
            "হ্যালো... আমি sense করতে পারছি আপনি frustrated 🌀",
            "আসসালামু আলাইকুম... take a deep breath, আমি here to listen 🌪️",
            "হাই... let's talk about what's bothering you 🔥"
        ],
        "general": [
            "আমি understand your frustration... rage powerful emotion 💥",
            "এই anger express করা important... keep sharing 🌋",
            "আপনার feelings justified... continue expressing 🗣️"
        ],
        "problem": [
            "Let's channel this anger into positive energy ⚡",
            "এই situation temporary... solutions一🌈",
            "আপনার strength admirable, even in anger "
        ]
    },
    "neutral": {
        "greeting": [
            "হ্যালো! কেমন আছেন? 🤖",
            "আসসালামু আলাইকুম! কথা বলুন 💬",
            "হাই! আজকে কেমন যাচ্ছে? 🌟"
        ],
        "general": [
            "বুঝতে পারলাম! আরও বলুন... 💭",
            "Interesting! Continue... 🎯",
            "Thanks for sharing! What's on your mind? 💫"
        ],
        "problem": [
            "Let's think about solutions together 🤔",
            "এই problem solve করা যায়! 💡",
            "আমি help করতে পারি! 🔧"
        ]
    }
}

# Voice recording function
def record_voice():
    try:
        from audio_recorder_streamlit import audio_recorder
        audio_bytes = audio_recorder()
        if audio_bytes:
            # Save audio temporarily
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_bytes)
            return "temp_audio.wav"
    except:
        st.warning("Voice recording not available")
    return None

# Convert speech to text
def speech_to_text(audio_file):
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language='bn-BD')
            return text
    except:
        return None

# Simple emotion detection
def detect_user_mood(text):
    text_lower = text.lower()
    
    happy_words = ['happy', 'joy', 'good', 'great', 'awesome', 'খুশি', 'ভালো', 'মজা', 'অসাধারণ', 'বাহ']
    sad_words = ['sad', 'bad', 'unhappy', 'দুঃখ', 'খারাপ', 'কষ্ট', 'বিষণ্ণ', 'হতাশ']
    angry_words = ['angry', 'mad', 'hate', 'frustrated', 'রাগ', 'ক্রোধ', 'ঝগড়া', 'বিরক্ত']
    
    happy_count = sum(1 for word in happy_words if word in text_lower)
    sad_count = sum(1 for word in sad_words if word in text_lower)
    angry_count = sum(1 for word in angry_words if word in text_lower)
    
    if happy_count > sad_count and happy_count > angry_count:
        return "happy", "আপনি আজ খুবই খুশি এবং positive mood এ আছেন! 😊"
    elif sad_count > happy_count and sad_count > angry_count:
        return "sad", "আপনি আজ একটু দুঃখিত বা down feel করছেন 🫂"
    elif angry_count > happy_count and angry_count > sad_count:
        return "angry", "আপনি কিছুটা রাগান্বিত বা frustrated feel করছেন 🌪️"
    else:
        return "neutral", "আপনার mood স্বাভাবিক আছে 🤖"

# Smart response generator
def generate_smart_response(user_input, user_mood, conversation_history):
    # Analyze conversation context
   # Enhanced context detection
    context_keywords = {
    "work": ["কাজ", "অফিস", "প্রজেক্ট", "বস", "ক্যারিয়ার", "পেশা", "ইন্টারভিউ", "চাকরি"],
    "family": ["পরিবার", "বাবা", "মা", "ভাই", "বোন", "দাদা", "দাদী", "নানা", "নানি"],
    "love": ["প্রেম", "গার্লফ্রেন্ড", "বয়ফ্রেন্ড", "বিয়ে", "রিলেশনশিপ", "প্রেমিকা", "প্রেমিক"],
    "health": ["স্বাস্থ্য", "ডাক্তার", "ওষুধ", "ব্যাথা", "হাসপাতাল", "ফিটনেস", "ওজন", "ডায়েট"],
    "study": ["স্টাডি", "পরীক্ষা", "রেজাল্ট", "বিদ্যালয়", "কলেজ", "বিশ্ববিদ্যালয়", "পড়াশোনা"],
    "finance": ["টাকা", "আয়", "ব্যয়", "বিনিয়োগ", "সঞ্চয়", "বাজেট", "বেতন", "ঋণ"],
    "friendship": ["বন্ধু", "ফ্রেন্ড", "সোশ্যাল", "সম্পর্ক", "বন্ধুত্ব"]
}
    # Detect context
    current_context = "general"
    for context, keywords in context_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            current_context = context
            break
    
    # Get appropriate response based on mood and context
    responses = MOOD_RESPONSES[user_mood]
    
    if "hello" in user_input.lower() or "hi" in user_input.lower() or "হ্যালো" in user_input:
        return random.choice(responses["greeting"])
    elif any(word in user_input for word in ["problem", "issue", "সমস্যা", "কষ্ট"]):
        return random.choice(responses["problem"])
    else:
        response = random.choice(responses["general"])
        
      # Add context-specific advice with BIG responses
if current_context == "work":
    work_advice = """
    
💼 **ক্যারিয়ার ও কাজ সম্পর্কে বিশেষ পরামর্শ:**

🎯 **পেশাগত উন্নতির জন্য:**
• নতুন skills শিখতে থাকুন regularly
• Networking গুরুত্বপূর্ণ - colleagues সাথে ভাল relation maintain করুন
• Time management শিখুন - Pomodoro technique try করতে পারেন

🔄 **Work-Life Balance:**
• Office time আর personal time আলাদা রাখুন
• Regular breaks নিন - প্রতি 1 hour এ 5-10 minute break
• Weekend এ office work avoid করার try করুন

📈 **Career Growth:**
• Short-term আর long-term goals set করুন
• Mentor খুঁজুন - experienced person এর guidance নিন
• Online courses করুন (Coursera, Udemy, YouTube)

🔥 **Motivation:**
"সফলতা overnight আসে না, regularly work করার ফল!"
"""
    response += work_advice

elif current_context == "family":
    family_advice = """
    
👨‍👩‍👧‍👦 **পরিবার সম্পর্কে গভীর পরামর্শ:**

❤️ **সম্পর্ক উন্নতির উপায়:**
• Regular family time রাখুন -weekly একসাথে meal খান
• Active listening practice করুন - শুধু শুনুন, judgment দেবেন না
• Appreciation প্রকাশ করুন - small things এর জন্য thanks বলুন

🏡 **Family Bonding:**
• Family games খেলুন - Ludo, Carrom, Cards
• একসাথে cooking করুন - special weekend activity
• Family photos দেখুন - memories share করুন

🤝 **Conflict Resolution:**
• Calmly কথা বলুন - raised voice সমস্যা বাড়ায়
• Understanding develop করুন - অন্য person এর perspective বুঝার try করুন
• Compromise শিখুন - relationships এ give and take important

💝 **Special Tips:**
"পরিবার আমাদের safe space - এখানে আমরা exactly who we are!"
"""
    response += family_advice

elif current_context == "love":
    love_advice = """
    
❤️ **প্রেম ও সম্পর্ক সম্পর্কে বিশেষ গাইডলাইন:**

💑 **Healthy Relationship Tips:**
• Communication - regularly feelings share করুন
• Trust build করুন - honesty আর transparency maintain করুন
• Personal space respect করুন - everyone needs alone time

🌟 **Relationship Growth:**
• New experiences share করুন - একসাথে new places visit করুন
• Goals set করুন - future plans together তৈরি করুন
• Appreciation regularly প্রকাশ করুন - small gestures matter

🔄 **Challenges Handle:**
• Arguments calmly handle করুন - cooling period নিন if needed
• Understanding develop করুন - partner এর feelings validate করুন
• Compromise করুন - relationships require adjustment

💞 **Romantic Gestures:**
• Surprise gifts দিন - doesn't have to be expensive
• Love letters লিখুন - old school but very effective
• Quality time spend করুন - phones away, just each other

🌹 **Beautiful Thought:**
"True love isn't about finding the perfect person, but about seeing an imperfect person perfectly."
"""
    response += love_advice

elif current_context == "health":
    health_advice = """
    
🏥 **স্বাস্থ্য ও ফিটনেস সম্পর্কে সম্পূর্ণ গাইড:**

🍎 **Healthy Eating Habits:**
• Balanced diet নিন - proteins, carbs, fats, vitamins, minerals
• Regular meals খান - breakfast never skip করুন
• Water plenty পান করুন - 8 glasses daily

💪 **Physical Fitness:**
• Daily exercise করুন - 30 minutes walking
• Yoga বা meditation try করুন - mental health এর জন্য excellent
• Strength training করুন - weekly 2-3 times

😴 **Sleep & Rest:**
• Regular sleep schedule maintain করুন
• 7-8 hours sleep নিন daily
• Screen time reduce করুন bedtime আগে

🧠 **Mental Health:**
• Stress management শিখুন - deep breathing, meditation
• Hobbies develop করুন - painting, music, gardening
• Social connections maintain করুন - friends সাথে regularly meet করুন

🩺 **Regular Checkups:**
• Doctor visit করুন regularly
• Health screenings avoid করুন
• Vaccinations up to date রাখুন

🌟 **Health Mantra:**
"স্বাস্থ্যই সম্পদ - small daily habits create big long-term results!"
"""
    response += health_advice

# Additional contexts with big responses
elif current_context == "study":
    study_advice = """
    
📚 **স্টাডি ও শিক্ষা সম্পর্কে বিস্তারিত পরামর্শ:**

🎓 **Effective Learning Techniques:**
• Active recall practice করুন - just reading নয়, recall করুন
• Spaced repetition ব্যবহার করুন - regularly revise করুন
• Pomodoro technique follow করুন - 25 minutes study, 5 minutes break

📖 **Study Planning:**
• Study schedule তৈরি করুন - realistic goals set করুন
• Priority basis পড়ুন - important topics first
• Regular breaks নিন - brain needs rest

🧠 **Memory Improvement:**
• Mnemonics ব্যবহার করুন - memory techniques
• Visual learning try করুন - diagrams, mind maps
• Teach others - explaining helps understanding

💻 **Online Learning:**
• Structured courses নিন - Coursera, edX, Khan Academy
• Note-taking করুন - digital বা handwritten
• Practice regularly - theoretical knowledge alone insufficient

🚀 **Motivation for Students:**
"Education is the most powerful weapon which you can use to change the world - Nelson Mandela"
"""
    response += study_advice

elif current_context == "finance":
    finance_advice = """
    
💰 **ফাইন্যান্স ও টাকা সম্পর্কে সম্পূর্ণ গাইড:**

💸 **Smart Saving Tips:**
• Budget তৈরি করুন - income আর expenses track করুন
• Emergency fund তৈরি করুন -6 months expenses
• Automatic savings set করুন - monthly automatic transfer

📈 **Investment Strategies:**
• Start early - compound magic কাজ করে
• Diversify portfolio - different types investments
• Long-term thinking - get rich quick schemes avoid করুন

💳 **Debt Management:**
• High-interest debt first pay off করুন
• Credit cards wisely ব্যবহার করুন
• Living within means practice করুন

🏠 **Financial Planning:**
• Retirement planning early শুরু করুন
• Insurance necessary - health, life insurance
• Financial goals set করুন - short-term and long-term

💡 **Money Mindset:**
"It's not about how much you make, but how much you keep and how well it works for you!"
"""
    response += finance_advice

elif current_context == "friendship":
    friendship_advice = """
    
👫 **বন্ধুত্ব ও সামাজিক সম্পর্ক সম্পর্কে বিশেষ পরামর্শ:**

🤝 **Building Strong Friendships:**
• Regular contact রাখুন - calls, messages, meets
• Active listening practice করুন - genuine interest নিন
• Support during tough times - true friends difficult times এ পাশে থাকেন

🌟 **Maintaining Friendships:**
• Remember important dates - birthdays, anniversaries
• Small gestures করুন - checking in, asking about their life
• Forgiveness practice করুন - nobody perfect

🎉 **Social Skills:**
• Conversation skills develop করুন - open-ended questions জিজ্ঞাসা করুন
• Empathy cultivate করুন - others' feelings understand করার try করুন
• Authentic থাকুন - pretend করা unnecessary

💫 **Quality vs Quantity:**
"Few genuine friends better than many superficial relationships!"

🌺 **Friendship Quotes:**
"A real friend is one who walks in when the rest of the world walks out."
"""
    response += friendship_advice

return response

def main():
    st.set_page_config(
        page_title="Smart বাংলা Chatbot - আপনার Mood বুঝবে!",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .mood-indicator {
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        text-align: center;
        font-weight: bold;
    }
    .happy { background-color: #FFEAA7; color: #E17055; }
    .sad { background-color: #74B9FF; color: #0984E3; }
    .angry { background-color: #FF7675; color: #D63031; }
    .neutral { background-color: #DFE6E9; color: #2D3436; }
    .voice-btn {
        background-color: #00B894;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"> Smart বাংলা Chatbot</div>', unsafe_allow_html=True)
    st.markdown("### **আপনার Mood বুঝে Response দিবে!** ")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_mood" not in st.session_state:
        st.session_state.user_mood = "neutral"
    if "mood_description" not in st.session_state:
        st.session_state.mood_description = "আপনার mood এখনও analyze করা হয়নি"
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Mood display
        st.subheader("🎭 আপনার Current Mood")
        mood_class = st.session_state.user_mood
        st.markdown(f'<div class="mood-indicator {mood_class}">{st.session_state.mood_description}</div>', 
                   unsafe_allow_html=True)
        
        # Voice recording section
        st.subheader("🎤 Voice Input")
        st.info("Voice recording feature coming soon!")
        
        # Statistics
        if st.session_state.messages:
            st.subheader("📊 Statistics")
            mood_count = {}
            for msg in st.session_state.messages:
                if msg["role"] == "user" and "mood" in msg:
                    mood_count[msg["mood"]] = mood_count.get(msg["mood"], 0) + 1
            
            if mood_count:
                st.write("**Mood Distribution:**")
                for mood, count in mood_count.items():
                    st.write(f"- {mood}: {count} বার")
        
        # Clear chat
        if st.button("🗑️ Chat Clear করুন"):
            st.session_state.messages = []
            st.session_state.user_mood = "neutral"
            st.session_state.mood_description = "Chat cleared!"
            st.rerun()
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "user" and "mood" in message:
                    st.caption(f"Mood: {message['mood']}")
    
    with col2:
        st.subheader("💡 Tips")
        st.info("""
        Try saying:
        - "আজকে আমার খুব ভালো লাগছে"
        - "আমি একটু upset feel করছি"
        - "কাজ নিয়ে problem হচ্ছে"
        - "পরিবারের situation ভালো না"
        """)
    
    # Chat input with voice option
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.chat_input("আপনার message লিখুন বা voice record করুন...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎤 Voice Input", use_container_width=True):
            st.info("Voice recording feature will be added soon!")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Detect user mood
        current_mood, mood_desc = detect_user_mood(user_input)
        st.session_state.user_mood = current_mood
        st.session_state.mood_description = mood_desc
        
        # Store mood with user message
        st.session_state.messages[-1]["mood"] = current_mood
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
            st.caption(f"Mood: {current_mood}")
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                time.sleep(1)  # Simulate thinking
                
                # Generate smart response
                response = generate_smart_response(
                    user_input, 
                    current_mood, 
                    st.session_state.messages
                )
                
                # Type effect
                message_placeholder = st.empty()
                full_response = ""
                for char in response:
                    full_response += char
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
                message_placeholder.markdown(full_response)
                
                # Add mood-based advice
                if current_mood == "sad":
                    st.info("💡 **সাজেশন:** Music শুনুন, walk করুন, কাছের মানুষের সাথে কথা বলুন")
                elif current_mood == "angry":
                    st.info("💡 **সাজেশন:** Deep breathing করুন, counting করুন, break নিন")
                elif current_mood == "happy":
                    st.success("🎉 **সাজেশন:** এই positive energy maintain করুন, others কে inspire করুন!")
        
        # Add bot response to history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "mood_aware": True
        })

if __name__ == "__main__":
    main()





