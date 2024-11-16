import openai
from typing import Dict, Any
from .utils import DistanceCalculator, calculate_distance_decay

class OutgoingAgent:
    def __init__(self, gp_facility):
        """
        Initialize outgoing agent for a GP facility
        
        Args:
            gp_facility: Class instance containing GP facility details
        """
        self.gp = gp_facility
        self.conversation_scores = {}
        self.distance_calculator = DistanceCalculator()
        
    def get_patient_info(self, patient_id: str) -> Dict[str, Any]:
        """
        Get patient information from GP records
        
        Args:
            patient_id: Unique identifier for the patient
            
        Returns:
            dict: Patient information and medical requirements
        """
        return self.gp.get_patient_details(patient_id)
    
    async def evaluate_specialist_response(self, specialist_response: Dict, patient_info: Dict) -> float:
        """
        Use AI to evaluate specialist facility response and generate a score
        """
        # First check if the facility is within budget
        if specialist_response['cost_estimate'] > patient_info['budget']:
            return 0.0
        
        prompt = f"""
        As a GP evaluating specialist facilities for patient referral, analyze this specialist's response:
        
        Specialist Evaluation:
        {specialist_response['ai_evaluation']}
        
        Facility Details:
        - Capability Score: {specialist_response['capability_score']}
        - Wait Time: {specialist_response['waiting_time']}
        - Treatment Available: {specialist_response['specialized_treatment_available']}
        
        Patient Requirements:
        {patient_info['requirements']}
        
        Provide a numerical score (0-100) based on how well this facility matches the patient's needs.
        Consider these factors with their weights:
        - Medical Capability (60%)
        - Wait Time (20%)
        - Specialized Treatment (20%)
        
        Focus only on medical suitability and availability. Do not consider location or cost.
        Explain your scoring reasoning.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a GP evaluating specialist facilities for patient referral."},
                {"role": "user", "content": prompt}
            ]
        )
        
        ai_evaluation = response.choices[0].message.content
        base_score = self._parse_ai_score(ai_evaluation)
        
        # Calculate travel time and decay factor
        travel_time, distance = self.distance_calculator.calculate_travel_time(
            patient_info['address'],
            specialist_response['location']
        )
        
        decay_factor = calculate_distance_decay(
            travel_time,
            max_acceptable_time=patient_info.get('max_travel_time', 120)
        )
        
        # Apply decay factor to base score
        final_score = base_score * decay_factor
        
        return final_score
    
    def _parse_ai_score(self, ai_evaluation: str) -> float:
        """Extract numerical score from AI evaluation text"""
        # Implement parsing logic to extract score from AI response
        # This is a simplified example
        try:
            # Look for a number between 0 and 100 in the text
            import re
            scores = re.findall(r'\b([0-9]{1,3})\b', ai_evaluation)
            if scores:
                score = float(scores[0])
                return min(max(score, 0), 100) / 100  # Normalize to 0-1
        except:
            pass
        return 0.0
