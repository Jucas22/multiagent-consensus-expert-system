from agents import (
    EthicExpertAgent,
    PrivacyExpertAgent,
    PsychologyExpertAgent,
    LegalExpertAgent,
    AIEngineeringExpertAgent,
    CybersecurityExpertAgent,
)
from workflow.debate_workflow import run_debate_workflow
from workflow.document_generator import generate_consensus_document
from config import OUTPUT_DIR


def main():
    topic = input("Introduce el tema a debatir (enter para usar el tema por defecto): ")
    if not topic:
        topic = (
            "¿Debería utilizarse un sistema de IA para analizar conversaciones de "
            "WhatsApp, redes sociales, historial de navegación y compras online "
            "con el fin de detectar patologías psicológicas?"
        )

    # 1. Inicializar expertos
    experts = [
        EthicExpertAgent(),
        PrivacyExpertAgent(),
        PsychologyExpertAgent(),
        LegalExpertAgent(),
        AIEngineeringExpertAgent(),
        CybersecurityExpertAgent(),  # o PolicyExpertAgent()
    ]

    # 2. Ejecutar workflow de debate
    debate_result = run_debate_workflow(topic, experts)

    # 3. Generar documento de consenso
    consensus_doc = generate_consensus_document(topic, debate_result)

    # 4. Guardar en outputs/
    path = OUTPUT_DIR / "consenso_salud_mental_ia.md"
    path.write_text(consensus_doc, encoding="utf-8")

    print(f"Documento de consenso generado en: {path}")


if __name__ == "__main__":
    main()
