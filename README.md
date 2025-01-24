# Content Creator Bot

Content Creator Bot is a Telegram bot designed to assist content creators in tracking their growth, providing dynamic content creation tips, and engaging them in a 21-day challenge to improve their reach and impact. The bot leverages APIs, machine learning, and automation to offer personalized guidance and performance tracking.

---

## Features

### 1. **Start Menu**
- The bot provides an intuitive start menu with options like:
  - 📚 **Content Creation Guide**
  - 🎯 **Start 21-Day Challenge**
  - 🚀 **Creator Tips for 2025**
  - 📊 **View Leaderboard**

### 2. **21-Day Challenge**
- Users can start a 21-day content creation challenge.
- Daily reminders encourage users to share their progress.
- Tracks user engagement metrics like views, likes, and comments.

### 3. **Dynamic Suggestions**
- Fetches dynamic tips for content creation and creator growth using predefined tips.
- Provides formatted and visually appealing responses with media.

### 4. **Sentiment Analysis**
- Uses Hugging Face's `distilbert-base-uncased-finetuned-sst-2-english` model to analyze sentiment in content.

### 5. **YouTube Metrics**
- Fetches YouTube video metrics (views, likes, and comments) using YouTube Data API.

### 6. **Leaderboard**
- Tracks and ranks users based on engagement metrics.

### 7. **Daily Reminders**
- Sends automated reminders for the challenge using `apscheduler`.

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/agusain2001/CreatorContentBot.git
    cd content-creator-bot
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set environment variables:**
    - `TELEGRAM_TOKEN`: Your Telegram bot token.
    - `YOUTUBE_API_KEY`: Your YouTube Data API key.
    - `GEMINI_API_KEY`: Your Google Gemini API key.

4. **Run the bot:**
    ```bash
    python bot.py
    ```

---

## Usage
- Start the bot by messaging `/start` to @Routine_2025_bot on Telegram.
- Use the main menu to explore features such as guides, challenges, and the leaderboard.
- Share your social handles and viral content to begin the 21-day challenge.
- Regularly update your content progress by sharing links and view counts.


### Commands

- **`/start`**: Initialize the bot and start interacting.
- **`/start_challenge`**: Begin the 21-day content creation challenge.
- **`/evaluate_challenge`**: Check your progress and eligibility for brand deals.
- **`/leaderboard`**: View the leaderboard rankings.

### Interaction Workflow

1. **Start**:
   - Use `/start` to interact with the bot.
   - Share your social handle and viral content when prompted.
2. **Engage**:
   - Use dynamic suggestions to improve your content creation skills.
   - Participate in the 21-day challenge.
3. **Track Progress**:
   - Regularly share your daily content links and metrics.
   - View your leaderboard position.
4. **Celebrate**:
   - Complete the challenge to unlock rewards and opportunities.

---

## Example Interactions

- **Start Command:**
  ```
  /start
  👋 Hi [User]! Welcome to the Content Creator Bot! Let’s make you a star 🌟.
  ```

- **Content Suggestions:**
  - Receive dynamic tips and guides on improving your content creation strategy.

- **Daily Reminders:**
  - Get notified to share content and track your growth during the challenge.

## Dependencies

- Python libraries:
  - `python-telegram-bot`
  - `transformers`
  - `googleapiclient`
  - `apscheduler`
  - `requests`


## API Usage

### YouTube Data API
- Fetches video metrics like views, likes, and comments.

### Hugging Face Sentiment Analysis
- Analyzes sentiment in user content.

### Google Gemini API
- Provides dynamic content suggestions (future integration).

---



## File Structure

```
.
├── bot.py                  # Main bot script
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## Technologies Used

- **Python Libraries**:
  - `telegram`: For bot interactions.
  - `apscheduler`: For scheduling daily reminders.
  - `transformers`: For sentiment analysis.
  - `googleapiclient`: For YouTube Data API integration.
- **APIs**:
  - Telegram Bot API
  - YouTube Data API
  - Google Gemini API

---

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Disclaimer

This bot uses APIs that may have usage limits. Ensure you have valid API keys and adhere to their usage policies.
