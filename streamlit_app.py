# chatBot_lightweight.py
import streamlit as st
import requests
import json

# Alternative using a smaller model or API
def detect_emotion_simple(text):
    """Simple rule-based emotion detection as fallback"""
    positive_words = ['happy', 'joy', 'excited', 'good', 'great', 'wonderful', 'amazing']
    negative_words = ['sad', 'angry', 'mad', 'bad', 'terrible', 'awful', 'hate']
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in positive_words):
        return 'joy', 0.8
    elif any(word in text_lower for word in negative_words):
        return 'sadness', 0.8
    else:
        return 'neutral', 0.5

def main():
    st.title("Emotion Chatbot")
    
    # Initialize session state
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    # User input
    user_input = st.text_input("You:")
    
    if user_input:
        # Try to use transformers if available, otherwise use fallback
        try:
            from transformers import pipeline
            emotion_pipeline = pipeline("text-classification", 
                                      model="bhadresh-savani/bert-base-uncased-emotion",
                                      return_all_scores=True)
            results = emotion_pipeline(user_input)
            emotion = max(results[0], key=lambda x: x['score'])
            emotion_name = emotion['label']
            confidence = emotion['score']
        except:
            # Fallback to simple detection
            emotion_name, confidence = detect_emotion_simple(user_input)
        
        # Generate response
        responses = {
            'joy': "That's wonderful! 😊",
            'sadness': "I'm here for you. 💙",
            'anger': "I understand you're upset.",
            'fear': "It's okay to feel scared sometimes.",
            'surprise': "Wow! That's surprising!",
            'neutral': "Thanks for sharing that."
        }
        
        response = responses.get(emotion_name, "I appreciate you sharing that.")
        
        # Store conversation
        st.session_state.conversation.append({
            'user': user_input,
            'emotion': emotion_name,
            'confidence': f"{confidence:.2f}",
            'bot': response
        })
    
    # Display conversation
    for i, chat in enumerate(st.session_state.conversation):
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Bot** [{chat['emotion']} - {chat['confidence']}]: {chat['bot']}")
        st.write("---")

if __name__ == "__main__":
    main()
