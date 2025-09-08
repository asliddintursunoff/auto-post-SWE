# SWE Topics Telegram Bot with Gemini

Automatically generates creative posts about Software Engineering (SWE) topics and sends them to your Telegram channel using Gemini.

---

## Features

- Fetches Software Engineering topics and facts.
- Generates creative, engaging, HTML-formatted posts with Gemini.
- Automatically schedules and posts to Telegram at multiple times per day.
- Fully configurable with environment variables.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/asliddintursunoff/auto-post-SWE.git
cd auto-post-SWE
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```
BOT_TOKEN=your_telegram_bot_token
CHANNEL_ID=@your_channel_id
```

- `BOT_TOKEN`: Telegram bot token from [BotFather](https://t.me/BotFather)  
- `CHANNEL_ID`: Your Telegram channel ID (must be a channel where your bot is an admin)

---

## Usage

Run the bot:

```bash
python post_maker.py
```

The bot automatically schedules posts three times a day at randomized minutes:

- (10:00-11:00)
- (14:00-15:00)
- (20:00-21:00)  

You can adjust these times in the code.

---

## File Structure

```
my_project/
├── .gitignore        # Ignore environment, pycache, logs
├── README.md         # This file
├── requirements.txt  # Python dependencies
├── main.py # running project
├── post_maker.py     # Main scheduler and Telegram sender
└── swe_topics.py          # topics about Software Engineering
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---



