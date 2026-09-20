# Vermikendra Product Requirements Document (PRD)

## 1. Problem Statement
Rural vermicompost operators (e.g., KVKs, Lakhpati Didi) lack scientific methods to determine compost maturity, often leading to premature or delayed harvesting. Physical constraints such as ammonia and high moisture degrade electronic sensors quickly. 

## 2. Core Objectives
Vermikendra is a cyber-physical system (CPS) designed to scientifically measure and predict vermicompost readiness in offline, rural environments.
- Monitor temperature gradients (preventing worm loss > 35°C).
- Monitor moisture content and provide misting actuation.
- Estimate compost maturity by analyzing the rate-of-change of CO2 respiration (via ePTFE-protected NDIR sensing).

## 3. Success Metrics
1. **Safety:** System must function 100% offline (no cloud dependency).
2. **Reliability:** Hardware must survive 95% RH and high ammonia environments using ePTFE venting.
3. **Resilience:** The edge node must protect the bed (actuating the misting pump) even if the gateway is offline.
4. **Accuracy:** Respiration rate trend calculation (R² > 0.90) determines readiness.
