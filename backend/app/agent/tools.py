import json
from app.database import SessionLocal
from app import models
from datetime import date
from langchain.tools import tool
from app.agent.llm import llm


def safe_json_loads(content: str, fallback: dict):
    try:
        content = content.strip()

        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        return json.loads(content)
    except Exception:
        return fallback


@tool
def log_interaction_tool(text: str):
    """Extract structured CRM interaction data from raw HCP interaction text."""

    fallback = {
        "hcp_name": "",
        "interaction_type": "",
        "interaction_date": str(date.today()),
        "topics_discussed": "",
        "materials_shared": "",
        "samples_distributed": "",
        "sentiment": "",
        "outcome": "",
        "follow_up_action": "",
        "summary": text,
    }

    prompt = f"""
You are an AI assistant for a life-science CRM used by medical sales representatives.

Extract structured interaction data.

Return ONLY valid JSON with these keys:
{json.dumps(fallback, indent=2)}

Rules:
- If date is not mentioned, use today's date: {date.today()}.
- If user says "met", use interaction_type: "In-person Meeting".
- Sentiment must be Positive, Neutral, Negative, or empty string.
- Do not invent facts.

Interaction note:
{text}
"""

    response = llm.invoke(prompt)
    return safe_json_loads(response.content, fallback)


@tool
def edit_interaction_tool(text: str):
    """Edit an existing CRM interaction using interaction ID and requested field updates."""

    fallback = {
        "interaction_id": None,
        "updates": {},
        "status": "failed",
        "message": "Could not parse edit request."
    }

    prompt = f"""
You are editing an existing CRM interaction.

Extract the interaction ID and only the fields the user wants to update.

Return ONLY valid JSON:
{{
  "interaction_id": null,
  "updates": {{}}
}}

Allowed update fields:
- hcp_name
- interaction_type
- interaction_date
- topics_discussed
- materials_shared
- samples_distributed
- sentiment
- outcome
- follow_up_action
- summary

Rules:
- Only include fields explicitly requested by the user.
- Do not include empty fields.
- If no interaction ID is mentioned, interaction_id must be null.
- Convert sentiment values to Positive, Neutral, or Negative.

User request:
{text}
"""

    response = llm.invoke(prompt)
    parsed = safe_json_loads(response.content, fallback)

    interaction_id = parsed.get("interaction_id")
    updates = parsed.get("updates", {})

    if not interaction_id:
        return {
            "status": "failed",
            "message": "Please provide an interaction ID to edit.",
            "interaction_id": None,
            "updates": updates
        }

    if not updates:
        return {
            "status": "failed",
            "message": "No update fields were found.",
            "interaction_id": interaction_id,
            "updates": {}
        }

    allowed_fields = {
        "hcp_name",
        "interaction_type",
        "interaction_date",
        "topics_discussed",
        "materials_shared",
        "samples_distributed",
        "sentiment",
        "outcome",
        "follow_up_action",
        "summary",
    }

    clean_updates = {
        key: value
        for key, value in updates.items()
        if key in allowed_fields and value not in [None, ""]
    }

    db = SessionLocal()

    try:
        interaction = db.query(models.Interaction).filter(
            models.Interaction.id == interaction_id
        ).first()

        if not interaction:
            return {
                "status": "failed",
                "message": f"Interaction {interaction_id} not found.",
                "interaction_id": interaction_id,
                "updates": clean_updates
            }

        for key, value in clean_updates.items():
            setattr(interaction, key, value)

        db.commit()
        db.refresh(interaction)

        return {
            "status": "success",
            "message": f"Interaction {interaction_id} updated successfully.",
            "interaction_id": interaction_id,
            "updates": clean_updates,
            "updated_interaction": {
                "id": interaction.id,
                "hcp_name": interaction.hcp_name,
                "interaction_type": interaction.interaction_type,
                "interaction_date": interaction.interaction_date,
                "topics_discussed": interaction.topics_discussed,
                "materials_shared": interaction.materials_shared,
                "samples_distributed": interaction.samples_distributed,
                "sentiment": interaction.sentiment,
                "outcome": interaction.outcome,
                "follow_up_action": interaction.follow_up_action,
                "summary": interaction.summary,
            }
        }

    finally:
        db.close()

        
@tool
def suggest_follow_up_tool(text: str):
    """Suggest a next best follow-up action for the HCP interaction."""

    prompt = f"""
You are a life-science CRM assistant.

Suggest one practical follow-up action based on this interaction.
Return ONLY valid JSON:
{{
  "follow_up_action": "",
  "reason": ""
}}

Interaction:
{text}
"""
    response = llm.invoke(prompt)
    return safe_json_loads(response.content, {
        "follow_up_action": "Schedule a follow-up discussion.",
        "reason": "General follow-up recommended."
    })


@tool
def hcp_lookup_tool(text: str):
    """Extract HCP lookup request information."""

    prompt = f"""
Extract the HCP name from this request.

Return ONLY valid JSON:
{{
  "hcp_name": "",
  "lookup_intent": ""
}}

Request:
{text}
"""
    response = llm.invoke(prompt)
    return safe_json_loads(response.content, {
        "hcp_name": "",
        "lookup_intent": "HCP profile lookup"
    })


@tool
def material_recommendation_tool(text: str):
    """Recommend sales or medical materials based on interaction context."""

    prompt = f"""
You are a CRM assistant for pharma field representatives.

Recommend relevant materials based on the interaction.

Return ONLY valid JSON:
{{
  "recommended_materials": [],
  "reason": ""
}}

Interaction:
{text}
"""
    response = llm.invoke(prompt)
    return safe_json_loads(response.content, {
        "recommended_materials": [],
        "reason": ""
    })