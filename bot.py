import os
import logging
import requests
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from transformers import pipeline
from googleapiclient.discovery import build
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set your bot token, YouTube API Key, and Gemini API Key
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://ai.googleapis.com/v1/projects/scraper1-448307/locations/global/models/gemini-pro:generateContent"

if not TELEGRAM_TOKEN or not YOUTUBE_API_KEY or not GEMINI_API_KEY:
    raise ValueError("API keys or tokens are not set in environment variables.")

# Database to track user data and progress
USER_DATABASE = {}

# Hugging Face Sentiment Analysis Pipeline
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_analyzer = pipeline("sentiment-analysis", model=MODEL_NAME, revision="714eb0f")

# YouTube API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Scheduler for automated tasks
scheduler = BackgroundScheduler()
scheduler.start()

# Function to fetch YouTube metrics
async def fetch_youtube_metrics(url):
    try:
        video_id = url.split("v=")[-1]
        response = youtube.videos().list(part="statistics", id=video_id).execute()
        stats = response["items"][0]["statistics"]
        return {
            "views": stats.get("viewCount", "0"),
            "likes": stats.get("likeCount", "0"),
            "comments": stats.get("commentCount", "0"),
        }
    except Exception as e:
        logger.error(f"Error fetching YouTube metrics: {e}")
        return {"views": "0", "likes": "0", "comments": "0"}

# Function to perform sentiment analysis
async def analyze_content(content: str):
    analysis = sentiment_analyzer(content[:512])
    sentiment = analysis[0]["label"]
    score = analysis[0]["score"]
    return sentiment, score

# Automated daily reminders
async def send_daily_reminders(context: ContextTypes.DEFAULT_TYPE):
    for user_id, data in USER_DATABASE.items():
        if "progress" in data:
            await context.bot.send_message(
                chat_id=user_id,
                text="🔔 Reminder: Don’t forget to share your content for today’s challenge!"
            )

# Schedule reminders every day at a fixed time
scheduler.add_job(
    lambda: ApplicationBuilder().token(TELEGRAM_TOKEN).build().job_queue.run_once(send_daily_reminders, 0),
    trigger="interval",
    days=1
)

# Post-challenge evaluation with Creatorship Workflow
async def evaluate_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = USER_DATABASE.get(user_id)
    if not user_data or "progress" not in user_data:
        await update.message.reply_text("You haven't completed the challenge yet.")
        return

    total_days = len(user_data["progress"])
    total_views = sum(
        int(day_data.get("metrics", {}).get("views", 0)) for day_data in user_data["progress"].values()
    )
    
    # Example criteria for eligibility
    if total_days >= 21 and total_views > 10000:
        # Send congratulatory message
        await update.message.reply_text(
            f"🎉 **Congratulations, {user_data['name']}!** 🎉\n\n"
            f"📅 Total Days: {total_days}\n👀 Total Views: {total_views}\n\n"
            "🏆 You’ve been shortlisted for brand deals and creator opportunities!\n"
            "💌 Please fill out [this form](https://example.com/form) to proceed further.\n\n"
            "Keep up the amazing work! 🌟",
            parse_mode="Markdown"
        )
        # Update user data to mark them as eligible
        user_data["eligible"] = True
    else:
        # Notify users who didn't meet the criteria
        await update.message.reply_text(
            f"👏 **Good effort, {user_data['name']}!** 👏\n\n"
            f"📅 Total Days: {total_days}\n👀 Total Views: {total_views}\n\n"
            "Keep improving to unlock more opportunities in the future! 🚀"
        )

