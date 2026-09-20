import db
from assistant.context_builder import build_node_context
from assistant.intent_router import route_intent
from assistant.llm_provider import get_llm_provider

def run_test():
    print("--- Phase 24 & 25: Assistant Determinism Test ---")
    
    conn = db.get_connection()
    context = build_node_context(conn, 999)
    conn.close()
    
    # 1. Ask about temperature
    intent_temp = route_intent("What is the temperature", "en-IN")
    ans_temp = get_llm_provider().generate_answer(intent_temp, context, "en-IN")
    print(f"Q: What is the temperature?\nA: {ans_temp}")
    
    # 2. Ask about moisture
    intent_moist = route_intent("What is the moisture", "en-IN")
    ans_moist = get_llm_provider().generate_answer(intent_moist, context, "en-IN")
    print(f"Q: What is the moisture?\nA: {ans_moist}")
    
    # 3. Ask about unknown
    intent_unk = route_intent("How should I prepare my farm for heavy rain?", "en-IN")
    ans_unk = get_llm_provider().generate_answer(intent_unk, context, "en-IN")
    print(f"Q: How should I prepare my farm for heavy rain?\nA: {ans_unk}")

if __name__ == "__main__":
    run_test()
