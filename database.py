"""SQLite database handler for tracking seen posts

Privacy Note: This database only stores public Reddit post metadata.
No user-identifiable information is collected or stored.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class PostDatabase:
    """Handles SQLite database operations for tracking seen posts."""
    
    def __init__(self, db_path: str = "seen_posts.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
    
    def _create_tables(self):
        """Create tables if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_posts (
                post_id TEXT PRIMARY KEY,
                subreddit TEXT,
                title TEXT,
                score INTEGER,
                num_comments INTEGER,
                url TEXT,
                permalink TEXT,
                created_utc TIMESTAMP,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def is_seen(self, post_id: str) -> bool:
        """Check if a post has been seen before."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM seen_posts WHERE post_id = ?", (post_id,))
        return cursor.fetchone() is not None
    
    def add_post(self, post_data: Dict) -> bool:
        """Add a new post to the database.
        
        Returns True if added successfully, False if already exists.
        """
        if self.is_seen(post_data["post_id"]):
            return False
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO seen_posts (post_id, subreddit, title, score, 
                                   num_comments, url, permalink, created_utc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post_data["post_id"],
            post_data["subreddit"],
            post_data["title"],
            post_data["score"],
            post_data["num_comments"],
            post_data["url"],
            post_data["permalink"],
            post_data["created_utc"]
        ))
        self.conn.commit()
        return True
    
    def get_recent_posts(self, limit: int = 10) -> List[Dict]:
        """Get most recent posts from database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM seen_posts 
            ORDER BY first_seen DESC 
            LIMIT ?
        """, (limit,))
        
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM seen_posts")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT subreddit) FROM seen_posts")
        subreddits = cursor.fetchone()[0]
        
        return {
            "total_posts": total,
            "unique_subreddits": subreddits
        }
    
    def cleanup_old_records(self, max_records: int = 10000):
        """Remove old records if database exceeds max_records."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM seen_posts")
        count = cursor.fetchone()[0]
        
        if count > max_records:
            cursor.execute("""
                DELETE FROM seen_posts 
                WHERE post_id IN (
                    SELECT post_id FROM seen_posts 
                    ORDER BY first_seen ASC 
                    LIMIT ?
                )
            """, (count - max_records,))
            self.conn.commit()
    
    def clear_database(self):
        """Clear all records from database (use with caution)."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM seen_posts")
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        self.conn.close()
