from google.adk.agents import Agent

from docs.constants import (
    GLOBAL_GUARDRAILS,
    TEMPLATE_INSTRUCCIONES,
    LLM_MODEL,
)


class BaseExpertAgent:
    """Base de todos los expertos y punto único de llamada al LLM."""

    def __init__(
        self,
        role_name: str,
        role_description: str,
        output_key: str = "text",
        blackboard=None,
    ) -> None:
        self.role_name = role_name
        self.blackboard = blackboard
        self.output_key = output_key

        # Construimos el prompt completo incluyendo el rol
        system_prompt = f"{GLOBAL_GUARDRAILS}\n\n" f"{TEMPLATE_INSTRUCCIONES}"

        self.agent = Agent(
            name=self.role_name,
            model=LLM_MODEL,
            instruction=role_description,
            global_instruction=system_prompt,
            output_key=output_key,
        )

    async def get_response(self, message: str) -> str | None:
        """Consulta el LLM y concatena los deltas del estado para la clave configurada."""
        try:
            fragments: list[str] = []
            async for event in self.agent.run_async(
                user_id="user123",
                message=message,
            ):
                actions = getattr(event, "actions", None)
                state_delta = getattr(actions, "state_delta", None)
                if state_delta is None:
                    continue

                delta_value = getattr(state_delta, self.output_key, None)
                if delta_value:
                    fragments.append(str(delta_value))

            full_response = "".join(fragments).strip()
            return full_response or None
        except Exception as e:
            print(f"Error obteniendo respuesta del agente {self.role_name}: {e}")
            return None
