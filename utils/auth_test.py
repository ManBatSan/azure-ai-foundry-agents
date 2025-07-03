import os

from azure.ai.projects import AIProjectClient
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main():
    load_dotenv(override=True)
    endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
    subscription_id = os.getenv("SUBSCRIPTON_ID")
    resource_group_name = os.getenv("RESOURCE_GROUP_NAME")
    project_name = os.getenv("PROJECT_NAME")

    if not all([endpoint, subscription_id, resource_group_name, project_name]):
        raise EnvironmentError(
            "Please ensure AI_FOUNDRY_ENDPOINT, SUBSCRIPTON_ID, "
            "RESOURCE_GROUP_NAME, and PROJECT_NAME are set in your .env file."
        )

    try:
        client = AIProjectClient(
            endpoint=endpoint,
            subscription_id=subscription_id,
            resource_group_name=resource_group_name,
            project_name=project_name,
            credential=DefaultAzureCredential(),
        )
        print("✅ Authentication successful!")
    except AzureError as e:
        print(f"❌ Authentication failed: {e}")
        return

    try:
        agent = client.agents.create_agent(
            model="gpt-4o-mini",
            name="my-agent",
            instructions="You are helpful agent",
        )
        print(f"Created agent, agent ID: {agent.id}")

        # Do something with your Agent!
        # See samples here https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-projects_1.0.0b12/sdk/ai/azure-ai-agents/samples

        client.agents.delete_agent(agent.id)
        print("Deleted agent")
    except AzureError as e:
        print(f"❌ API call failed: {e}")


if __name__ == "__main__":
    main()
