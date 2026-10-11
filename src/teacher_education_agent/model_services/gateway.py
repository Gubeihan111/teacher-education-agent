"""DeepSeek/Qwen routing migrated from the previous agent."""
import json
from teacher_education_agent.core.config import Settings
from .contracts import ModelRequest, ModelResponse

class ModelGateway:
    def __init__(self, settings: Settings): self.settings = settings
    def select_provider(self, task_type: str) -> str:
        return "deepseek" if task_type in {"reasoning", "conflict", "evidence", "judgment"} else "qwen"
    async def complete(self, request: ModelRequest) -> ModelResponse:
        provider = self.select_provider(request.task_type)
        key = self.settings.deepseek_api_key if provider == "deepseek" else self.settings.dashscope_api_key
        base = self.settings.deepseek_base_url if provider == "deepseek" else self.settings.dashscope_base_url
        model = self.settings.deepseek_model if provider == "deepseek" else self.settings.qwen_model
        if not key: raise RuntimeError(f"{provider}_not_configured")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=key, base_url=base, timeout=self.settings.model_timeout_seconds, max_retries=self.settings.model_max_retries)
        options = {"model": model, "messages": list(request.messages), "temperature": request.temperature}
        if request.require_json: options["response_format"] = {"type": "json_object"}
        response = await client.chat.completions.create(**options)
        content = response.choices[0].message.content or ""
        return ModelResponse(provider, model, content, json.loads(content) if request.require_json else None)
    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.settings.dashscope_api_key: raise RuntimeError("qwen_not_configured")
        from openai import AsyncOpenAI
        client=AsyncOpenAI(api_key=self.settings.dashscope_api_key,base_url=self.settings.dashscope_base_url,timeout=self.settings.model_timeout_seconds)
        response=await client.embeddings.create(model=self.settings.embedding_model,input=texts,dimensions=self.settings.vector_dimension)
        return [item.embedding for item in response.data]
