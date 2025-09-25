# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Search optimization utilities for batching and caching"""

import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from google.adk.tools import google_search
from config import CACHE_CONFIG, OPTIMIZATIONS

class SearchCache:
    """Simple in-memory cache for search results"""

    def __init__(self, ttl_seconds: int = 3600, max_size: int = 100):
        self.cache = {}
        self.ttl = ttl_seconds
        self.max_size = max_size
        self.access_times = {}

    def _make_key(self, query: str) -> str:
        """Create a cache key from a query"""
        return hashlib.md5(query.encode()).hexdigest()

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached result if available and not expired"""
        if not OPTIMIZATIONS["enable_caching"]:
            return None

        key = self._make_key(query)
        if key in self.cache:
            cached_time = self.access_times.get(key, 0)
            if time.time() - cached_time < self.ttl:
                return self.cache[key]
            else:
                # Expired, remove from cache
                del self.cache[key]
                del self.access_times[key]
        return None

    def set(self, query: str, result: Dict[str, Any]):
        """Cache a search result"""
        if not OPTIMIZATIONS["enable_caching"]:
            return

        # Implement simple LRU by removing oldest if at max size
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            del self.access_times[oldest_key]

        key = self._make_key(query)
        self.cache[key] = result
        self.access_times[key] = time.time()

# Global cache instance
_search_cache = SearchCache(
    ttl_seconds=CACHE_CONFIG["ttl_seconds"],
    max_size=CACHE_CONFIG["max_size"]
)

def batch_google_search(queries: List[str], max_workers: int = 3) -> List[Dict[str, Any]]:
    """
    Execute multiple Google searches in parallel with caching

    Args:
        queries: List of search queries
        max_workers: Maximum number of parallel searches

    Returns:
        List of search results in the same order as queries
    """
    results = [None] * len(queries)
    queries_to_fetch = []
    indices_to_fetch = []

    # Check cache first
    for i, query in enumerate(queries):
        cached = _search_cache.get(query)
        if cached:
            results[i] = cached
        else:
            queries_to_fetch.append(query)
            indices_to_fetch.append(i)

    if not queries_to_fetch:
        return results

    # Batch execute uncached queries
    if OPTIMIZATIONS["batch_search"]:
        # Execute in parallel
        with ThreadPoolExecutor(max_workers=min(max_workers, len(queries_to_fetch))) as executor:
            futures = []
            for query in queries_to_fetch:
                future = executor.submit(google_search.invoke, {'query': query})
                futures.append(future)

            # Collect results
            for i, future in enumerate(futures):
                result = future.result()
                idx = indices_to_fetch[i]
                results[idx] = result
                # Cache the result
                _search_cache.set(queries_to_fetch[i], result)
    else:
        # Sequential execution (fallback)
        for i, query in enumerate(queries_to_fetch):
            result = google_search.invoke({'query': query})
            idx = indices_to_fetch[i]
            results[idx] = result
            _search_cache.set(query, result)

    return results

def optimize_search_queries(queries: List[str]) -> List[str]:
    """
    Optimize search queries by:
    1. Removing duplicates
    2. Combining similar queries
    3. Adding search operators for better results
    """
    optimized = []
    seen = set()

    for query in queries:
        # Normalize query
        normalized = query.lower().strip()

        # Skip duplicates
        if normalized in seen:
            continue
        seen.add(normalized)

        # Add search operators for better precision
        if "real estate" in normalized and "site:" not in normalized:
            # Add real estate sites for better results
            query = f'{query} (site:zillow.com OR site:realtor.com OR site:redfin.com)'
        elif "M&A" in normalized or "acquisition" in normalized:
            # Add business news sites
            query = f'{query} (site:bloomberg.com OR site:reuters.com OR site:wsj.com)'

        optimized.append(query)

    return optimized

def create_batched_search_tool():
    """Create a FunctionTool for batched searching"""
    from google.adk.tools import FunctionTool

    def batched_search_wrapper(
        real_estate_queries: List[str],
        financial_queries: List[str]
    ) -> Dict[str, Any]:
        """Execute batched and cached Google searches for better performance."""

        # Optimize queries
        real_estate_queries = optimize_search_queries(real_estate_queries)
        financial_queries = optimize_search_queries(financial_queries)

        # Execute in parallel batches
        all_queries = real_estate_queries + financial_queries
        all_results = batch_google_search(all_queries)

        # Split results back
        real_estate_results = all_results[:len(real_estate_queries)]
        financial_results = all_results[len(real_estate_queries):]

        return {
            'real_estate_results': real_estate_results,
            'financial_results': financial_results,
            'queries_processed': len(all_queries),
            'cache_hits': sum(1 for r in all_results if r and r.get('from_cache', False))
        }

    return FunctionTool(
        func=batched_search_wrapper
    )

def clear_cache():
    """Clear the search cache"""
    global _search_cache
    _search_cache = SearchCache(
        ttl_seconds=CACHE_CONFIG["ttl_seconds"],
        max_size=CACHE_CONFIG["max_size"]
    )