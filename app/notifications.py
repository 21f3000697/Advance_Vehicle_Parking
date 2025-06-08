from datetime import datetime, timedelta
import random

class SmartNotificationSystem:
    def __init__(self):
        self.weather_alerts = {
            'rain': 'Don\'t forget your umbrella! We\'ve prioritized covered parking spots for you.',
            'snow': 'Weather alert: Snow expected. We\'ve reserved spots closer to exits for your convenience.',
            'storm': 'Severe weather alert! Consider using our covered parking areas.',
            'sunny': 'Perfect weather for our open-air spots! Save on covered parking rates today.'
        }
        
        self.time_based_messages = {
            'morning': [
                'Beat the rush hour! Early bird discounts active until 7 AM.',
                'Good morning! Traffic prediction: {} congestion expected.',
                'Breakfast special: Park before 8 AM and get ₹50 off at our café!'
            ],
            'evening': [
                'Evening plans? Extended parking rates available after 6 PM.',
                'Beat the evening rush! Premium spots still available.',
                'Night parking special: Flat rate of ₹100 after 8 PM!'
            ]
        }

    def generate_smart_reminder(self, reservation, user_behavior_score):
        """
        Generate personalized reminders based on user behavior and context
        """
        time_to_expiry = reservation.end_time - datetime.now()
        message = None
        
        if time_to_expiry < timedelta(minutes=30):
            if user_behavior_score >= 80:
                message = f"Gentle reminder: Your parking session ends in {time_to_expiry.minutes} minutes. Need an extension?"
            else:
                message = f"Important: Your parking session expires in {time_to_expiry.minutes} minutes. Please extend or move your vehicle."
                
        return message

    def create_environmental_impact_message(self, impact_score):
        """
        Generate eco-friendly messaging based on user's environmental impact
        """
        if impact_score >= 90:
            return "🌟 Eco-warrior alert! Your sustainable parking choices are making a difference!"
        elif impact_score >= 70:
            return "🌿 Great job on choosing eco-friendly parking options!"
        elif impact_score >= 50:
            return "🌱 Small changes make a big impact. Try our EV spots next time!"
        else:
            return "💡 Tip: Choose covered parking or EV spots to increase your eco-score!"

    def generate_loyalty_notification(self, user):
        """
        Create personalized loyalty program notifications
        """
        points_to_next_tier = 0
        current_tier = ""
        
        if user.loyalty_points < 200:
            points_to_next_tier = 200 - user.loyalty_points
            current_tier = "Bronze"
        elif user.loyalty_points < 500:
            points_to_next_tier = 500 - user.loyalty_points
            current_tier = "Silver"
        elif user.loyalty_points < 1000:
            points_to_next_tier = 1000 - user.loyalty_points
            current_tier = "Gold"
            
        if points_to_next_tier > 0:
            return f"You're just {points_to_next_tier} points away from {current_tier}! Park with us this weekend for 2x points!"
        else:
            return "Congratulations on reaching Platinum status! Enjoy your premium benefits!"

    def create_smart_offer(self, user, current_weather):
        """
        Generate personalized offers based on user behavior and conditions
        """
        if current_weather in ['rain', 'snow']:
            return f"Weather protection offer: ₹50 off covered parking spots today!"
            
        if datetime.now().weekday() >= 5:  # Weekend
            return "Weekend special: Double loyalty points and ₹100 off on 4+ hours parking!"
            
        if 6 <= datetime.now().hour <= 9:  # Morning rush
            return "Early bird offer: Park before 7 AM for just ₹60/hour!"
            
        return "Standard rates apply. Book now to secure your spot!"

    def generate_gamification_message(self, user):
        """
        Create engaging gamification messages
        """
        achievements = []
        
        if user.total_bookings >= 50:
            achievements.append("🏆 Parking Pro (50+ bookings)")
        if user.loyalty_points >= 1000:
            achievements.append("👑 Platinum Parker")
        if len([r for r in user.reservations if r.payment_status == 'completed']) >= 20:
            achievements.append("💫 Reliable Regular")
            
        if achievements:
            return f"Your parking achievements: {', '.join(achievements)}"
        else:
            return "Start parking with us to earn exciting achievements!"

    def get_congestion_prediction(self, lot, time):
        """
        Predict parking lot congestion (simplified version)
        """
        hour = time.hour
        weekday = time.weekday()
        
        if weekday < 5:  # Weekday
            if 7 <= hour <= 9:  # Morning rush
                return "High"
            elif 16 <= hour <= 18:  # Evening rush
                return "High"
            elif 10 <= hour <= 15:  # Business hours
                return "Medium"
            else:
                return "Low"
        else:  # Weekend
            if 10 <= hour <= 18:  # Shopping hours
                return "Medium"
            else:
                return "Low" 