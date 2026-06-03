"""
LLM provider abstraction.

Returns a LangChain chat model based on LLM_PROVIDER env var.
Swap the provider in .env — no code changes needed.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings


def get_chat_model() -> BaseChatModel:
    """
    Return a configured LangChain chat model.

    Supported providers:
    - "openai"    → ChatOpenAI  (default)
    - "anthropic" → ChatAnthropic
    - "gemini"    → ChatGoogleGenerativeAI
    """
    if settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.anthropic_model,
            api_key=settings.anthropic_api_key or None,  # type: ignore[arg-type]
        )

    if settings.llm_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.gemini_api_key or None,  # type: ignore[arg-type]
        )

    # Default: OpenAI
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key or None,  # type: ignore[arg-type]
    )
