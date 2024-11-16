import openai
import asyncio
from typing import Dict, Tuple, Any, Optional, List
from data.agent_class import PatientSearch, HealthcareFacility
from .utils import DistanceCalculator, calculate_distance_decay
from .incoming_agent import IncomingAgent

class ReferralMatcher:
    def __init__(self, facilities: List[HealthcareFacility]):
        """
        Initialize the referral matching system
        
        Args:
            facilities: List of HealthcareFacility instances
        """
        self.incoming_agents = [IncomingAgent(facility) for facility in facilities]
        self.distance_calculator = DistanceCalculator()
        self.conversation_results = {}
        
    def find_best_match(self, patient_search: PatientSearch) -> None:
        """
        Find the best matching facility for a patient
        
        Args:
            patient_search: PatientSearch instance containing patient requirements
        """
        for agent in self.incoming_agents:
            self._evaluate_facility(agent, patient_search)
    
    def _evaluate_facility(self, agent: IncomingAgent, patient_search: PatientSearch) -> None:
        """Evaluate a single facility for the patient"""
        facility_info = agent.get_facility_info()
        
        # Early budget check
        # if facility_info['price'] > patient_search.get_budget():
        #     self.conversation_results[agent] = {
        #         "score": 0,
        #         "facility_info": facility_info,
        #         "evaluation": None,
        #         "reason": "Facility excluded due to budget constraints",
        #         "travel_time": None,
        #         "distance": None
        #     }
        #     return
        
        # Get facility's evaluation of the patient case
        evaluation = agent.evaluate_patient_case(patient_search.get_condition())
        
        # Calculate travel information
        travel_time, distance = self.distance_calculator.calculate_travel_time(
            patient_search.get_location(),
            facility_info['location']
        )
        
        # Get base score (0-100)
        base_score = self._parse_ai_score(evaluation['ai_evaluation'])
        
        # Get distance decay factor (0-1)
        decay_factor = calculate_distance_decay(travel_time)
        
        # Apply decay factor
        decayed_score = base_score * decay_factor
        
        # Scale the decayed score back to 0-100 range
        max_decayed_score = max(
            [self._get_decayed_score(agent) for agent in self.incoming_agents] + [decayed_score]
        )
        
        if max_decayed_score > 0:
            final_score = (decayed_score / max_decayed_score) * 100
        else:
            final_score = 0
        
        self.conversation_results[agent] = {
            "score": final_score,
            "raw_score": base_score,
            "decay_factor": decay_factor,
            "facility_info": facility_info,
            "evaluation": evaluation,
            "travel_time": travel_time,
            "distance": distance
        }
    
    def _get_decayed_score(self, agent: IncomingAgent) -> float:
        """Helper method to get decayed score for an agent if it exists"""
        if agent in self.conversation_results and self.conversation_results[agent].get("raw_score") is not None:
            return self.conversation_results[agent]["raw_score"] * self.conversation_results[agent].get("decay_factor", 1.0)
        return 0
    
    def _parse_ai_score(self, ai_evaluation: str) -> float:
        """Extract numerical score from AI evaluation text"""
        try:
            import re
            scores = re.findall(r'\b([0-9]{1,3})\b', ai_evaluation)
            if scores:
                score = float(scores[0])
                return min(max(score, 0), 100)  # Keep as 0-100
        except:
            pass
        return 0.0
    
    def get_best_matches(self, limit: int = 3) -> List[Tuple[IncomingAgent, Dict[str, Any]]]:
        """
        Get the top matching facilities
        
        Args:
            limit: Number of top matches to return
            
        Returns:
            List of tuples containing (agent, result_details)
        """
        if not self.conversation_results:
            return []
            
        # Sort facilities by score
        sorted_results = sorted(
            self.conversation_results.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return sorted_results[:limit]
