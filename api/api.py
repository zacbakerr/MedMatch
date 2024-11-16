from flask import Flask, request, jsonify
from data.agent_class import PatientSearch, HealthcareFacility
from agents.converstaion import ReferralMatcher
from typing import List
import os
from supabase import create_client, Client

app = Flask(__name__)

# Initialize Supabase client
supabase: Client = create_client(
    "https://doltxirrioqkjpgnmwwm.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvbHR4aXJyaW9xa2pwZ25td3dtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE3NzE3ODMsImV4cCI6MjA0NzM0Nzc4M30.7JgT5JOK3w7WAxUwq61EufQ0aJDKfx015sIOnAmkQBU"
)

def get_facilities_from_db() -> List[HealthcareFacility]:
    """Fetch healthcare facilities from Supabase"""
    try:
        response = supabase.table('facility_information').select("*").execute()
        facilities = []
        
        for facility_data in response.data:
            facility = HealthcareFacility(
                facility_name=facility_data['facility_name'],
                location=facility_data['location'],
                availability=facility_data['availability'],
                facilities=facility_data['facilities'],
                price=facility_data['price']
            )
            facilities.append(facility)
            
        return facilities
    except Exception as e:
        print(f"Error fetching facilities: {e}")
        return []

@app.route('/api/match-patient', methods=['POST'])
def match_patient():
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                'error': 'Missing patient description'
            }), 400
            
        patient_search = PatientSearch(
            patient_location="London",
            condition_description=data['description'],
            max_budget=5000
        )
        
        facilities = get_facilities_from_db()
        
        if not facilities:
            return jsonify({
                'error': 'No facilities available'
            }), 500
        
        matcher = ReferralMatcher(facilities)
        matcher.find_best_match(patient_search)
        
        # Get only the best match
        matches = matcher.get_best_matches(limit=1)
        
        if not matches:
            return jsonify({
                'error': 'No suitable matches found'
            }), 404
        
        # Get the single best match
        best_agent, best_details = matches[0]
        facility_info = best_details['facility_info']
        
        # Return only essential information
        return jsonify({
            'facility_name': facility_info['name'],
            'location': facility_info['location'],
            'match_score': best_details['score']
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