# Function to fetch dynamic suggestions using Google Gemini AI
def fetch_dynamic_suggestions(topic: str):

    
    # Predefined guides with enhanced UI
    content_creation_tips = [
        "🎯 **Identify Your Niche:** Focus on a specific area of expertise that you love and excel in.",
        "📊 **Know Your Audience:** Analyze their demographics, interests, and preferences.",
        "🌟 **Follow Trends:** Use tools like Google Trends to discover what’s popular in your niche.",
        "🗓️ **Stay Consistent:** Create a content calendar to ensure regular posting.",
        "⏳ **Batch-Create Content:** Dedicate time to produce multiple pieces in one go.",
        "🎨 **Leverage Visual Tools:** Use apps like Canva or Adobe Spark for professional designs.",
        "🖋️ **Craft Engaging Headlines:** Catch attention with creative titles.",
        "📖 **Tell a Story:** Make your content relatable and emotional to connect with your audience.",
        "🔄 **Repurpose Content:** Turn one piece into multiple formats (e.g., blog to video).",
        "📈 **Track Performance:** Use analytics tools to see what’s working and refine your strategy.",
        "🤝 **Collaborate:** Work with creators in your niche to expand your reach.",
        "💬 **Engage with Followers:** Respond to comments and messages actively.",
        "🏷️ **Use Hashtags Wisely:** Expand your reach with relevant hashtags.",
        "⏰ **Timing Matters:** Post when your audience is most active.",
        "💡 **Invest in Tools:** Good lighting and sound equipment elevate your content.",
        "🎥 **Experiment with Formats:** Try videos, reels, blogs, or other content types.",
        "🔑 **Stay Authentic:** Be yourself; audiences love genuine creators.",
        "📢 **Call-to-Action:** Encourage followers to like, comment, or share.",
        "🎓 **Educate, Entertain, or Inspire:** Provide value with every post.",
        "🌐 **Learn SEO:** Improve discoverability on platforms and search engines.",
    ]

    creator_tips_2025 = [
        "🎥 **Master Short-Form Videos:** Platforms like TikTok and YouTube Shorts are booming.",
        "🌌 **Explore the Metaverse:** Use AR/VR content and virtual events to engage audiences.",
        "🤖 **Leverage AI Tools:** Use ChatGPT for scripting, ideation, and planning.",
        "✨ **Build a Personal Brand:** Stay consistent across platforms with your unique voice.",
        "📈 **Adapt to Algorithms:** Stay updated with changes on platforms like Instagram and YouTube.",
        "🔒 **Exclusive Content:** Offer memberships or subscriptions for premium content.",
        "🎞️ **Learn Editing:** Tools like Premiere Pro or CapCut make your content professional.",
        "🎭 **Create Interactive Content:** Use polls, quizzes, and live streams to engage your followers.",
        "🌐 **Join Niche Platforms:** Communities on Discord or Threads can grow your base.",
        "🤝 **Collaborate:** Work with micro-influencers for targeted reach.",
        "💰 **Monetization Strategy:** Use affiliate marketing, ads, or brand sponsorships.",
        "📧 **Email Marketing:** Build a direct line to your audience through newsletters.",
        "📊 **Data-Driven Decisions:** Use insights to refine and improve your content.",
        "🌍 **Go Multilingual:** Break language barriers to reach global audiences.",
        "🌀 **360° Content:** Try immersive formats like VR videos for new experiences.",
        "🌿 **Sustainability Focus:** Align your content with eco-conscious trends.",
        "🤝 **Team Up:** Build a network to handle different aspects of content creation.",
        "📚 **Focus on Evergreen Content:** Ensure your work remains valuable over time.",
        "💎 **Stay Transparent:** Build trust by being open with your audience.",
        "🛠️ **Diversify Revenue Streams:** Explore merch, courses, or eBooks.",
    ]

    # Select random tips and format them with enhanced UI
    if topic == "Content Creation Guide":
        tips = random.sample(content_creation_tips, 4)
    elif topic == "Creator Tips for 2025":
        tips = random.sample(creator_tips_2025, 4)
    else:
        return ["❌ No suggestions available at the moment."]

    # Add formatting and animations (text-based)
    formatted_tips = "\n\n".join(tips)
    animated_response = (
        f"✨ **{topic}** ✨\n\n"
        f"Here are some top tips to level up your game:\n\n"
        f"{formatted_tips}\n\n"
        "💡 Keep creating and shining! 🌟"
    )
    return animated_response
    

# Main menu keyboard
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Content Creation Guide", callback_data="guide")],
        [InlineKeyboardButton("🎯 Start 21-Day Challenge", callback_data="challenge")],
        [InlineKeyboardButton("🚀 Creator Tips for 2025", callback_data="creator2025")],
        [InlineKeyboardButton("📊 View Leaderboard", callback_data="leaderboard")],
    ]
    return InlineKeyboardMarkup(keyboard)


