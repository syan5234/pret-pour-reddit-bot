"""
Pret Pour Support Bot - Reddit Monitor

A read-only tool that monitors Reddit for questions about pret-pour.com.
This bot NEVER auto-posts comments or takes any write actions.
All responses must be manually reviewed and posted by the user.
"""

import time
import csv
import sys
from datetime import datetime
from typing import List, Dict

import praw
from dotenv import load_dotenv

from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDITS,
    KEYWORDS,
    MAX_POSTS_PER_SEARCH,
    TIME_FILTER,
    DATABASE_PATH,
    EXPORT_FILE,
    READ_ONLY,
    RATE_LIMIT_DELAY,
    MAX_DATABASE_RECORDS,
)
from database import PostDatabase


def print_banner():
    """Print the bot banner."""
    print("=" * 60)
    print("🤖 Pret Pour Support Bot")
    print("=" * 60)
    print(f"Monitoring: {', '.join(SUBREDDITS)}")
    print(f"Keywords: {', '.join(KEYWORDS)}")
    print(f"Mode: {'READ-ONLY' if READ_ONLY else 'WRITE'}")
    print("=" * 60)
    print()


def validate_config():
    """Validate configuration settings."""
    errors = []
    
    if not REDDIT_CLIENT_ID:
        errors.append("REDDIT_CLIENT_ID is not set")
    if not REDDIT_CLIENT_SECRET:
        errors.append("REDDIT_CLIENT_SECRET is not set")
    if not REDDIT_USER_AGENT:
        errors.append("REDDIT_USER_AGENT is not set")
    if not SUBREDDITS:
        errors.append("SUBREDDITS list is empty")
    if not KEYWORDS:
        errors.append("KEYWORDS list is empty")
    if MAX_POSTS_PER_SEARCH <= 0:
        errors.append("MAX_POSTS_PER_SEARCH must be positive")
    if RATE_LIMIT_DELAY < 1:
        errors.append("RATE_LIMIT_DELAY must be at least 1 second")
    
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)


def create_reddit_instance() -> praw.Reddit:
    """Create and return a Reddit API instance."""
    try:
        return praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
    except Exception as e:
        print(f"❌ Failed to create Reddit instance: {e}")
        sys.exit(1)


def search_subreddits(reddit: praw.Reddit, db: PostDatabase) -> List[Dict]:
    """Search subreddits for relevant posts.
    
    Returns list of new posts found.
    """
    new_posts = []
    
    for keyword in KEYWORDS:
        print(f"🔍 Searching for '{keyword}'...")
        
        try:
            subreddit = reddit.subreddit("+".join(SUBREDDITS))
            
            for post in subreddit.search(keyword, time_filter=TIME_FILTER, limit=MAX_POSTS_PER_SEARCH):
                post_data = {
                    "post_id": post.id,
                    "subreddit": str(post.subreddit),
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "url": f"https://reddit.com{post.permalink}",
                    "permalink": post.permalink,
                    "created_utc": datetime.fromtimestamp(post.created_utc),
                }
                
                # Check if we've seen this post before
                if not db.is_seen(post.id):
                    db.add_post(post_data)
                    new_posts.append(post_data)
            
            # Rate limiting
            time.sleep(RATE_LIMIT_DELAY)
            
        except praw.exceptions.RedditAPIException as e:
            print(f"⚠️  Reddit API error for keyword '{keyword}': {e}")
            continue
        except Exception as e:
            print(f"⚠️  Unexpected error for keyword '{keyword}': {e}")
            continue
    
    return new_posts


def display_post(post: Dict, index: int):
    """Display a post in a formatted way."""
    print(f"\n[{index}] 📌 NEW POST FOUND!")
    print(f"    Subreddit: r/{post['subreddit']}")
    print(f"    Title: {post['title']}")
    print(f"    Score: {post['score']} | Comments: {post['num_comments']}")
    print(f"    URL: {post['url']}")
    print()


def export_to_csv(posts: List[Dict], filename: str):
    """Export posts to CSV file."""
    if not posts:
        return
    
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=posts[0].keys())
            writer.writeheader()
            writer.writerows(posts)
        
        print(f"📄 Exported {len(posts)} posts to {filename}")
    except Exception as e:
        print(f"⚠️  Failed to export to CSV: {e}")


def main():
    """Main function."""
    # Safety check
    if not READ_ONLY:
        raise ValueError("READ_ONLY must be True. Auto-posting is disabled.")
    
    # Validate configuration
    validate_config()
    
    print_banner()
    
    # Initialize
    db = PostDatabase(DATABASE_PATH)
    reddit = create_reddit_instance()
    
    try:
        # Search for posts
        new_posts = search_subreddits(reddit, db)
        
        # Display results
        if new_posts:
            print(f"\n✅ Found {len(new_posts)} new posts!")
            print("-" * 60)
            
            for i, post in enumerate(new_posts, 1):
                display_post(post, i)
            
            # Export to CSV
            export_to_csv(new_posts, EXPORT_FILE)
        else:
            print("\n📭 No new posts found.")
        
        # Show stats
        stats = db.get_stats()
        print("\n📊 Database Stats:")
        print(f"   Total posts tracked: {stats['total_posts']}")
        print(f"   Unique subreddits: {stats['unique_subreddits']}")
        
        # Cleanup old records if needed
        db.cleanup_old_records(MAX_DATABASE_RECORDS)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitor stopped by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("✅ Monitor complete. Review posts and reply manually on Reddit.")
    print("=" * 60)


if __name__ == "__main__":
    main()
