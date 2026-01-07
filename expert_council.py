import asyncio
import sys
from pathlib import Path

# Añadimos la raíz del proyecto al path para asegurar importaciones correctas
sys.path.append(str(Path(__file__).parent))

from docs.constants import CONSENSE_THEME
from workflow.blackboard import Blackboard

# Importar agentes
from agents.ethic_expert import EthicExpertAgent
from agents.legal_expert import LegalExpertAgent
from agents.psychology_expert import PsychologyExpertAgent
from agents.security_expert import SecurityExpertAgent
from agents.ai_expert import AIExpertAgent


async def run_council():
    print("🚀 Iniciando Consejo de Expertos - Sistema Multiagente Académico")

    # 1. Inicializar Pizarra Compartida
    print(f"\n📋 Creando Pizarra Compartida con el tema:\n'{CONSENSE_THEME}'")
    blackboard = Blackboard(topic=CONSENSE_THEME)

    # 2. Inicializar Agentes
    print("\n👥 Inicializando Agentes...")
    try:
        agents = [
            EthicExpertAgent(),
            LegalExpertAgent(),
            PsychologyExpertAgent(),
            SecurityExpertAgent(),
            AIExpertAgent(),
        ]

        # 3. Asignar Pizarra a los Agentes
        # Asignamos la pizarra a cada instancia para que puedan acceder al contexto compartido
        for agent in agents:
            agent.blackboard = blackboard
            print(f"  ✅ {agent.role_name} inicializado y conectado a la pizarra.")

        print("\n✨ Inicialización completada con éxito.")
        print("--------------------------------------------------")
        print(f"Estado de la Pizarra: {blackboard}")
        print("Agentes listos para comenzar el debate.")

        # 4. Iterar por cada agente, solicitar respuesta y actualizar pizarra
        for agent in agents:
            print(f"\n🗣️ Solicitando opinión a {agent.role_name}...")
            context = blackboard.get_context_for_agent(agent.role_name)
            respuesta = await agent.get_response(context)

            if respuesta:
                blackboard.add_opinion(agent.role_name, respuesta)
                print(
                    f"  📝 Respuesta recibida y registrada. Opiniones acumuladas: {len(blackboard.opinions)}"
                )
            else:
                print(f"  ⚠️ No se obtuvo respuesta de {agent.role_name}.")

        print("\n✅ Iteración completada. Estado final de la pizarra:")
        print(f"  - Tema: {blackboard.topic}")
        print(f"  - Opiniones registradas: {len(blackboard.opinions)}")

    except Exception as e:
        print(f"\n❌ Error durante la inicialización o iteración: {e}")
        import traceback

        traceback.print_exc()


def main():
    asyncio.run(run_council())


if __name__ == "__main__":
    main()
