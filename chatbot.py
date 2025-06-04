import os
import json
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_chatbot_response(user_message, user_id=None):
    """
    Get response from ChatGPT for customer support
    """
    try:
        # System prompt for e-commerce customer support
        system_prompt = """
        You are an AI customer support assistant for an e-commerce platform. 
        You are helpful, friendly, and knowledgeable about:
        - Order tracking and status
        - Return and refund policies
        - Product information and recommendations
        - Account management
        - Shipping information
        - General shopping assistance
        
        Always be polite and professional. If you cannot help with something specific,
        direct the user to contact human support. Keep responses concise but helpful.
        
        Company policies:
        - Free shipping on orders over $50
        - 30-day return policy for most items
        - 24-48 hour processing time for orders
        - Customer service available 24/7
        """
        
        # Add user context if available
        context = ""
        if user_id:
            context = f"\nUser ID: {user_id}"
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt + context},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        logger.info(f"Chatbot response generated for user {user_id}")
        return ai_response
        
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        
        # Fallback responses for common scenarios
        fallback_responses = {
            "track": "I'd be happy to help you track your order! Please provide your order number and I'll look it up for you. You can also check your order status in the Orders section of your account.",
            "return": "Our return policy allows returns within 30 days of purchase. Items must be in original condition. You can start a return from your Orders page or contact our support team for assistance.",
            "shipping": "We offer free shipping on orders over $50. Standard shipping takes 3-5 business days, and expedited shipping is available for faster delivery.",
            "default": "I apologize, but I'm having trouble processing your request right now. Please try again in a moment, or contact our customer service team for immediate assistance."
        }
        
        # Simple keyword matching for fallback
        message_lower = user_message.lower()
        if any(word in message_lower for word in ["track", "order", "status"]):
            return fallback_responses["track"]
        elif any(word in message_lower for word in ["return", "refund", "exchange"]):
            return fallback_responses["return"]
        elif any(word in message_lower for word in ["ship", "delivery", "shipping"]):
            return fallback_responses["shipping"]
        else:
            return fallback_responses["default"]

def get_product_recommendation_response(user_preferences, user_id=None):
    """
    Get product recommendations from ChatGPT based on user preferences
    """
    try:
        system_prompt = """
        You are an AI shopping assistant that provides personalized product recommendations.
        Based on user preferences, suggest relevant products from our catalog.
        Be specific about product features and explain why you're recommending them.
        Keep recommendations relevant to our e-commerce platform categories:
        Electronics, Clothing, Books, Home & Garden, Sports.
        """
        
        prompt = f"Based on these preferences: {user_preferences}, recommend 3 products that would be perfect for this customer. Explain why each recommendation fits their needs."
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Product recommendation error: {e}")
        return "I'd be happy to help you find the perfect products! Could you tell me more about what you're looking for? For example, your budget, preferred category, or specific features you need?"

def analyze_customer_sentiment(message):
    """
    Analyze customer sentiment to provide better support
    """
    try:
        system_prompt = """
        Analyze the sentiment of this customer message. Respond with JSON in this format:
        {"sentiment": "positive/neutral/negative", "confidence": 0.0-1.0, "urgency": "low/medium/high"}
        
        Consider urgency based on:
        - Complaints or problems: high urgency
        - Questions or requests: medium urgency  
        - Compliments or general chat: low urgency
        """
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},
            max_tokens=200
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return {"sentiment": "neutral", "confidence": 0.5, "urgency": "medium"}

def generate_personalized_email(user_id, email_type="welcome"):
    """
    Generate personalized email content using ChatGPT
    """
    try:
        email_prompts = {
            "welcome": "Write a welcoming email for a new customer who just signed up for our e-commerce platform. Make it warm and highlight key features.",
            "abandoned_cart": "Write an email to encourage a customer to complete their purchase. Be friendly and offer assistance.",
            "order_confirmation": "Write an order confirmation email that's professional but friendly. Include next steps.",
            "shipping_notification": "Write a shipping notification email with tracking information placeholder."
        }
        
        prompt = email_prompts.get(email_type, email_prompts["welcome"])
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an email marketing specialist for an e-commerce platform. Write engaging, personalized emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Email generation error: {e}")
        return "Thank you for choosing our platform! We're excited to serve you."
