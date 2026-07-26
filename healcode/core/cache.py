"""
HealCode Caching Foundation (SQLite-backed)
With intelligent target path timestamp validation.
"""

import os
import sqlite3
import json
import time
from typing import Any, Optional
from healcode.exceptions import CacheError
from healcode.utils.logger import HealCodeLogger

logger = HealCodeLogger.get_logger()

class CacheManager:
    def __init__(self, db_path: str = ".healcode_cache.db") -> None:
        self.db_path = os.path.abspath(db_path)
        self.connection: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self) -> None:
        try:
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            
            # Check if table exists and has last_modified column
            try:
                cursor.execute("SELECT last_modified FROM cache LIMIT 1")
            except sqlite3.OperationalError:
                # Drop table to force recreation with new schema
                cursor.execute("DROP TABLE IF EXISTS cache")
                
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    expires_at REAL,
                    last_modified REAL
                )
            """)
            self.connection.commit()
            logger.debug(f"Cache database initialized at {self.db_path}")
        except Exception as e:
            raise CacheError(f"Failed to initialize SQLite cache database: {e}")

    def get(self, key: str, target_path: Optional[str] = None) -> Optional[Any]:
        if not self.connection:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT value, expires_at, last_modified FROM cache WHERE key = ?", (key,))
            row = cursor.fetchone()
            if not row:
                return None
            value_json, expires_at, cached_mtime = row
            if expires_at and expires_at < time.time():
                self.delete(key)
                return None
            
            # Check target path modification time for cache validation
            if target_path and os.path.exists(target_path):
                current_mtime = self._get_target_mtime(target_path)
                if cached_mtime and current_mtime > cached_mtime:
                    logger.debug(f"Cache invalidated for key '{key}' because target has been modified.")
                    self.delete(key)
                    return None

            return json.loads(value_json)
        except Exception as e:
            logger.warning(f"Cache get error for key '{key}': {e}")
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = 3600, target_path: Optional[str] = None) -> None:
        if not self.connection:
            return
        try:
            value_json = json.dumps(value)
            expires_at = time.time() + ttl_seconds if ttl_seconds > 0 else None
            last_modified = self._get_target_mtime(target_path) if target_path else time.time()
            
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO cache (key, value, expires_at, last_modified) VALUES (?, ?, ?, ?)",
                (key, value_json, expires_at, last_modified)
            )
            self.connection.commit()
        except Exception as e:
            logger.warning(f"Cache set error for key '{key}': {e}")

    def delete(self, key: str) -> None:
        if not self.connection:
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
            self.connection.commit()
        except Exception as e:
            logger.warning(f"Cache delete error for key '{key}': {e}")

    def clear(self) -> None:
        if not self.connection:
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM cache")
            self.connection.commit()
            logger.debug("Cache cleared successfully.")
        except Exception as e:
            raise CacheError(f"Failed to clear cache: {e}")

    def close(self) -> None:
        if self.connection:
            self.connection.close()
            self.connection = None

    def _get_target_mtime(self, target_path: str) -> float:
        try:
            if os.path.isdir(target_path):
                # Return maximum mtime of all files within target path to check if anything changed
                max_mtime = os.path.getmtime(target_path)
                for root, dirs, files in os.walk(target_path):
                    for file in files:
                        try:
                            mtime = os.path.getmtime(os.path.join(root, file))
                            if mtime > max_mtime:
                                max_mtime = mtime
                        except (FileNotFoundError, PermissionError):
                            pass
                return max_mtime
            return os.path.getmtime(target_path)
        except Exception:
            return time.time()
