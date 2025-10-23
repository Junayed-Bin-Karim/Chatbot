import streamlit as st
import time
import random

# Simple emotion detection without transformers
def simple_emotion_detection(text):
    text_lower = text.lower()
    
    joy_words = ['happy', 'joy', 'excited', 'good', 'great', 'wonderful', 'amazing', 'খুশি', 'ভালো', 'মজা']
    sadness_words = ['sad', 'unhappy', 'depressed', 'bad', 'terrible', 'দুঃখ', 'খারাপ', 'কষ্ট']
    anger_words = ['angry', 'mad', 'frustrated', 'hate', 'রাগ', 'ক্রোধ', 'ঝগড়া']
    fear_words = ['scared', 'afraid', 'fear', 'worried', 'ভয়', 'চিন্তা', 'আশঙ্কা']
    
    if any(word in text_lower for word in joy_words):
        return 'joy', 0.85
    elif any(word in text_lower for word in sadness_words):
        return 'sadness', 0.85
    elif any(word in text_lower for word in anger_words):
        return 'anger', 0.85
    elif any(word in text_lower for word in fear_words):
        return 'fear', 0.85
    else:
        return 'neutral', 0.5

# Bengali responses
BENGALI_RESPONSES = {
    'joy': [
        "আহা! খুব ভালো লাগল শুনে! 😊",
        "আপনার আনন্দে আমিও খুশি! ✨",
        "ওয়াও! এটি真是 চমৎকার খবর! 🌟"
    ],
    'sadness': [
        "আমি খুবই দুঃখিত শুনে 💙",
        "আপনার পাশে আছি 🫂", 
        "কথা বলে দেখুন, হালকা হবে 🌸"
    ],
    'anger': [
        "রাগ হওয়া স্বাভাবিক 🌪️",
        "কি bothering আপনাকে বলুন?",
        "শান্ত হোন, আমি আছি 🫂"
    ],
    'fear': [
        "ভয় পাওয়া স্বাভাবিক 🌈",
        "কি worry করছেন বলুন?",
        "আপনি একা নন 🌼"
    ],
    'neutral': [
        "বুঝতে পারলাম 🌟",
        "আরও বলুন... 💬",
        "মজার হয়েছে! 😄"
    ]
}

def main():
    st.set_page_config(
        page_title="বাংলা চ্যাটবট",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 সরল বাংলা চ্যাটবট")
    st.markdown("আমার সাথে বাংলায় কথা বলুন! 💬")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "emotion" in message:
                st.caption(f"Emotion: {message['emotion']} ({message['confidence']}%)")
    
    # Chat input
    if prompt := st.chat_input("আপনার মনের কথা লিখুন..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("ভাবছি..."):
                time.sleep(1)  # Simulate thinking
                
                # Detect emotion
                emotion, confidence = simple_emotion_detection(prompt)
                
                # Get Bengali response
                response = random.choice(BENGALI_RESPONSES.get(emotion, BENGALI_RESPONSES['neutral']))
                
                full_response = f"{response}"
                
                st.markdown(full_response)
                st.caption(f"🧠 Emotion: {emotion} ({confidence*100:.1f}%)")
        
        # Add to history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "emotion": emotion,
            "confidence": f"{confidence*100:.1f}"
        })

if __name__ == "__main__":
    main()
