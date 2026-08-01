# 🤖 Pret Pour Support Bot

A Reddit monitoring tool that helps you find and respond to questions about pret-pour.com.

## ✨ Features

- 🔍 Monitors multiple subreddits for relevant questions
- 🎯 Keyword-based search with smart filtering
- 📊 Post scoring to prioritize high-value discussions
- 💾 SQLite database to track seen posts (avoid duplicates)
- 📝 Export results to CSV for analysis
- 🔒 **Read-only** — never auto-posts or takes write actions

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/syan5234/pret-pour-reddit-bot.git
cd pret-pour-reddit-bot

# Install dependencies
pip install -r requirements.txt

# Configure Reddit API credentials
cp .env.example .env
# Edit .env with your credentials (get them from https://www.reddit.com/prefs/apps)

# Run the monitor
python monitor.py
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Subreddits to monitor
SUBREDDITS = ["webdev", "startups", "smallbusiness"]

# Keywords to search for
KEYWORDS = ["pret-pour", "pret pour"]

# Search frequency (in hours)
CHECK_INTERVAL = 1

# Maximum posts to fetch per search
MAX_POSTS = 25
```

## 📊 Output Example

```
============================================================
Pret Pour Support Bot - Monitor Mode
============================================================
Monitoring subreddits: webdev, startups, smallbusiness
Keywords: pret-pour, pret pour
Mode: READ-ONLY (no auto-posting)
============================================================

[2024-01-15 10:30] New post found!
  Subreddit: r/webdev
  Title: How to use pret-pour.com for quick prototyping?
  Score: 15 | Comments: 8
  URL: https://reddit.com/r/webdev/abc123

[2024-01-15 10:31] New post found!
  Subreddit: r/startups
  Title: Best tools for rapid deployment?
  Score: 42 | Comments: 23
  URL: https://reddit.com/r/startups/def456
```

## 🛡️ Safety Features

- ✅ **Read-only mode** — never posts comments automatically
- ✅ **Rate limiting** — respects Reddit API limits
- ✅ **Duplicate detection** — tracks seen posts in SQLite
- ✅ **Manual review** — you decide what to respond to

## 📁 Project Structure

```
pret-pour-reddit-bot/
├── monitor.py          # Main monitoring script
├── config.py           # Configuration settings
├── database.py         # SQLite database handler
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PRAW](https://praw.readthedocs.io/) - The Python Reddit API Wrapper
- Reddit API for providing access to community discussions
