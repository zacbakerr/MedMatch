from data.agent_class import HealthcareFacility, PatientSearch
from agents.converstaion import ReferralMatcher

# Create sample facilities
facilities = [
    HealthcareFacility(
        facility_name="City Physiotherapy Center",
        location="123 Medical Drive, London",
        availability=[9, 10, 11, 14, 15, 16],  # Available appointment hours
        facilities="""
        - Modern physiotherapy equipment
        - Hydrotherapy pool
        - Sports rehabilitation center
        - Specialized back pain treatment
        - Multiple treatment rooms
        """,
        price=75.0
    ),
    
    HealthcareFacility(
        facility_name="Advanced Spine Specialists",
        location="456 Harley Street, London",
        availability=[11, 13, 14],
        facilities="""
        - Advanced diagnostic imaging
        - Specialized spine treatment equipment
        - Pain management center
        - Rehabilitation gym
        - Surgical facilities
        """,
        price=200.0
    ),
    
    HealthcareFacility(
        facility_name="Community Health Clinic",
        location="789 High Street, London",
        availability=[9, 10, 11, 12, 13, 14, 15, 16],
        facilities="""
        - Basic physiotherapy equipment
        - General treatment rooms
        - Simple exercise facilities
        - Group therapy space
        """,
        price=45.0
    ),
    
    HealthcareFacility(
        facility_name="Elite Sports Medicine",
        location="321 Olympic Way, London",
        availability=[10, 11, 14, 15],
        facilities="""
        - State-of-the-art rehabilitation center
        - Advanced biomechanical analysis
        - Sports specific equipment
        - Recovery and conditioning facilities
        - Performance testing lab
        """,
        price=150.0
    )
]

# Create a sample patient
patient = PatientSearch(
    patient_location="15 Baker Street, London",
    condition_description="""
    Chronic lower back pain lasting 3 months. Pain is worse in the morning 
    and after sitting for long periods. Patient is a 45-year-old office worker 
    who exercises occasionally. Previous physiotherapy provided temporary relief. 
    Looking for long-term solution and pain management strategies.
    """,
    max_budget=100.0
)

def main():
    # Create matcher
    matcher = ReferralMatcher(facilities)
    
    # Find best matches
    print("Finding best matches for patient...")
    print("\nPatient Details:")
    print(f"Location: {patient.get_location()}")
    print(f"Budget: £{patient.get_budget()}")
    print(f"Condition: {patient.get_condition()}")
    print("\nEvaluating facilities...")
    
    matcher.find_best_match(patient)
    top_matches = matcher.get_best_matches(limit=3)
    
    print("\nTop Matches:")
    print("=" * 50)
    
    for i, (agent, result) in enumerate(top_matches, 1):
        print(f"\n{i}. {agent.facility.get_facility_name()}")
        print(f"Score: {result['score']:.2f}")
        print(f"Price: £{agent.facility.get_price()}")
        print(f"Travel Time: {result['travel_time']} minutes")
        print(f"Distance: {result['distance']:.1f} km")
        print("\nFacilities:")
        print(agent.facility.get_facilities())
        print("\nAI Evaluation:")
        print(result['evaluation']['ai_evaluation'])
        print("-" * 50)

if __name__ == "__main__":
    main() 