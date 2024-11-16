import openai
import asyncio
from typing import Dict, Tuple, Any, Optional

class ReferralConversation:
    def __init__(self, outgoing_agent, incoming_agents):
        self.outgoing_agent = outgoing_agent
        self.incoming_agents = incoming_agents
        self.conversation_results = {}
        
    async def conduct_referral_conversation(self, patient_id: str) -> None:
        """
        Conduct AI-powered conversations between GP and specialist facilities
        """
        patient_info = self.outgoing_agent.get_patient_info(patient_id)
        
        # Create tasks for all specialist evaluations
        tasks = []
        for specialist in self.incoming_agents:
            tasks.append(self._conduct_single_conversation(specialist, patient_info))
        
        # Run all conversations concurrently
        await asyncio.gather(*tasks)
    
    async def _conduct_single_conversation(self, specialist, patient_info: Dict) -> None:
        """Conduct conversation with a single specialist"""
        facility_info = specialist.get_facility_info()
        
        # Early budget check
        if facility_info.get('min_cost', 0) > patient_info['budget']:
            # Skip conversation if facility is over budget
            self.conversation_results[specialist] = {
                "score": 0,
                "facility_info": facility_info,
                "evaluation": None,
                "conversation_summary": "Facility excluded due to budget constraints",
                "travel_time": None,
                "distance": None
            }
            return
        
        # Initialize conversation with AI
        conversation_prompt = f"""
        Patient Information:
        {patient_info}
        
        Facility Information:
        {facility_info}
        
        Conduct a brief conversation between the GP and specialist facility to determine suitability for referral.
        Focus on key aspects like:
        1. Patient's specific needs
        2. Facility's capabilities
        3. Treatment options
        4. Availability and timing
        5. Cost considerations
        """
        
        # Simulate conversation using AI
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are moderating a conversation between a GP and a specialist facility."},
                {"role": "user", "content": conversation_prompt}
            ]
        )
        
        conversation_summary = response.choices[0].message.content
        
        # Get specialist's evaluation
        specialist_evaluation = await specialist.evaluate_patient_case(
            patient_info["condition"],
            patient_info["requirements"]
        )
        
        # Combine all information
        complete_response = {
            **facility_info,
            **specialist_evaluation,
            "conversation_summary": conversation_summary
        }
        
        # Score the conversation
        score = await self.outgoing_agent.evaluate_specialist_response(
            complete_response,
            patient_info["requirements"]
        )
        
        # Add travel information to results
        travel_time, distance = self.outgoing_agent.distance_calculator.calculate_travel_time(
            patient_info['address'],
            facility_info['location']
        )
        
        self.conversation_results[specialist] = {
            "score": score,
            "facility_info": facility_info,
            "evaluation": specialist_evaluation,
            "conversation_summary": conversation_summary,
            "travel_time": travel_time,
            "distance": distance
        }
    
    def get_best_match(self) -> Tuple[Optional[Any], float, Optional[Dict]]:
        if not self.conversation_results:
            return None, 0, None
            
        best_specialist = max(
            self.conversation_results.items(),
            key=lambda x: x[1]["score"]
        )
        
        return (
            best_specialist[0],
            best_specialist[1]["score"],
            best_specialist[1]["facility_info"]
        )
