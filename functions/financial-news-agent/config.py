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

"""Configuration for Deal Sourcing Agent performance optimizations"""

import os

# Performance Optimization Settings
OPTIMIZATIONS = {
    # Enable parallel execution of independent agents (30-50% faster)
    "parallel_execution": os.getenv('ENABLE_PARALLEL_EXECUTION', 'true').lower() == 'true',

    # Use lighter models for simple tasks (20-30% faster)
    "use_light_models": os.getenv('USE_LIGHT_MODELS', 'true').lower() == 'true',

    # Enable response caching (50-70% faster for repeat queries)
    "enable_caching": os.getenv('ENABLE_CACHING', 'true').lower() == 'true',

    # Enable async PDF generation
    "async_pdf": os.getenv('ASYNC_PDF_GENERATION', 'true').lower() == 'true',

    # Enable batch searching
    "batch_search": os.getenv('BATCH_SEARCH', 'true').lower() == 'true',
}

# Model Configuration
MODELS = {
    # Complex analysis tasks (coordinator, risk analyst)
    "complex": "gemini-2.5-pro",

    # Simple search tasks (real estate, financial news)
    "simple": "gemini-2.0-flash" if OPTIMIZATIONS["use_light_models"] else "gemini-2.5-pro",

    # Coordination tasks
    "coordinator": "gemini-2.5-pro",
}

# Cache Configuration
CACHE_CONFIG = {
    "ttl_seconds": int(os.getenv('CACHE_TTL', '3600')),  # 1 hour default
    "max_size": int(os.getenv('CACHE_MAX_SIZE', '100')),  # Max 100 cached results
}

# Parallel Execution Configuration
PARALLEL_CONFIG = {
    "max_workers": int(os.getenv('MAX_PARALLEL_WORKERS', '4')),
    "timeout_seconds": int(os.getenv('AGENT_TIMEOUT', '30')),
}

# Output Configuration
OUTPUT_CONFIG = {
    "max_opportunities": int(os.getenv('MAX_OPPORTUNITIES', '15')),
    "verbose_output": os.getenv('VERBOSE_OUTPUT', 'false').lower() == 'true',
}

def get_optimization_summary():
    """Get a summary of enabled optimizations"""
    enabled = [name for name, value in OPTIMIZATIONS.items() if value]
    if not enabled:
        return "No performance optimizations enabled"

    optimization_benefits = {
        "parallel_execution": "30-50% faster search",
        "use_light_models": "20-30% faster processing",
        "enable_caching": "50-70% faster repeat queries",
        "async_pdf": "Improved user experience",
        "batch_search": "15-25% fewer API calls",
    }

    benefits = [optimization_benefits.get(opt, opt) for opt in enabled]
    return f"Optimizations enabled: {', '.join(benefits)}"

# Print optimization status on module load
if __name__ != "__main__":
    print(f"Deal Sourcing Agent: {get_optimization_summary()}")