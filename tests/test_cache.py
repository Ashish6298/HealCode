"""
Tests for SQLite Caching
"""

import os
import tempfile
import time
from healcode.core.cache import CacheManager

def test_cache_set_get_clear() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "cache.db")
        cache = CacheManager(db_path=db_path)
        
        # Test basic set/get
        cache.set("key1", {"data": "value1"}, ttl_seconds=10)
        val = cache.get("key1")
        assert val == {"data": "value1"}

        # Test TTL expiration
        cache.set("key2", "expired_val", ttl_seconds=1)
        time.sleep(1.1)
        assert cache.get("key2") is None

        # Test clear
        cache.set("key3", "some_data", ttl_seconds=60)
        cache.clear()
        assert cache.get("key3") is None

        cache.close()
