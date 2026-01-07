import asyncio
import os

from google.adk.agents import LlmAgent
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.cloud import storage

# Ahora esto funcionará automáticamente sin rutas ni JSON
client = storage.Client()
print("¡Conectado exitosamente usando Application Default Credentials!")

# Asegúrate de tener tu API Key configurada
api_key = os.getenv("GOOGLE_API_KEY")  #
api_base = os.getenv("ADK_API_BASE") or None
model = os.getenv("ADK_MODEL") or None

# 1. Definir el agente
model = "gemini-2.0-flash"
agent = Agent(
    name="TestAgent",
    model=model,  # O el modelo que tengas disponible (ej. gemini-2.0-flash)
    instruction="Eres un asistente útil. Responde de forma concisa para confirmar que el test funciona.",
)
app = AdkApp(agent=agent)


async def main():
    print("--- Iniciando Test del Agente ---")

    # 2. Configurar servicios en memoria
    # InMemorySessionService es ideal para pruebas locales ya que no requiere base de datos
    session_service = InMemorySessionService()

    runner = Runner(
        agent=agent, app_name="test_app_rapido", session_service=session_service
    )

    # 3. Crear una sesión temporal
    user_id = "usuario_prueba"
    session = await session_service.create_session(
        app_name="test_app_rapido", user_id=user_id
    )

    # 4. Preparar el mensaje del usuario
    # El ADK usa tipos específicos de google.genai para el contenido
    user_msg = types.Content(
        role="user",
        parts=[
            types.Part(text="Hola, ¿puedes escucharme? Realizando test de conexión.")
        ],
    )

    print(f"Enviando mensaje: '{user_msg.parts[0].text}'")

    # 5. Ejecutar el agente y escuchar la respuesta
    # Usamos run_async para procesar el flujo de eventos
    async for event in runner.run_async(
        user_id=user_id, session_id=session.id, new_message=user_msg
    ):
        # El runner emite varios eventos (pensamiento, llamadas a herramientas, etc.)
        # Aquí solo nos interesa la respuesta final al usuario
        if event.is_final_response():
            respuesta = event.content.parts[0].text
            print(f"\nRespuesta del Agente: {respuesta}")

    print("\n--- Test Finalizado ---")


if __name__ == "__main__":
    asyncio.run(main())
