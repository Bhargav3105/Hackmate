from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

# Connect to Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def clean_json(text):
    """
    Cleans AI response and extracts valid JSON
    even if the model adds extra text around it
    """
    # Remove markdown code blocks if present
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()

    # Find JSON object in the response
    start = text.find('{')
    end = text.rfind('}') + 1

    if start != -1 and end != 0:
        text = text[start:end]

    return text


def calculate_compatibility(user_profile, candidate_profile):
    """
    Takes two user profiles and returns:
    - A compatibility score (0-100)
    - A clear explanation of why they match
    - Specific strengths of the match
    """

    prompt = f"""
    You are an expert hackathon team formation AI.

    Analyze these two developer profiles and calculate their
    compatibility as hackathon teammates.

    PROFILE 1 (Current User):
    - Name: {user_profile.get('full_name', 'User')}
    - Skills: {', '.join(user_profile.get('skills', []))}
    - Experience: {user_profile.get('experience_level', 'Intermediate')}
    - Availability: {user_profile.get('availability', '3-5 hrs')}
    - Goals: {', '.join(user_profile.get('goals', []))}

    PROFILE 2 (Potential Teammate):
    - Name: {candidate_profile.get('full_name', 'Candidate')}
    - Skills: {', '.join(candidate_profile.get('skills', []))}
    - Experience: {candidate_profile.get('experience_level', 'Intermediate')}
    - Availability: {candidate_profile.get('availability', '3-5 hrs')}
    - Goals: {', '.join(candidate_profile.get('goals', []))}

    Return ONLY a JSON object with this exact structure, no other text:
    {{
        "score": 85,
        "summary": "one sentence explaining the match",
        "strengths": [
            "strength 1",
            "strength 2",
            "strength 3"
        ],
        "potential_challenges": "one sentence about challenges",
        "recommended_roles": {{
            "user": "suggested role for profile 1",
            "candidate": "suggested role for profile 2"
        }}
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a hackathon team formation expert. "
                           "You must respond with valid JSON only. "
                           "No explanations, no markdown, just JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    raw = response.choices[0].message.content
    cleaned = clean_json(raw)
    result = json.loads(cleaned)
    return result


def generate_project_ideas(skills, experience, goals, team_size=2):
    """
    Takes team skills and returns 3 buildathon project ideas
    with features, timeline and MVP roadmap
    """

    prompt = f"""
    You are an expert hackathon mentor and product strategist.

    Generate 3 innovative buildathon project ideas for this team:
    - Combined Skills: {', '.join(skills)}
    - Experience Level: {experience}
    - Goals: {', '.join(goals)}
    - Team Size: {team_size} people

    Focus on the Sarvam AI track: Developer Tools and Software Infrastructure.

    Return ONLY a JSON object with this exact structure, no other text:
    {{
        "ideas": [
            {{
                "title": "Project Name",
                "tagline": "one line description",
                "problem": "what problem does this solve",
                "solution": "how it solves the problem",
                "key_features": [
                    "feature 1",
                    "feature 2",
                    "feature 3",
                    "feature 4"
                ],
                "tech_stack": ["tech 1", "tech 2", "tech 3"],
                "mvp_timeline": {{
                    "day_1": "what to build on day 1",
                    "day_2": "what to build on day 2",
                    "day_3": "what to build on day 3"
                }},
                "wow_factor": "what makes this stand out to judges",
                "difficulty": "Medium"
            }}
        ]
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a hackathon mentor and product strategist. "
                           "You must respond with valid JSON only. "
                           "No explanations, no markdown, just JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )

    raw = response.choices[0].message.content
    cleaned = clean_json(raw)
    result = json.loads(cleaned)
    return result


def get_ai_recommendations(user_profile):
    """
    Returns personalized recommendations for the user
    based on their profile
    """

    prompt = f"""
    You are a hackathon coach giving personalized advice.

    Based on this developer profile:
    - Skills: {', '.join(user_profile.get('skills', []))}
    - Experience: {user_profile.get('experience_level', 'Intermediate')}
    - Availability: {user_profile.get('availability', '3-5 hrs')}
    - Goals: {', '.join(user_profile.get('goals', []))}

    Return ONLY a JSON object with this exact structure, no other text:
    {{
        "missing_skills": [
            "skill they should look for in teammates"
        ],
        "ideal_team_size": 3,
        "recommended_role": "their ideal role in the team",
        "tips": [
            "tip 1 for hackathon success",
            "tip 2",
            "tip 3"
        ]
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a hackathon coach. "
                           "You must respond with valid JSON only. "
                           "No explanations, no markdown, just JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=400
    )

    raw = response.choices[0].message.content
    cleaned = clean_json(raw)
    result = json.loads(cleaned)
    return result

def assign_team_roles(team_members, project_idea=""):
    """
    Analyzes team members' skills and assigns
    the best role for each person.
    team_members = list of dicts with
    name and skills
    """

    members_text = "\n".join([
        f"- {m['name']}: {', '.join(m.get('skills', []))}"
        for m in team_members
    ])

    prompt = f"""
    You are an expert hackathon team organizer.

    Analyze this team and assign the best role
    for each member based on their skills.

    Team members and their skills:
    {members_text}

    Project context: {project_idea if project_idea
    else 'General hackathon project'}

    Return ONLY a JSON object:
    {{
        "roles": [
            {{
                "name": "member name",
                "role": "specific role title",
                "responsibilities": [
                    "key responsibility 1",
                    "key responsibility 2",
                    "key responsibility 3"
                ],
                "why": "one sentence explaining why
                this role suits them"
            }}
        ],
        "team_summary": "one sentence about
        the team's overall strength"
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a hackathon team "
                           "organizer. Return valid "
                           "JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    raw = response.choices[0].message.content
    cleaned = clean_json(raw)
    result = json.loads(cleaned)
    return result