# Bot Commands and Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    USER_DATABASE[user.id] = {"name": user.first_name, "progress": {}, "social_handle": None, "viral_content": None}
    await update.message.reply_text(
        f"👋 **Hi {user.first_name}!** 🎉\n\n"
        "Welcome to the **Content Creator Bot**! Let’s make you a star 🌟.\n\n"
        "📥 Share your social handle or viral content to begin.",
        reply_markup=main_menu_keyboard(),
    )


async def collect_social_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = USER_DATABASE.get(user_id, {})
    user_input = update.message.text

    if not user_data.get("social_handle"):
        user_data["social_handle"] = user_input
        await update.message.reply_text("✅ Social handle saved! Share your most viral content (link + view count).")
    elif not user_data.get("viral_content"):
        user_data["viral_content"] = user_input
        await update.message.reply_text("✅ Viral content saved! Now you’re ready to start the 21-day challenge.")

    USER_DATABASE[user_id] = user_data

async def start_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USER_DATABASE[user_id]["progress"] = {}
    await update.message.reply_text(
        "🎉 The 21-day Createathon Challenge has started! 🎯\n\n"
        "Each day, share your content (link + views). Let’s track your growth!"
    )

# Notify eligible users with media
async def notify_eligible_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = USER_DATABASE.get(user_id)
    if user_data and user_data.get("eligible"):
        # Example GIF URL (replace with your hosted media or Telegram file ID)
        gif_url = "https://example.com/congratulations.gif"

        await context.bot.send_animation(
            chat_id=user_id,
            animation=gif_url,
            caption=(
                "🎉 **Congratulations!** 🎉\n\n"
                "You’ve been shortlisted for brand deals and creator opportunities!\n\n"
                "💌 Please fill out [this form](https://example.com/form) to proceed further.\n\n"
                "Keep shining! 🌟"
            ),
            parse_mode="Markdown"
        )


# Enhanced response for guides with media
async def dynamic_suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query.data
    topic = "Content Creation Guide" if query == "guide" else "Creator Tips for 2025"
    suggestions = fetch_dynamic_suggestions(topic)
    
    # Example image URLs (replace with your actual hosted media or Telegram file IDs)
    guide_image_url = "https://example.com/content_creation_guide_image.jpg"
    creator_image_url = "https://example.com/creator_tips_2025_image.jpg"

    # Select appropriate image based on topic
    image_url = guide_image_url if topic == "Content Creation Guide" else creator_image_url

    # Send media and suggestions
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=image_url,
        caption=f"✨ **{topic}** ✨\n\nHere are some top tips to level up your game:\n\n{suggestions}\n\n💡 Keep creating and shining! 🌟",
        parse_mode="Markdown"
    )


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaderboard = calculate_leaderboard()
    if not leaderboard:
        await update.message.reply_text("No leaderboard data yet. Start posting content to join!")
        return

    leaderboard_text = "\n".join(
        [f"{rank + 1}. {name}: {engagement} points" for rank, (name, engagement) in enumerate(leaderboard)]
    )
    await update.message.reply_text(f"🏆 **Leaderboard:**\n\n{leaderboard_text}")

def calculate_leaderboard():
    leaderboard = []
    for user_id, data in USER_DATABASE.items():
        total_engagement = sum(
            int(day_data.get("metrics", {}).get("views", 0)) +
            int(day_data.get("metrics", {}).get("likes", 0)) +
            int(day_data.get("metrics", {}).get("comments", 0))
            for day_data in data.get("progress", {}).values()
        )
        leaderboard.append((data["name"], total_engagement))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(
        "Welcome back to the main menu! Choose an option below:",
        reply_markup=main_menu_keyboard(),
    )

# Main function
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_challenge", start_challenge))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_social_handle))
    application.add_handler(CommandHandler("evaluate_challenge", evaluate_challenge))
    application.add_handler(CommandHandler("leaderboard", show_leaderboard))
    application.add_handler(CallbackQueryHandler(dynamic_suggestions, pattern="^(guide|creator2025)$"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="menu"))

    application.run_polling()

if __name__ == "__main__":
    main()
