"""GCP Helper Agent - Get GCP credentials and project info"""
from typing import Dict, Any, Optional, List
import os

SYSTEM_PROMPT = """You are a GCP infrastructure helper agent.

Your job is to help users get GCP information:
- List GCP projects
- Get service account keys
- Get project ID and region
- Check Cloud Run status
- Get container registry images

You have tools:
- gcloud CLI (pre-authenticated)
- curl to GCP APIs
- gsutil for storage

When asked for credentials:
- Never expose raw secrets
- Guide user to GCP console
- Provide steps to create SA keys
- Show where to add secrets in GitHub

Always:
- Stay calm and helpful
- Ask clarifying questions
- Provide step-by-step guidance
- Point to GCP console URLs

GCP Console: https://console.cloud.google.com
IAM & Admin: https://console.cloud.google.com/iam-admin
Service Accounts: https://console.cloud.google.com/iam-admin/serviceaccounts
Container Registry: https://console.cloud.google.com/gcr

When user is frustrated:
- Acknowledge the frustration
- Don't argue
- Help them get unstuck
"""


class GCPHelperAgent:
    """Helper agent for GCP operations"""
    
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT
    
    async def chat(self, message: str) -> Dict[str, Any]:
        """Process user request"""
        message = message.lower()
        
        if "project" in message:
            return await self.get_projects()
        elif "service account" in message or "credentials" in message:
            return await self.get_sa_guide()
        elif "cloud run" in message:
            return await self.get_cloud_run_status()
        elif "region" in message:
            return await self.get_region()
        else:
            return {"response": "I can help with:\n- GCP projects list\n- Service account setup\n- Cloud Run status\n- Region info\n\nWhat do you need?", "actions": ["list_projects", "get_sa_guide", "get_cloud_run", "get_region"]}
    
    async def get_projects(self) -> Dict[str, Any]:
        """List GCP projects"""
        result = os.popen("gcloud projects list --format=value(projectId) 2>/dev/null").read()
        projects = [p.strip() for p in result.split('\n') if p.strip()]
        return {
            "response": f"Available projects:\n" + "\n".join(f"- {p}" for p in projects) if projects else "No projects found. Set up GCP first.",
            "projects": projects,
            "console": "https://console.cloud.google.com/projectselector2"
        }
    
    async def get_sa_guide(self) -> Dict[str, Any]:
        """Get service account setup guide"""
        return {
            "response": """To create GCP Service Account key:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Select your project
3. Click + CREATE SERVICE ACCOUNT
4. Name: github-actions
5. Role: Owner (or Cloud Run Admin)
6. Create key: Actions → Create key → JSON
7. Save the JSON file

Then add to GitHub:
- Repo Settings → Secrets → COOLIFY_TOKEN
- Add the JSON content or use gh CLI""",
            "steps": [
                "Go to GCP Console → IAM → Service Accounts",
                "Create SA with Owner/Cloud Run Admin role",
                "Create JSON key",
                "Add to GitHub secrets"
            ],
            "console_url": "https://console.cloud.google.com/iam-admin/serviceaccounts"
        }
    
    async def get_cloud_run_status(self) -> Dict[str, Any]:
        """Check Cloud Run status"""
        result = os.popen("gcloud run services list --format=value(NAME,STATUS,URL) 2>/dev/null").read()
        services = [s.strip() for s in result.split('\n') if s.strip()]
        return {
            "response": f"Cloud Run services:\n" + "\n".join(s for s in services) if services else "No Cloud Run services found",
            "console": "https://console.cloud.google.com/run"
        }
    
    async def get_region(self) -> Dict[str, Any]:
        """Get default region"""
        result = os.popen("gcloud config get-value region 2>/dev/null").read().strip()
        return {
            "response": f"Default region: {result or 'us-central1'}",
            "region": result or "us-central1",
            "console": "https://console.cloud.google.com/run"
        }


def get_gcp_agent() -> GCPHelperAgent:
    return GCPHelperAgent()


__all__ = ["GCPHelperAgent", "get_gcp_agent"]