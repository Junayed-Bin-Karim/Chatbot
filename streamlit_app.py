import streamlit as st
import time
import random

# Page configuration
st.set_page_config(
    page_title="Emotion Chatbot - বাংলা",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .chat-user {
        background-color: #d1ecf1;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border: 1px solid #bee5eb;
    }
    .chat-bot {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border: 1px solid #f5c6cb;
    }
    .emotion-badge {
        background-color: #6c757d;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Cache the emotion model
@st.cache_resource
def load_emotion_model():
    try:
        from transformers import pipeline
        return pipeline("text-classification", 
                       model="bhadresh-savani/bert-base-uncased-emotion",
                       return_all_scores=True)
    except Exception as e:
        st.error(f"Model load error: {e}")
        return None

# Bengali responses based on emotions
BENGALI_RESPONSES = {
    'sadness': [
        "আমি খুবই দুঃখিত যে আপনি এভাবে অনুভব করছেন। আমি আপনার পাশে আছি 💙",
        "এটা শুনে আমারও খুব খারাপ লাগছে। আপনি একা নন, আমি আছি 🫂",
        "কথাগুলো শেয়ার করার জন্য ধন্যবাদ। আমি শুনছি এবং যত্ন নিচ্ছি 🌸"
    ],
    'joy': [
        "ওয়াও! এটি শুনে আমি খুবই খুশি হলাম! 😊",
        "আপনার আনন্দ দেখে আমারও ভালো লাগছে! ✨",
        "এটা真是 চমৎকার! আপনার সুখ আমাকেও প্রভাবিত করছে 🌟"
    ],
    'love': [
        "ভালোবাসা真是世界上最美的 احساس! ❤️",
        "প্রেমের这种感觉真是 অসাধারণ! 💕",
        "আপনার প্রেমের কথা শুনে我的心ও ভরিয়ে গেছে 🌹"
    ],
    'anger': [
        "আমি বুঝতে পারছি আপনি রাগান্বিত। কি bothering আপনাকে বলুন?",
        "রেগে যাওয়া স্বাভাবিক। কথা বলে দেখুন, সাহায্য করতে পারি 🫂",
        "এই রাগের feeling প্রকাশ করা important 🌪️"
    ],
    'fear': [
        "ভয় পাওয়া স্বাভাবিক। কি担心 করছেন বলুন?",
        "আপনি একা নন, আমি আছি। ভয়ের সাথে deal করা যায় 🌈",
        "এই ভয়ের কথা share করার জন্য ধন্যবাদ 🌼"
    ],
    'surprise': [
        "ওহ! এটি真是 অপ্রত্যাশিত! 😮",
        "বাহ! এটি真是 আশ্চর্যজনক খবর! 🎉",
        "আমি真是 এটি预料 করিনি! কি happened? ✨"
    ]
}

# Bengali small talk responses
BENGALI_SMALL_TALK = {
    'greeting': [
        "নমস্কার! আমি আপনার ইমোশন চ্যাটবট 🤖",
        "হ্যালো! কেমন আছেন আপনি? 😊",
        "আসসালামু আলাইকুম! কথা বলুন 🎈"
    ],
    'how_are_you': [
        "আমি ভালো আছি, ধন্যবাদ! আপনার কথা শুনে খুশি হলাম 🌟",
        "আমি ঠিক আছি! আপনার সাথে কথা বলে ভালো লাগছে 😄",
        "আমি great! আপনি কেমন আছেন? 🌈"
    ],
    'thanks': [
        "আপনাকেও ধন্যবাদ! 😊",
        "কোনো সমস্যা নেই! আবার কথা বলবেন 🌸",
        "আপনার কথায় আমি খুশি 🌟"
    ],
    'name': [
        "আমি একটি ইমোশন ডিটেকশন চ্যাটবট! আমার নাম ইমো-বট 🤖",
        "আমিই আপনার বাংলা ইমোশন চ্যাটবট! 😊"
    ],
    'joke': [
        "কেন scientists পরমাণু বিশ্বাস করে না? কারণ তারা সবকিছু তৈরি করে! 😄",
        "একটা মুরগি রাস্তা পার হয়েছিল। কেন? ওপারে যেতে! 🐔",
        "কম্পিউটার কখনো ঠান্ডা লাগে না? কারণ তার উইন্ডোজ আছে! 💻"
    ]
}

def detect_bengali_small_talk(text):
    """বাংলা small talk detect করা"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['হ্যালো', 'হাই', 'নমস্কার', 'আসসালাম']):
        return random.choice(BENGALI_SMALL_TALK['greeting'])
    elif any(word in text_lower for word in ['কেমন', 'কি অবস্থা', 'কেমন আছ']):
        return random.choice(BENGALI_SMALL_TALK['how_are_you'])
    elif any(word in text_lower for word in ['ধন্যবাদ', 'থ্যাংকস', 'শুকরিয়া']):
        return random.choice(BENGALI_SMALL_TALK['thanks'])
    elif any(word in text_lower for word in ['নাম', 'কে', 'তোমার']):
        return random.choice(BENGALI_SMALL_TALK['name'])
    elif any(word in text_lower for word in ['জোক', 'কমেডি', 'মজার']):
        return random.choice(BENGALI_SMALL_TALK['joke'])
    
    return None

def get_bengali_response(emotion, confidence):
    """ইমোশন based বাংলা response"""
    if emotion in BENGALI_RESPONSES:
        return random.choice(BENGALI_RESPONSES[emotion])
    else:
        return "আপনার কথা শেয়ার করার জন্য ধন্যবাদ 🌟"

def main():
    # Header
    st.title("🤖 বাংলা ইমোশন চ্যাটবট")
    st.markdown("আমার সাথে কথা বলুন, আমি আপনার emotions বুঝতে পারব! 💬")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ সেটিংস")
        st.markdown("""
        **কিভাবে ব্যবহার করবেন:**
        - শুধু টাইপ করুন এবং এন্টার চাপুন
        - আমি আপনার emotions detect করব
        - বাংলা বা English উভয়তেই লিখতে পারেন
        """)
        
        if st.button("🗑️ কনভারসেশন ক্লিয়ার করুন"):
            st.session_state.messages = []
            st.rerun()
    
    # Load emotion model
    emotion_model = load_emotion_model()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"<div class='chat-user'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            with st.chat_message("assistant"):
                st.markdown(f"<div class='chat-bot'>{message['content']}</div>", unsafe_allow_html=True)
                if "emotion" in message:
                    st.caption(f"🧠 সনাক্ত emotion: {message['emotion']} ({message['confidence']}%)")
    
    # Chat input
    if prompt := st.chat_input("আপনার মনের কথা লিখুন..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-user'>{prompt}</div>", unsafe_allow_html=True)
        
        # Generate bot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Check for small talk first
            small_talk_response = detect_bengali_small_talk(prompt)
            
            if small_talk_response:
                full_response = small_talk_response
                emotion = "small_talk"
                confidence = "100"
            else:
                # Detect emotion using AI model
                if emotion_model:
                    try:
                        results = emotion_model(prompt)
                        emotion_data = max(results[0], key=lambda x: x['score'])
                        emotion = emotion_data['label']
                        confidence = f"{emotion_data['score']*100:.1f}"
                    except:
                        emotion = "neutral"
                        confidence = "50.0"
                else:
                    emotion = "neutral"
                    confidence = "50.0"
                
                # Get Bengali response
                full_response = get_bengali_response(emotion, confidence)
            
            # Simulate typing effect
            typing_response = ""
            for char in full_response:
                typing_response += char
                message_placeholder.markdown(f"<div class='chat-bot'>{typing_response}</div>", unsafe_allow_html=True)
                time.sleep(0.02)
            
            # Show emotion detection info
            if emotion != "small_talk":
                st.caption(f"🧠 সনাক্ত emotion: {emotion} ({confidence}% confidence)")
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "emotion": emotion,
            "confidence": confidence
        })

    # Statistics section
    if st.session_state.messages:
        st.sidebar.markdown("---")
        st.sidebar.header("📊 পরিসংখ্যান")
        
        # Count emotions
        emotion_count = {}
        for msg in st.session_state.messages:
            if "emotion" in msg and msg["emotion"] != "small_talk":
                emotion_count[msg["emotion"]] = emotion_count.get(msg["emotion"], 0) + 1
        
        if emotion_count:
            st.sidebar.write("**Emotions detected:**")
            for emotion, count in emotion_count.items():
                st.sidebar.write(f"- {emotion}: {count} বার")

if __name__ == "__main__":
    main()
