import asyncio
import os

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.function_tool import FunctionTool
from google.genai.types import Content, Part

from basic_calculator.tools.math_tools import basic_calculator
from basic_calculator.config import settings


os.environ["GOOGLE__GENAI_USE_VERTEXAI"] = settings.google.genai_use_vertexai
os.environ["GOOGLE_API_KEY"] = settings.google.api_key.get_secret_value() if hasattr(settings.google.api_key, "get_secret_value") else settings.google.api_key

APP_NAME = "ToolEnabledApp"

calc_tool = FunctionTool(basic_calculator)

root_agent = LlmAgent(
    name="MathAssistant",
    model=settings.google.model,
    instruction=(
        "You are a precise mathematical assistant. "
        "You must use the 'basic_calculator' tool for ANY calculation. "
        "Do not calculate in your head. "
        "If the tool returns an error, report it to the user."
        ),
    tools=[calc_tool]
)

async def main() -> None:
    session_services = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_services
    )

    user_id = "math_user_01"
    session_id = "math_session"

    await session_services.create_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )

    query = "Multiply 15.5 by 4 and then tell me the result."
    print(f"USER: {query}")

    message = Content(parts=[Part(text=query)])

    print(f"AGENT: ", end="", flush=True)

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call:
                    print(f"\n[SYSTEM: Tool call Detected: {part.function_call.name}]\n", end="")
                if part.text:
                    print(part.text, end="", flush=True)
    print("\n")


if __name__=="__main__":
    asyncio.run(main=main())
