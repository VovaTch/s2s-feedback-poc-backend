def create_message_openai(role: str, message: str) -> dict[str, str]:
    if role not in ["system", "user", "assistant"]:
        raise KeyError(
            f"Role must be one of 'system', 'user', or 'assistant'. Got {role} instead."
        )
    return {"role": role, "content": message}
