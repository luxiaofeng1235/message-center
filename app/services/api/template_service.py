class TemplateService:
    """消息模板服务。"""

    async def render(self, template_key: str, variables: dict | None = None) -> dict:
        # TODO: render content and payload using template
        return {"template_key": template_key, "variables": variables or {}}
