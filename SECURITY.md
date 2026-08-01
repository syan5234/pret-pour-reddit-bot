# 🔒 Security Policy

## Overview

Pret Pour Support Bot is designed with security and privacy in mind. This document outlines the security measures and best practices for using this tool.

## Security Features

### ✅ Read-Only Mode
- **Never posts comments** or takes any write actions
- **Never votes** (upvote/downvote) on posts
- **Never creates posts** or sends private messages
- All responses must be **manually reviewed and posted** by the user

### ✅ Credential Protection
- Reddit API credentials are stored in environment variables
- `.env` file is **gitignored** and never committed
- No hardcoded credentials in source code
- Use `.env.example` as a template

### ✅ Data Privacy
- **No user-identifiable information** is collected or stored
- Only public Reddit post metadata is tracked (post ID, title, score, comments)
- Database stores minimal data needed for deduplication
- All data is stored locally on your machine

### ✅ Rate Limiting
- Respects Reddit API rate limits (60 requests/minute)
- Configurable delay between API calls (default: 2 seconds)
- Prevents accidental API abuse

### ✅ Input Validation
- Configuration settings are validated before execution
- Graceful error handling for API failures
- No shell command execution (prevents command injection)
- Parameterized SQL queries (prevents SQL injection)

## Best Practices

### 1. Credential Management
```bash
# Create .env file from template
cp .env.example .env

# Edit .env with your credentials
# NEVER commit .env to version control
```

### 2. Database Security
- SQLite database is stored locally
- Consider encrypting the database if storing sensitive data
- Regularly clean up old records with `cleanup_old_records()`
- Use `clear_database()` to remove all data when no longer needed

### 3. CSV Export Security
- CSV files contain public Reddit data only
- Store CSV files securely if archiving
- Delete CSV files when no longer needed

### 4. API Usage
- Monitor your Reddit API usage in Reddit app settings
- Stop the bot immediately if you notice unusual activity
- Report any security issues to the maintainers

## Known Limitations

1. **No encryption**: Database and CSV files are not encrypted
2. **Local storage only**: Data is stored on your local machine
3. **No authentication**: Anyone with access to your machine can run the bot

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:
- Do NOT open a public GitHub issue
- Contact the maintainers directly
- Provide detailed information about the vulnerability

## Security Checklist

Before using this bot, ensure you have:

- [ ] Created a secure `.env` file with your credentials
- [ ] Verified `.env` is in `.gitignore`
- [ ] Reviewed the code for any security concerns
- [ ] Understand the data being collected
- [ ] Have a plan for managing exported CSV files
- [ ] Know how to stop the bot quickly if needed

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
