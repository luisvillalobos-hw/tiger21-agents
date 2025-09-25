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

"""Agent entry point for deal_sourcing - imports from main agent file"""

import sys
import os

# Add parent directory to path to import from root level
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def __getattr__(name):
    if name == 'root_agent':
        import deal_sourcing_agent
        return deal_sourcing_agent.root_agent
    elif name == 'deal_sourcing_coordinator':
        import deal_sourcing_agent
        return deal_sourcing_agent.deal_sourcing_coordinator
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ["root_agent", "deal_sourcing_coordinator"]