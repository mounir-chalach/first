"""
Caching utilities for MASI Dashboard
Provides data caching with TTL support
"""

import pickle
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheManager:
    """Manage cache files with TTL support"""

    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a given key"""
        safe_key = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)
        return self.cache_dir / f"{safe_key}.pkl"

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        Cache a value with TTL

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        Returns:
            True if successful, False otherwise
        """
        try:
            cache_path = self._get_cache_path(key)
            cache_data = {
                'value': value,
                'timestamp': datetime.now(),
                'ttl': ttl
            }

            with open(cache_path, 'wb') as f:
                pickle.dump(cache_data, f)

            logger.debug(f"Cached data for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error caching data for {key}: {str(e)}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve cached value if not expired

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        try:
            cache_path = self._get_cache_path(key)

            if not cache_path.exists():
                return None

            with open(cache_path, 'rb') as f:
                cache_data = pickle.load(f)

            # Check if expired
            timestamp = cache_data['timestamp']
            ttl = cache_data['ttl']

            if datetime.now() > timestamp + timedelta(seconds=ttl):
                logger.debug(f"Cache expired for key: {key}")
                cache_path.unlink()  # Delete expired cache
                return None

            logger.debug(f"Cache hit for key: {key}")
            return cache_data['value']
        except Exception as e:
            logger.error(f"Error retrieving cache for {key}: {str(e)}")
            return None

    def delete(self, key: str) -> bool:
        """Delete a cache entry"""
        try:
            cache_path = self._get_cache_path(key)
            if cache_path.exists():
                cache_path.unlink()
                logger.debug(f"Deleted cache for key: {key}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting cache for {key}: {str(e)}")
            return False

    def clear_all(self) -> int:
        """Clear all cache files"""
        try:
            count = 0
            for cache_file in self.cache_dir.glob("*.pkl"):
                cache_file.unlink()
                count += 1
            logger.info(f"Cleared {count} cache files")
            return count
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return 0

    def clear_expired(self) -> int:
        """Clear only expired cache files"""
        try:
            count = 0
            for cache_file in self.cache_dir.glob("*.pkl"):
                try:
                    with open(cache_file, 'rb') as f:
                        cache_data = pickle.load(f)

                    timestamp = cache_data['timestamp']
                    ttl = cache_data['ttl']

                    if datetime.now() > timestamp + timedelta(seconds=ttl):
                        cache_file.unlink()
                        count += 1
                except:
                    # If we can't read it, delete it
                    cache_file.unlink()
                    count += 1

            logger.info(f"Cleared {count} expired cache files")
            return count
        except Exception as e:
            logger.error(f"Error clearing expired cache: {str(e)}")
            return 0


# Global cache manager instance
_cache_manager = CacheManager()


def cache_data(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Cache data with TTL

    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds (default: 1 hour)

    Returns:
        True if successful
    """
    return _cache_manager.set(key, value, ttl)


def get_cached_data(key: str) -> Optional[Any]:
    """
    Get cached data if available and not expired

    Args:
        key: Cache key

    Returns:
        Cached value or None
    """
    return _cache_manager.get(key)


def clear_cache(key: str = None) -> bool:
    """
    Clear cache for a specific key or all cache

    Args:
        key: Cache key to clear, or None to clear all

    Returns:
        True if successful
    """
    if key:
        return _cache_manager.delete(key)
    else:
        _cache_manager.clear_all()
        return True


def clear_expired_cache() -> int:
    """
    Clear expired cache entries

    Returns:
        Number of entries cleared
    """
    return _cache_manager.clear_expired()
