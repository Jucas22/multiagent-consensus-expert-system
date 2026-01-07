import vertexai

# Tus importaciones específicas
from google.adk.agents import Agent
from vertexai.agent_engines import AdkApp

# CONFIGURACIÓN
PROJECT_ID = "project-99da2f28-3eb5-4ad1-8f2"  # Reemplaza con tu ID real de GCP
LOCATION = "us-central1"  # O la región que estés usando (ej. europe-west1)


def main():
    print(f"🔄 Inicializando Vertex AI en el proyecto: {PROJECT_ID}...")

    # 1. Inicializar el SDK de Vertex AI
    # Esto usará automáticamente las credenciales de 'gcloud auth application-default login'
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print("✅ Vertex AI inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error al inicializar Vertex AI: {e}")
        return

    # 2. Instanciar y probar el Agente
    # NOTA: La forma exacta de instanciar 'AdkApp' depende de tu librería específica.
    # Aquí pongo un ejemplo genérico de cómo suelen funcionar:
    try:
        print("🤖 Creando instancia de AdkApp...")

        agent = Agent(
            name="test", model="gemini-2.0-flash", instruction="Eres un asistente útil."
        )

        print("✅ Agente instanciado. Listo para pruebas.")

        response = agent.run_live(
            "Hola, ¿puedes escucharme? Realizando test de conexión."
        )
        print(f"Respuesta del agente: {response}")

    except Exception as e:
        print(f"❌ Error al crear el Agente: {e}")
        print("Verifica que tengas los permisos 'Vertex AI User' en tu cuenta.")


if __name__ == "__main__":
    main()
