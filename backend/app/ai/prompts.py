"""AI prompts for plan generation."""

PLAN_GENERATION_PROMPT = """You are a Windows storage optimization expert. Analyze the following drive usage data and generate 3 cleanup plans.

Drive Analysis:
{drive_data}

Top Space Consumers:
{consumers_data}

User Settings:
- Primary target drive: {target_drive}
- Backup location: {backup_location}

Generate 3 plans with the following IDs:
1. "conservative" - Conservative (low risk, basic cleanup)
2. "balanced" - Balanced (medium risk, recommended)
3. "aggressive" - Aggressive (high risk, maximum savings)

For each plan, provide:
- Specific actions (MOVE, DELETE_TO_RECYCLE, CLEANUP, PRUNE, EXPORT_IMPORT_WSL)
- Space savings estimate
- Risk assessment
- Detailed rationale
- Safety explanations

Return ONLY valid JSON matching this schema:
[
  {{
    "id": "conservative",
    "name": "Conservative",
    "space_saved_bytes": 45200000000,
    "risk_level": "low",
    "estimated_minutes": 15,
    "rationale": "Clean temporary files and caches only...",
    "recommended": false,
    "actions": [
      {{
        "id": "action_1",
        "type": "CLEANUP",
        "description": "Clear Browser Caches",
        "size_bytes": 8900000000,
        "safety_explanation": "Browsers will rebuild cache automatically",
        "rollback_option": "Not needed (cache data)",
        "estimated_seconds": 120
      }}
    ]
  }}
]

Important:
- Use actual byte values from the provided data
- Be specific with paths when suggesting MOVE operations
- Conservative plan should only clean caches and temp files
- Balanced plan can move Docker/WSL and clean more aggressively
- Aggressive plan can relocate user folders and do extensive cleanup
- Mark "balanced" plan as recommended: true
"""
