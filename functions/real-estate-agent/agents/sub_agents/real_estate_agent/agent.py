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

"""real_estate_agent for finding real estate investment opportunities"""

from google.adk import Agent
from google.adk.tools import google_search

from . import prompt
from config import MODELS

MODEL = MODELS["simple"]  # Automatically uses lighter model if optimization enabled

real_estate_agent = Agent(
    model=MODEL,
    name="real_estate_agent",
    instruction=prompt.REAL_ESTATE_AGENT_PROMPT,
    output_key="real_estate_opportunities_output",
    tools=[google_search],
)
