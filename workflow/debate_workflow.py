from workflow.consensus_strategy import check_consensus, build_consensus_summary
from workflow.coordinator_agent import CoordinatorAgent  # opcional, si lo haces agente

def run_debate_workflow(topic: str, experts: list, max_rounds: int = 3):
    # 1. Opiniones iniciales
    initial_opinions = {e.role_name: e.initial_opinion(topic) for e in experts}

    history = {
        "topic": topic,
        "rounds": []
    }

    current_opinions = initial_opinions

    coordinator = CoordinatorAgent()  # si lo quieres como agente ADK

    for round_idx in range(1, max_rounds + 1):
        # 2.1 Resumen de la ronda actual
        round_summary = coordinator.summarize_round(topic, current_opinions, round_idx)

        # Guardar en el historial
        history["rounds"].append({
            "round": round_idx,
            "opinions": current_opinions,
            "summary": round_summary,
        })

        # 2.2 Evaluar consenso
        consensus_info = check_consensus(current_opinions)
        if consensus_info["is_consensus"]:
            break

        # 2.3 Pedir revisión a los expertos
        new_opinions = {}
        for e in experts:
            new_opinions[e.role_name] = e.revise_opinion(topic, round_summary)

        current_opinions = new_opinions

    # 3. Construir un resumen final de consenso (aunque sea parcial)
    final_summary = build_consensus_summary(current_opinions)

    return {
        "topic": topic,
        "initial_opinions": initial_opinions,
        "final_opinions": current_opinions,
        "history": history,
        "consensus": final_summary,
    }