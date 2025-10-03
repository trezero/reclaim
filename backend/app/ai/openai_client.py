"""OpenAI API integration for plan generation."""

import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.ai.prompts import PLAN_GENERATION_PROMPT


class OpenAIClient:
    """OpenAI API client for generating cleanup plans."""

    def __init__(self, api_key: str):
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
        self.temperature = 0.7
        self.max_tokens = 2000

    async def generate_plans(
        self,
        drive_data: Dict[str, Any],
        consumers_data: List[Dict[str, Any]],
        target_drive: str,
        backup_location: str
    ) -> List[Dict[str, Any]]:
        """Generate cleanup plans using OpenAI."""
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

            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Windows storage optimization expert. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Parse response
            content = response.choices[0].message.content
            plans = json.loads(content)

            return plans

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
