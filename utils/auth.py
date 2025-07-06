import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv(override=True)


def get_client() -> AIProjectClient:
    """
    Authenticate and return an Azure AI Foundry project client.
    """

    endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
    subscription_id = os.getenv("SUBSCRIPTON_ID")
    resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
    project_name = os.getenv("PROJECT_NAME")

    if not all([endpoint, subscription_id, resource_group_name, project_name]):
        raise EnvironmentError(
            "Please ensure AI_FOUNDRY_ENDPOINT, SUBSCRIPTON_ID, RESOURCE_GROUP_NAME, "
            "and PROJECT_NAME are set in your .env file."
        )

    # Instantiate Foundry client
    client = AIProjectClient(
        endpoint=endpoint,
        subscription_id=subscription_id,
        resource_group_name=resource_group_name,
        project_name=project_name,
        credential=DefaultAzureCredential(),
    )
    return client
