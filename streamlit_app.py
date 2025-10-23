import streamlit as st
import time

# Cache the model loading
@st.cache_resource
def load_emotion_model():
    try:
        from transformers import pipeline
        return pipeline("text-classification", 
                       model="bhadresh-savani/bert-base-uncased-emotion",
                       return_all_scores=True)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

def main():
    st.set_page_config(page_title="Emotion Chatbot", page_icon="🤖")
    
    st.title("🤖 Emotion-Aware Chatbot")
    st.write("Chat with me and I'll detect your emotions!")
    
    # Load model
    with st.spinner("Loading emotion detection model..."):
        emotion_pipeline = load_emotion_model()
    
    if emotion_pipeline is None:
        st.error("""
        **Failed to load emotion detection model.**
        
        Please check that:
        - `transformers` and `torch` are in requirements.txt
        - The model name is correct
        - There's enough memory available
        """)
        return
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "emotion" in message:
                st.caption(f"Detected emotion: {message['emotion']}")
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Detect emotion and generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing emotion..."):
                try:
                    results = emotion_pipeline(prompt)
                    emotion = max(results[0], key=lambda x: x['score'])
                    emotion_name = emotion['label']
                    confidence = emotion['score']
                    
                    # Generate response based on emotion
                    responses = {
                        'sadness': "I'm sorry you're feeling this way. I'm here for you. 💙",
                        'joy': "That's wonderful! Your happiness is contagious! 😊",
                        'love': "It's beautiful to feel love. ❤️",
                        'anger': "I understand you're frustrated. Would you like to talk about it?",
                        'fear': "It's okay to feel scared sometimes. You're stronger than you think.",
                        'surprise': "Wow! That's quite surprising! What happened?"
                    }
                    
                    response = responses.get(emotion_name, "Thank you for sharing that with me.")
                    full_response = f"{response}\n\n*(Detected: {emotion_name} with {confidence:.1%} confidence)*"
                    
                except Exception as e:
                    full_response = "I understand. Thanks for sharing your feelings with me."
                    emotion_name = "unknown"
            
            st.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "emotion": emotion_name
        })

if __name__ == "__main__":
    main()
