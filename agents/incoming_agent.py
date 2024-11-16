import os
import openai
from typing import Dict, Any
from data.agent_class import HealthcareFacility

class IncomingAgent:
    def __init__(self, facility: HealthcareFacility):
        """
        Initialize incoming agent for a specialist facility
        
        Args:
            facility: HealthcareFacility instance containing facility details
        """
        self.facility = facility
        
    def get_facility_info(self) -> Dict[str, Any]:
        """Get basic facility information"""
        return {
            "name": self.facility.get_facility_name(),
            "location": self.facility.get_location(),
            "available_slots": self.facility.get_availability(),
            "facilities": self.facility.get_facilities(),
            "price": self.facility.get_price()
        }
    
    def evaluate_patient_case(self, patient_condition: str) -> Dict[str, Any]:
        """
        Evaluate patient case using AI to analyze facility capabilities
        """
        facility_info = self.get_facility_info()
        
        # Initialize OpenAI client with API key
        client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        prompt = f"""
        As a specialist facility ({facility_info['name']}), evaluate this patient case:
        
        Patient Condition: {patient_condition}
        
        Our Facility Information:
        - Name: {facility_info['name']}
        - Available Equipment/Services: {facility_info['facilities']}
        - Available Slots: {facility_info['available_slots']}
        
        Analyze if we can handle this case and provide:
        1. Capability score (0-100) - How well equipped we are to handle this specific case
        2. Whether we can provide specialized treatment
        3. Estimated treatment duration
        4. Detailed reasoning for the evaluation
        
        The score MUST be on a scale of 0 to 100, where:
        0 = Cannot handle the case at all
        25 = Basic capability but not ideal
        50 = Average capability
        75 = Good capability with most required services
        100 = Perfect match with all specialized services needed
        
        Focus only on medical suitability and availability.
        Include the numerical score (0-100) at the start of your response.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a healthcare facility evaluator. Always include a numerical score between 0-100 at the start of your response."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse AI response to extract evaluation metrics
        ai_evaluation = response.choices[0].message.content
        
        return {
            "facility_info": facility_info,
            "ai_evaluation": ai_evaluation
        }