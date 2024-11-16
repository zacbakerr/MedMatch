import openai
from typing import Dict, Any

class IncomingAgent:
    def __init__(self, specialist_facility):
        """
        Initialize incoming agent for a specialist facility
        
        Args:
            specialist_facility: Class instance containing specialist facility details
        """
        self.facility = specialist_facility
        
    def get_facility_info(self) -> Dict[str, Any]:
        """Get basic facility information"""
        return {
            "name": self.facility.name,
            "specialty": self.facility.specialty,
            "location": self.facility.location,
            "waiting_time": self.facility.get_waiting_time(),
            "available_equipment": self.facility.get_equipment(),
            "next_available_slot": self.facility.get_next_slot()
        }
    
    async def evaluate_patient_case(self, patient_condition: Dict, requirements: Dict) -> Dict[str, Any]:
        """
        Evaluate patient case using AI to analyze facility capabilities
        """
        facility_info = self.get_facility_info()
        
        prompt = f"""
        As a specialist facility ({self.facility.specialty}), evaluate this patient case:
        
        Patient Condition: {patient_condition}
        Requirements: {requirements}
        
        Our Facility Information:
        - Name: {facility_info['name']}
        - Equipment: {facility_info['available_equipment']}
        - Current Wait Time: {facility_info['waiting_time']}
        - Next Available Slot: {facility_info['next_available_slot']}
        
        Analyze if we can handle this case and provide:
        1. Capability score (0-10)
        2. Whether we can provide specialized treatment
        3. Estimated treatment duration
        4. Cost estimate
        5. Detailed reasoning
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical specialist facility evaluating a patient referral."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse AI response to extract evaluation metrics
        ai_evaluation = response.choices[0].message.content
        capability_score = self.facility.assess_patient_suitability(patient_condition)
        
        return {
            "can_handle": capability_score > 0,
            "capability_score": capability_score,
            "specialized_treatment_available": self.facility.check_treatment_availability(patient_condition),
            "estimated_treatment_duration": self.facility.estimate_treatment_duration(patient_condition),
            "cost_estimate": self.facility.estimate_cost(patient_condition),
            "ai_evaluation": ai_evaluation
        }
