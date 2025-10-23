# Installing the required libraries
# pip install transformers torch numpy pandas matplotlib seaborn

from transformers import pipeline
import numpy as np
import json
import datetime
import re
from collections import defaultdict, deque
import random

class EnhancedEmotionChatbot:
    def __init__(self):
        # Load emotion detection pipeline
        self.emotion_pipeline = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base", 
            return_all_scores=True
        )
        
        # Conversation history
        self.conversation_history = []
        self.user_profile = defaultdict(lambda: defaultdict(int))
        self.emotion_trend = deque(maxlen=10)  # Track last 10 emotions
        
        # Enhanced response templates
        self.response_templates = {
            "joy": [
                "That's wonderful! I'm really happy for you! 😊",
                "It's great to hear you're feeling joyful!",
                "Your happiness is contagious! Keep shining! ✨",
                "That sounds amazing! I'm glad things are going well for you."
            ],
            "anger": [
                "I understand you're feeling frustrated. Would you like to talk about what's bothering you?",
                "It sounds like you're dealing with something difficult. I'm here to listen.",
                "Take a deep breath. Sometimes expressing these feelings can help.",
                "I hear the frustration in your words. Want to share more about what's upsetting you?"
            ],
            "sadness": [
                "I'm really sorry you're feeling this way. Remember, you're not alone. 💙",
                "It takes courage to acknowledge sadness. I'm here to support you.",
                "This sounds really tough. Would it help to talk more about it?",
                "I'm listening, and I care about what you're going through."
            ],
            "fear": [
                "It's okay to feel scared sometimes. What's concerning you?",
                "Fear can be overwhelming. Talking about it might help ease your mind.",
                "I'm here with you. Would you like to share what's making you anxious?",
                "That sounds worrying. Remember, you're stronger than you think."
            ],
            "surprise": [
                "Wow! That's quite surprising!",
                "Oh really? I didn't see that coming!",
                "That's unexpected! Tell me more!",
                "Interesting development! What happened next?"
            ],
            "neutral": [
                "Thanks for sharing that with me.",
                "I appreciate you telling me that.",
                "That's interesting. Tell me more.",
                "I understand. What's on your mind?"
            ]
        }
        
        # Small talk responses
        self.small_talk_responses = {
            "greeting": ["Hello! 😊", "Hi there!", "Hey! How can I help you today?"],
            "how_are_you": ["I'm functioning well, thank you! How about you?", "I'm good, just here to chat with you!"],
            "thanks": ["You're welcome! 😊", "Happy to help!", "Anytime!"],
            "name": ["I'm your emotion-aware chatbot! You can call me EmoBot.", "I'm your friendly emotion detection chatbot!"],
            "weather": ["I'm not sure about the weather, but I hope it's nice where you are! ☀️"],
            "joke": ["Why don't scientists trust atoms? Because they make up everything! 😄"]
        }

    def detect_emotion(self, text):
        """Detects the emotion in the text using the pipeline."""
        try:
            results = self.emotion_pipeline(text)
            emotions = {res['label']: res['score'] for res in results[0]}
            primary_emotion = max(emotions, key=emotions.get)
            return primary_emotion, emotions[primary_emotion], emotions
        except Exception as e:
            print("Error detecting emotion:", e)
            return "neutral", 0.0, {}

    def analyze_emotion_trend(self):
        """Analyze the trend of emotions in the conversation"""
        if not self.emotion_trend:
            return "stable"
        
        recent_emotions = list(self.emotion_trend)[-5:]  # Last 5 emotions
        if len(recent_emotions) < 3:
            return "stable"
        
        # Simple trend analysis
        positive_emotions = ["joy", "surprise"]
        negative_emotions = ["anger", "sadness", "fear"]
        
        positive_count = sum(1 for e in recent_emotions if e in positive_emotions)
        negative_count = sum(1 for e in recent_emotions if e in negative_emotions)
        
        if positive_count > negative_count + 1:
            return "improving"
        elif negative_count > positive_count + 1:
            return "declining"
        else:
            return "stable"

    def handle_small_talk(self, text):
        """Handle common small talk phrases"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["hello", "hi", "hey"]):
            return random.choice(self.small_talk_responses["greeting"])
        elif any(word in text_lower for word in ["how are you", "how do you do"]):
            return random.choice(self.small_talk_responses["how_are_you"])
        elif any(word in text_lower for word in ["thank", "thanks"]):
            return random.choice(self.small_talk_responses["thanks"])
        elif any(word in text_lower for word in ["your name", "who are you"]):
            return random.choice(self.small_talk_responses["name"])
        elif "weather" in text_lower:
            return random.choice(self.small_talk_responses["weather"])
        elif any(word in text_lower for word in ["joke", "funny"]):
            return random.choice(self.small_talk_responses["joke"])
        
        return None

    def generate_personalized_response(self, emotion, confidence, all_emotions, user_input):
        """Generate a personalized response based on emotion and conversation context"""
        
        # Handle small talk first
        small_talk_response = self.handle_small_talk(user_input)
        if small_talk_response:
            return small_talk_response

        # If confidence is too low, respond neutrally
        if confidence < 0.2:
            return random.choice(self.response_templates["neutral"])

        # Get emotion trend
        trend = self.analyze_emotion_trend()
        
        # Choose random template for the detected emotion
        base_response = random.choice(self.response_templates[emotion])
        
        # Add trend-based follow-up
        if trend == "improving" and emotion in ["joy", "surprise"]:
            base_response += " And it seems like you've been in good spirits lately! 😊"
        elif trend == "declining" and emotion in ["sadness", "anger", "fear"]:
            base_response += " I've noticed you might be going through a tough time recently."
        
        # Add personalized touch for recurring emotions
        emotion_count = self.user_profile['emotion_count'][emotion]
        if emotion_count > 2:
            if emotion == "joy":
                base_response += " You often bring such positive energy! 🌟"
            elif emotion == "sadness":
                base_response += " I'm always here if you need to talk about what's been bothering you."
        
        return base_response

    def provide_emotion_insights(self):
        """Provide insights about the user's emotional patterns"""
        if not self.user_profile['emotion_count']:
            return "I'm still learning about your emotional patterns. Keep chatting!"
        
        total_interactions = sum(self.user_profile['emotion_count'].values())
        if total_interactions < 3:
            return "I need a bit more conversation to provide meaningful insights."
        
        most_common_emotion = max(self.user_profile['emotion_count'].items(), key=lambda x: x[1])
        emotion_percentage = (most_common_emotion[1] / total_interactions) * 100
        
        insights = [
            f"Based on our conversation, you most frequently express {most_common_emotion[0]} "
            f"({emotion_percentage:.1f}% of the time)."
        ]
        
        # Add trend insight
        trend = self.analyze_emotion_trend()
        if trend == "improving":
            insights.append("Your mood seems to be improving throughout our conversation! 📈")
        elif trend == "declining":
            insights.append("I notice your mood has been shifting. Remember, it's okay to not be okay. 💙")
        
        return " ".join(insights)

    def save_conversation(self, filename=None):
        """Save conversation history to a file"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        conversation_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "conversation_history": self.conversation_history,
            "user_profile": dict(self.user_profile['emotion_count'])
        }
        
        with open(filename, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        return filename

    def show_emotion_statistics(self):
        """Display basic emotion statistics"""
        if not self.user_profile['emotion_count']:
            return "No emotion data collected yet."
        
        total = sum(self.user_profile['emotion_count'].values())
        stats = ["Emotion Statistics:"]
        for emotion, count in sorted(self.user_profile['emotion_count'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100
            stats.append(f"{emotion}: {count} ({percentage:.1f}%)")
        
        return "\n".join(stats)

    def chat(self):
        """Main chat loop"""
        print("=" * 60)
        print("🤖 Enhanced Emotion-Aware Chatbot")
        print("I can detect emotions and provide personalized responses!")
        print("Special commands:")
        print("  'insights' - Get emotional insights")
        print("  'stats' - See emotion statistics")
        print("  'save' - Save conversation")
        print("  'exit' - End conversation")
        print("=" * 60)
        
        session_start = datetime.datetime.now()
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle special commands
                if user_input.lower() == 'exit':
                    duration = datetime.datetime.now() - session_start
                    print(f"\nChatbot: Goodbye! We chatted for {duration.seconds // 60} minutes. Take care! 👋")
                    break
                elif user_input.lower() == 'insights':
                    insights = self.provide_emotion_insights()
                    print(f"\nChatbot: {insights}")
                    continue
                elif user_input.lower() == 'stats':
                    stats = self.show_emotion_statistics()
                    print(f"\nChatbot: {stats}")
                    continue
                elif user_input.lower() == 'save':
                    filename = self.save_conversation()
                    print(f"\nChatbot: Conversation saved to {filename}")
                    continue
                elif user_input == '':
                    print("Chatbot: Please type something!")
                    continue

                # Detect emotion and generate response
                emotion, confidence, all_emotions = self.detect_emotion(user_input)
                
                # Update user profile and emotion trend
                self.user_profile['emotion_count'][emotion] += 1
                self.emotion_trend.append(emotion)
                
                # Generate response
                response = self.generate_personalized_response(emotion, confidence, all_emotions, user_input)
                
                # Store conversation
                self.conversation_history.append({
                    'timestamp': datetime.datetime.now().isoformat(),
                    'user_input': user_input,
                    'detected_emotion': emotion,
                    'confidence': confidence,
                    'chatbot_response': response
                })
                
                # Display response with emotion info
                print(f"\nChatbot [{emotion.upper()} - {confidence*100:.1f}%]: {response}")
                
                # Occasionally offer insights
                if len(self.conversation_history) % 5 == 0 and len(self.conversation_history) > 0:
                    if random.random() < 0.3:  # 30% chance
                        insight = self.provide_emotion_insights()
                        print(f"\nChatbot [INSIGHT]: {insight}")
                        
            except KeyboardInterrupt:
                print(f"\n\nChatbot: Session interrupted. Goodbye! 👋")
                break
            except Exception as e:
                print(f"\nChatbot: Sorry, I encountered an error. Let's continue. ({str(e)})")

# Initialize and run the enhanced chatbot
if __name__ == "__main__":
    chatbot = EnhancedEmotionChatbot()
    chatbot.chat()
