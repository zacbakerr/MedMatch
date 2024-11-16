from .utils import DistanceCalculator, calculate_distance_decay

class OutgoingAgent:
    def __init__(self, gp_facility):
        self.gp = gp_facility
        self.conversation_scores = {}
        self.distance_calculator = DistanceCalculator()
    
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
        
        response = await openai.ChatCompletion.acreate(
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