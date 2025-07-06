import asyncio
import os

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.contents import ChatHistory
from semantic_kernel.contents.chat_message_content import AuthorRole
from semantic_kernel.contents.function_call_content import FunctionCallContent
from semantic_kernel.contents.function_result_content import FunctionResultContent

from agents.foundry_agents_plugin import FoundryAgentsPlugin


async def main():
    kernel = Kernel()
    kernel.add_service(
        service=AzureChatCompletion(
            service_id="main_chat",
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
    )

    kernel.add_plugin(FoundryAgentsPlugin(), plugin_name="FoundryAgents")

    settings = AzureChatPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    history = ChatHistory()
    user_goal = "Write an in-depth article on the environmental impact of electric vehicles."
    history.add_user_message(user_goal)

    chat_service = kernel.get_service(service_id="main_chat", type=AzureChatCompletion)
    result = await chat_service.get_chat_message_content(
        chat_history=history, settings=settings, kernel=kernel
    )

    history.add_message(result)

    print("📰 Final article:\n")
    print(result, end="\n\n")

    print("🔍 Full function-calling trace:\n")
    for idx, msg in enumerate(history.messages):
        prefix = f"[{idx:02d}]"

        if msg.role == AuthorRole.USER:
            print(f"{prefix} 🟢 User: {msg.content}")

        for item in msg.items or []:
            if isinstance(item, FunctionCallContent):
                print(f"{prefix} → Function call: {item.function_name}({item.arguments})")
            elif isinstance(item, FunctionResultContent):
                raw = item.result
                if isinstance(raw, list) and raw and isinstance(raw[0], dict) and "text" in raw[0]:
                    text = raw[0]["text"]["value"]
                else:
                    text = raw
                print(f"{prefix} ← Function result: {text}")

        has_tool = any(
            isinstance(it, (FunctionCallContent, FunctionResultContent)) for it in msg.items or []
        )
        if msg.role == AuthorRole.ASSISTANT and not has_tool:
            content = msg.content.strip().replace("\n", " ")
            print(f"{prefix} 🟣 Assistant: {content}")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())
