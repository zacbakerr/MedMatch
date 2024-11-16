# In the ReferralMatcher class, modify the _evaluate_facility method:

def _evaluate_facility(self, agent: IncomingAgent, patient_search: PatientSearch) -> None:
    """Evaluate a single facility for the patient"""
    facility_info = agent.get_facility_info()
    
    # Get facility's evaluation of the patient case
    evaluation = agent.evaluate_patient_case(patient_search.get_condition())
    
    # Get base score (0-100) based only on facility capabilities
    base_score = self._parse_ai_score(evaluation['ai_evaluation'])
    
    # Store all information but only use base_score for now
    self.conversation_results[agent] = {
        "score": base_score,  # Using only the base facility capability score
        "raw_score": base_score,
        # Storing but not using these factors for now
        # "decay_factor": decay_factor,
        "facility_info": facility_info,
        "evaluation": evaluation,
        # "travel_time": travel_time,
        # "distance": distance
    }
    
    # Commented out location/budget factors for future use
    """
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
        return
        
    # Calculate travel information
    travel_time, distance = self.distance_calculator.calculate_travel_time(
        patient_search.get_location(),
        facility_info['location']
    )
    
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
    """ 