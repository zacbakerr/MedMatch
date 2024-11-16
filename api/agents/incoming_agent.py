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
        # Initialize OpenAI client with API key
        client = openai.OpenAI(
            api_key="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"
        )
        
        facility_info = self.get_facility_info()
        
        # Prepare the prompt with facility information
        prompt = f"""
        As a healthcare evaluator, analyze this facility for the patient condition: {patient_condition}

        Facility Information:
        - Name: {facility_info['name']}
        - Location: {facility_info['location']}
        - Available Slots: {facility_info['available_slots']}
        - Facilities: {facility_info['facilities']}
        - Price: {facility_info['price']}

        Provide a score from 0-100 based on how well the facility matches the patient's needs.
        Return response in this exact JSON format:
        {{
            "score": <number>,
            "reasoning": "<one sentence explanation>"
        }}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a healthcare evaluator. Provide a concise JSON response."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse AI response
        ai_evaluation = response.choices[0].message.content

        print(ai_evaluation)
        
        return {
            "facility_info": facility_info,
            "ai_evaluation": ai_evaluation
        }