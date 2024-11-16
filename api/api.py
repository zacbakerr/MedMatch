from flask import Flask, request, jsonify
from data.agent_class import PatientSearch, HealthcareFacility
from agents.converstaion import ReferralMatcher
from typing import List
import os
from supabase import create_client, Client
from flask_cors import CORS
import openai
import json

app = Flask(__name__)

CORS(app)

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

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/match-patient', methods=['POST'])
def match_patient():
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                'error': 'Missing patient description'
            }), 400
        
        # Parse the description using LLM to extract condition, location, and budget
        client = openai.OpenAI(
            api_key="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"
        )
        
        prompt = f"""
        Extract the medical condition, location (if provided), and budget (if provided) from this description:
        {data['description']}

        Return in this exact JSON format:
        {{
            "condition": "the medical condition or issue",
            "location": "the location if mentioned, otherwise null",
            "budget": number or null if not mentioned
        }}

        Be sure to:
        1. Always extract the medical condition
        2. Set location to null if not explicitly mentioned
        3. Set budget to null if no specific amount is mentioned
        4. If budget is mentioned, convert it to a number (remove currency symbols)
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a healthcare data extractor. Provide a structured JSON response."},
                {"role": "user", "content": prompt}
            ]
        )
        
        parsed_info = json.loads(response.choices[0].message.content)
        
        # Set defaults for missing values
        location = parsed_info.get('location') or "Shoreditch Exchange, London"
        budget = parsed_info.get('budget') or 99999999
        condition = parsed_info['condition']  # This should always be present
            
        patient_search = PatientSearch(
            patient_location=location,
            condition_description=condition,
            max_budget=budget
        )
        
        facilities = get_facilities_from_db()
        
        if not facilities:
            return jsonify({
                'error': 'No facilities available'
            }), 500
        
        matcher = ReferralMatcher(facilities)
        matcher.find_best_match(patient_search)
        
        # Get all matches with score > 60
        matches = matcher.get_filtered_matches()
        
        if not matches:
            return jsonify({
                'error': 'No suitable matches found'
            }), 404
        
        # Find best overall match (highest score)
        best_match = matches[0]  # Already sorted by score
        
        # Find best price among qualified matches
        best_price_match = min(matches, key=lambda x: x[1]['facility_info']['price'])
        
        # Find closest match among qualified matches
        closest_match = min(matches, key=lambda x: x[1].get('travel_time', float('inf')) 
                          if x[1].get('travel_time') is not None else float('inf'))
        
        def format_match(match_tuple):
            agent, details = match_tuple
            facility_info = details['facility_info']
            return {
                "facility_name": facility_info['name'],
                "location": facility_info['location'],
                "match_score": details['score'],
                "estimated_cost": facility_info['price'],
                "travel_time_car": details.get('travel_time', None),
                "price": facility_info['price']
            }
        
        response = {
            "best_match": format_match(best_match),
            "best_price": format_match(best_price_match),
            "closest_match": format_match(closest_match),
            "parsed_input": {
                "condition": condition,
                "location": location,
                "budget": budget
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in match_patient: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
