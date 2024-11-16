from typing import Dict, Tuple, Any, Optional, List
from data.agent_class import PatientSearch, HealthcareFacility
from .utils import DistanceCalculator, calculate_distance_decay
from .incoming_agent import IncomingAgent
import openai
import json

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
        # Collect all facility information upfront
        facilities_info = []
        for agent in self.incoming_agents:
            facility_info = agent.get_facility_info()
            
            # Early budget check
            if facility_info['price'] > patient_search.get_budget():
                self.conversation_results[agent] = {
                    "score": 0,
                    "facility_info": facility_info,
                    "evaluation": None,
                    "reason": "Facility excluded due to budget constraints",
                    "travel_time": None,
                    "distance": None
                }
                continue
            
            # Calculate travel time from Shoreditch Exchange
            travel_time, distance = self.distance_calculator.calculate_travel_time(
                "Shoreditch Exchange, London",
                facility_info['location']
            )
            
            facilities_info.append((agent, facility_info, travel_time, distance))

        if not facilities_info:
            return

        # Create single prompt for all facilities
        client = openai.OpenAI(
            api_key="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"
        )
        
        prompt = f"""
        As a healthcare evaluator, analyze these facilities for the patient condition: {patient_search.get_condition()}

        Facilities to evaluate:
        """
        
        for _, facility, _, _ in facilities_info:
            prompt += f"""
            - Name: {facility['name']}
              Location: {facility['location']}
              Available Slots: {facility['available_slots']}
              Facilities: {facility['facilities']}
              Price: {facility['price']}
            """

        prompt += """
        For each facility, provide a score (0-100) and brief reasoning.
        Return in this exact JSON format:
        {
            "evaluations": [
                {
                    "facility_name": "<name>",
                    "score": <number>,
                    "reasoning": "<one sentence explanation>"
                },
                ...
            ]
        }
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a healthcare evaluator. Provide a structured JSON response."},
                {"role": "user", "content": prompt}
            ]
        )
        
        ai_evaluation = response.choices[0].message.content

        ai_evaluation = ai_evaluation.strip()
        # Remove the ```json from start and ``` from end
        if ai_evaluation.startswith('```'):
            first_newline = ai_evaluation.find('\n')
            last_backticks = ai_evaluation.rfind('```')
            ai_evaluation = ai_evaluation[first_newline:last_backticks].strip()

        try:
            ai_evaluation_data = json.loads(ai_evaluation)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Failed content:", repr(ai_evaluation))
            return

        # Process evaluations and update conversation_results
        for agent, facility_info, travel_time, distance in facilities_info:
            score = self._parse_ai_score(ai_evaluation_data, facility_info['name'])
            self.conversation_results[agent] = {
                "score": score,
                "facility_info": facility_info,
                "evaluation": ai_evaluation,
                "travel_time": travel_time,
                "distance": distance
            }
    
    def _parse_ai_score(self, ai_evaluation: dict, facility_name: str) -> float:
        """Extract numerical score from AI evaluation text for a specific facility"""
        try:
            for evaluation in ai_evaluation['evaluations']:
                if evaluation['facility_name'] == facility_name:
                    return float(evaluation['score'])
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

        for item in self.conversation_results.items():
            print(item)
            print("")
            
        sorted_results = sorted(
            self.conversation_results.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return sorted_results[:limit]
    
    def get_filtered_matches(self) -> List[Tuple[IncomingAgent, Dict[str, Any]]]:
        """
        Get all matches with score > 60, sorted by score descending
        
        Returns:
            List of tuples containing (agent, result_details) for qualified matches
        """
        if not self.conversation_results:
            return []
        
        # Filter matches with score > 60 and sort by score
        qualified_matches = [
            (agent, result) 
            for agent, result in self.conversation_results.items()
            if result["score"] >= 60
        ]
        
        sorted_results = sorted(
            qualified_matches,
            key=lambda x: x[1]["score"],
            reverse=True
        )
        
        return sorted_results
