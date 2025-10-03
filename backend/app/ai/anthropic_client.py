"""Anthropic Claude API integration for plan generation."""

import json
from typing import List, Dict, Any
from anthropic import AsyncAnthropic
from app.ai.prompts import PLAN_GENERATION_PROMPT


class AnthropicClient:
    """Anthropic Claude API client for generating cleanup plans."""

    def __init__(self, api_key: str):
        """Initialize Anthropic client."""
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-sonnet-20240229"
        self.max_tokens = 4000

    async def generate_plans(
        self,
        drive_data: Dict[str, Any],
        consumers_data: List[Dict[str, Any]],
        target_drive: str,
        backup_location: str
    ) -> List[Dict[str, Any]]:
        """Generate cleanup plans using Anthropic Claude."""
        try:
            # Format data for prompt
            drives_str = json.dumps(drive_data, indent=2)
            consumers_str = json.dumps(consumers_data, indent=2)

            prompt = PLAN_GENERATION_PROMPT.format(
                drive_data=drives_str,
                consumers_data=consumers_str,
                target_drive=target_drive,
                backup_location=backup_location
            )

            # Call Anthropic API
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse response
            content = response.content[0].text
            plans = json.loads(content)

            return plans

        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None
