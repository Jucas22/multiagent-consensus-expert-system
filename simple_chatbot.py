import asyncio
import vertexai
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

# CONFIGURACIÓN
PROJECT_ID = "project-99da2f28-3eb5-4ad1-8f2"
LOCATION = "us-central1"


async def main():
    print(f"🔄 Inicializando Vertex AI en el proyecto: {PROJECT_ID}...")

    # 1. Inicializar Vertex AI
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print("✅ Vertex AI inicializado.")
    except Exception as e:
        print(f"❌ Error al inicializar Vertex AI: {e}")
        return

    # 2. Instanciar el Agente
    try:
        print("🤖 Iniciando Chatbot...")
        agent = Agent(
            name="chatbotbasico",
            model="gemini-2.0-flash",
            instruction="Eres un asistente útil, amable y conciso.",
            output_key="respuesta",
        )

        app = AdkApp(agent=agent)
        print("✅ Agente listo.\n")
        print("=========================================")
        print(" Escribe tu mensaje y presiona Enter.")
        print(" Para salir, escribe 'salir' o presiona Ctrl+C")
        print("=========================================\n")

        # Bucle principal del chat
        while True:
            try:
                # Usamos asyncio.to_thread para que input() no bloquee completamente el loop de eventos
                # aunque en este caso simple secuencial no es crítico, es buena práctica.
                text = await asyncio.to_thread(input, "👤 Tú: ")
                print(text)

                if text.lower().strip() in ["salir", "exit", "quit"]:
                    print("👋 Cerrando el chat. ¡Hasta luego!")
                    break

                if not text.strip():
                    continue

                print("🤖 Agente: ", end="", flush=True)

                # El objeto devuelto por run_live es un async_generator, así que debemos iterarlo asíncronamente
                async for event in agent.run_async(
                    user_id="user123",
                    message=f"{text}",
                ):
                    print(event)
                    print(event.keys)
                    print(event.actions.state_delta.respuesta)
                # response = agent.run_async(parent_context=None, inputs=text)

                # async for chunk in response:
                #     # A veces el chunk es un objeto, a veces es texto.
                #     # Convertimos a string por seguridad para imprimirlo.
                #     texto_chunk = str(chunk)

                #     print(texto_chunk, end="", flush=True)
                #     full_text += texto_chunk

                print()  # Salto de línea al final de la respuesta

            except KeyboardInterrupt:
                print("\n👋 Interrupción detectada. Saliendo...")
                break
            except Exception as e:
                print(f"\n❌ Error en el turno del chat: {e}")

    except Exception as e:
        print(f"❌ Error fatal al crear el Agente: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
