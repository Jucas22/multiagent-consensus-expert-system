class BaseExpertAgent:
    def __init__(self, role_name: str, system_prompt: str, tools: list | None = None):
        self.role_name = role_name
        self.system_prompt = system_prompt
        # aquí inicializarías el agente ADK con ese prompt y tools

    def initial_opinion(self, topic: str) -> str:
        """Primera postura independiente sobre el tema."""
        # llamada al modelo ADK con el prompt adecuado
        ...

    def revise_opinion(self, topic: str, summary_other_opinions: str) -> str:
        """Revisión de la postura tras ver el resumen del resto."""
        ...