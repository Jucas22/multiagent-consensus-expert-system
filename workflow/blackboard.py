from typing import List, Dict


class Blackboard:
    """
    Pizarra compartida que almacena el estado del debate y permite la comunicación entre agentes.
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.opinions: Dict[str, str] = {}  # agent_role -> opinion (markdown)
        self.conversation_history: List[Dict[str, str]] = (
            []
        )  # list of {role: ..., content: ...}
        self.consensus_status: str = "PENDING"

    def add_opinion(self, role_name: str, opinion: str):
        self.opinions[role_name] = opinion
        self.conversation_history.append(
            {"role": role_name, "content": opinion, "type": "OPINION_INITIAL"}
        )

    def get_context_for_agent(self, role_name: str) -> str:
        """Genera el contexto actual visible para un agente."""
        context = f"TEMA DE DEBATE: {self.topic}\n\n"

        # Añadir opiniones de otros si existen (para fases posteriores)
        if self.opinions:
            context += "OPINIONES ACTUALES DE OTROS EXPERTOS:\n"
            for r, text in self.opinions.items():
                if r != role_name:
                    context += (
                        f"--- OPINIÓN DE {r} ---\n{text}\n-----------------------\n"
                    )

        return context

    def __str__(self):
        return f"Blackboard(Topic: {self.topic}, Opinions: {len(self.opinions)})"
