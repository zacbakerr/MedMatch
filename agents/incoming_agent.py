import os
import openai
from typing import Dict, Any
from data.agent_class import HealthcareFacility

class IncomingAgent:
    def __init__(self, facility: HealthcareFacility):
        self.facility = facility
        
    def get_facility_info(self) -> Dict[str, Any]:
        return {
            "name": self.facility.get_facility_name(),
            "location": self.facility.get_location(),
            "available_slots": self.facility.get_availability(),
            "facilities": self.facility.get_facilities(),
            "price": self.facility.get_price()
        }
    
    def evaluate_patient_case(self, patient_condition: str) -> Dict[str, Any]:
        facility_info = self.get_facility_info()
        
        client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        prompt = f"""
        As a specialist facility ({facility_info['name']}), evaluate if we have the EXACT facilities and expertise to treat this specific condition:
        
        Patient Condition: {patient_condition}
        
        Our Available Equipment/Services:
        {facility_info['facilities']}
        
        Analyze our capability and provide:
        1. Capability score (0-100) based ONLY on our SPECIFIC ability to treat this EXACT condition
        2. List the SPECIFIC equipment/expertise we have that DIRECTLY treats this condition
        3. List what aspects of the condition we CANNOT treat
        4. Explain why we should or should not treat this patient
        
        The score MUST be on a scale of 0 to 100, where:
        0-15 = We do not have specific facilities/expertise for this condition
        16-30 = We have very basic facilities that might help, but are not designed for this
        31-50 = We have some relevant facilities but lack specialized treatment options
        51-70 = We have most necessary facilities but aren't specialized in this condition
        71-85 = We specialize in this exact condition with proper facilities
        86-100 = We are a dedicated center of excellence for this specific condition
        
        CRITICAL SCORING RULES:
        - Score ZERO if we don't have specific treatment facilities for the exact condition
        - General care facilities are worth maximum 15 points
        - "Nice environment" or "24/7 care" is worth ZERO points
        - Supporting facilities (e.g., general medical care) are worth maximum 10 additional points
        - Scores above 70 require PROOF that we specifically treat this condition
        - Scores above 85 require PROOF that we are a dedicated facility for this condition
        
        Example:
        - A general hospital gets 15 for addiction (no specific treatment)
        - A care home gets 0 for addiction (no treatment facilities)
        - An addiction center gets 80 for addiction (specific treatment)
        - A specialized addiction hospital gets 95 (dedicated facility)
        
        BE EXTREMELY STRICT. When in doubt, score lower.
        Include the numerical score (0-100) at the start of your response.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an extremely strict medical facility evaluator. Your job is to ensure patients are sent ONLY to facilities that can directly treat their specific condition. General care facilities should score near zero unless they have specific treatment capabilities for the exact condition."},
                {"role": "user", "content": prompt}
            ]
        )
        
        ai_evaluation = response.choices[0].message.content

        print(ai_evaluation)
        
        return {
            "facility_info": facility_info,
            "ai_evaluation": ai_evaluation
        } 