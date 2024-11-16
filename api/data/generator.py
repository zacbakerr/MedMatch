import numpy as np
import random
from typing import List
from agent_class import HealthcareFacility

class FacilityGenerator:
    """Generator for creating healthcare facility objects"""
    
    # List of facility details
    FACILITIES = [
        {
            "name": "Step By Step Recovery",
            "location": "5-7 Cranwood St, London EC1V 9EE", 
            "facilities":"Expert private residential alcohol treatment, drug detox, drug rehabilitation, addiction specialist care",
            "mean_price": 8500,
            "std_price": 1500,
            "min_price": 6000
        },
        {
            "name": "OK Rehab",
            "location": "48B Gun St, London E1 6AH",
            "facilities": "OK Rehab specialises in local drug and alcohol rehab and addiction treatment. This treatment is available via both inpatient and outpatient treatment providers. We also work with clinics that are able to facilitate treatment taking place in your own home, who are able to provide professional intervention and home detoxification. At OK Rehab, our aim is to help individuals break free from the shackles of addiction and find a treatment that's ideally suited to their needs. This treatment is applicable for drug addiction, alcoholism and process/behavioural addictions. Many of the treatments we may recommend taking place at residential rehab clinics. We have partnered with over 140 clinics of this nature across the UK and abroad. These clinics offer standalone detoxification services, or alternatively, you may combine detox with an extended rehabilitation.",
            "mean_price": 7500,
            "std_price": 1200,
            "min_price": 5500
        },
        {
            "name": "Detox Plus UK - Alcohol & Drug Rehab London",
            "location": "71-75 Shelton St, London WC2H 9JQ",
            "facilities": "We provide medical withdrawal treatment and alcohol rehabilitation with a comprehensive recovery package that treats every aspect of addiction. Our evidence-based treatments include CBT (Cognitive Behavioural Therapy), psychotherapy, integrated therapy combining psychotherapy and addiction counselling, person-centred therapy, dual diagnoses treatment, individual addiction therapy, and group therapy. We also offer cutting-edge holistic and complementary therapies like LLLT (Lower level laser light therapy) for sleep and stress reduction during withdrawals, and NAD treatment to reduce withdrawal side effects. Our bodywork consultants create bespoke health plans covering dietetics, fitness and overall wellbeing. Additional therapies include yoga, mindfulness, meditation, Thai Chi, massage and acupuncture for relaxation and healing, as well as music, art, equine therapy and drama for emotional processing. Each London alcohol treatment centre provides fully personalized addiction treatment programmes tailored to individual needs.",
            "mean_price": 9500,
            "std_price": 1800,
            "min_price": 7000
        },
        {
            "name": "Maudsley Hospital",
            "location": "Denmark Hill, London SE5 8AZ",
            "facilities": "The Maudsley Hospital in Camberwell first opened in 1915, initially as a military hospital and then in 1923 as a psychiatric hospital. Find out about our history The hospital is home to both inpatient and outpatient services for children and adults. To find out more about our services at Maudsley Hospital use our service finder.",
            "mean_price": 3500,
            "std_price": 800,
            "min_price": 2500
        },
        {
            "name": "Nightingale Hospital",
            "location": "11-19 Lisson Grove, London NW1 6SH",
            "facilities": "Central London's leading private mental health hospital, specialising in general mental health, including eating disorders and addictions. For over 30 years, we've been delivering leading mental health care across a variety of mental health conditions, such as anxiety, depression, obsessive-compulsive disorder (OCD), stress, and bipolar; as well as addictions and eating disorders. We offer effective and evidence-based treatment for a range of mental health problems, across outpatient treatment and therapy, day-patient treatment and inpatient treatment settings. We also offer repetitive transcranial magnetic stimulation (rTMS), electroconvulsive therapy (ECT) and a nasal spray for those with treatment-resistant depression.",
            "mean_price": 4200,
            "std_price": 900,
            "min_price": 3000
        },
        {
            "name": "Newham Centre for Mental Health",
            "location": "Cherry Tree Way, Glen Rd, London E13 8SP",
            "facilities": "The Newham Centre for Mental Health can be found at the rear of the site behind Newham University Hospital. The Coborn Centre for Adolescent Mental Health and the Research Unit is housed in neighbouring buildings.The unit provides a wide range of services available for people who require inpatient support and care for mental health problems or a mental health crisis. The unit aims to provide short and focused admissions in a 24 hour, seven days a week supportive and safe environment. We work closely with external organisations, stakeholders, statutory and non-statutory agencies which are there to support the patients on their journey to recovery. As an inpatient care provider, the service focuses on the needs of the individual and provides care that is individualised and promotes recovery and inclusion.",
            "mean_price": 2800,
            "std_price": 600,
            "min_price": 2000
        },
        {
            "name": "Westport Care Home",
            "location": "14-26 Westport St, Stepney Green, London E1 0RA",
            "facilities": "Based in East London's Stepney Green, our beautiful 41-bed home is an active part of our local community and provides respite care and long-term care for people who need residential, residential dementia and end of life care. Our home is a place of freedom and respect, where our dedicated team, many of whom live in the local areas of Barking, Upminster and Ilford, encourage residents to make their own choices and support them to remain as independent as possible. Known for our home-from-home environment, quality care and a fun and friendly atmosphere. we also maintain close contact with the vibrant inner London communities of Limehouse, Shadwell and Mile End, as many of the residents have lived in the local area all their lives.",
            "mean_price": 1200,
            "std_price": 300,
            "min_price": 800
        },
        {
            "name": "Bridgeside Lodge Care Home",
            "location": "61 Wharf Rd, London N1 7RY",
            "facilities": "Bridgeside Lodge offers dedicated and specialist care within a contemporary, gated care centre adjacent to the stunning Regent's Canal in Islington, North London. We are within easy reach for families, friends and loved ones close to St Pancras and Kings Cross. Our 24-hour care facility is built and furnished to the highest standards, offering support for adults aged 18 and above, including older people. Our expansive property is staffed by incredible teams of carers, complemented by visiting therapists, ensuring all residents enjoy a relaxed, supported lifestyle. Bridgeside Lodge offers professional care support for many conditions, including neurological, spinal and dementia diagnoses.",
            "mean_price": 1100,
            "std_price": 200,
            "min_price": 900
        },
        {
            "name": "Anchor - Silk Court care home",
            "location": "16 Ivimey St, London E2 6LR",
            "facilities": "Anchor's Silk Court care home in Bethnal Green is a trusted provider of care for elderly people, and we offer support for older people who have residential and dementia care needs. Our care home's qualified staff provide 24-hour care and support to help you maintain your chosen lifestyle. At Silk Court, activities play an important role and we aim to enhance our residents' quality of life by providing a varied range of social activities. We pride ourselves on the quality of our catering, with our Chef Manager preparing meals daily from fresh, seasonal ingredients. Set in a residential location and in its own grounds, Silk Court is near to local shops, pubs, post office. Our home has excellent bus and railway routes to the city. In times of uncertainty, Anchor is a care provider you can depend on. We are proudly not-for-profit with 60 years of experience. We're here to help and look forward to giving you a warm welcome.",
            "mean_price": 1500,
            "std_price": 100,
            "min_price": 750
        }
    ]
    
    @classmethod
    def generate_all_facilities(cls) -> List[HealthcareFacility]:
        """Generate all facilities from the FACILITIES list"""
        generated_facilities = []
        
        for facility in cls.FACILITIES:
            # Generate price using normal distribution
            price = max(facility["min_price"], 
                       np.random.normal(facility["mean_price"], 
                                      facility["std_price"]))
            
            # Generate random availability list (8 time slots)
            availability = [random.randint(0, 1) for _ in range(8)]
            
            # Create facility object
            generated_facility = HealthcareFacility(
                facility_name=facility["name"],
                location=facility["location"],
                availability=availability,
                facilities=facility["facilities"],
                price=price
            )
            
            generated_facilities.append(generated_facility)
            
        return generated_facilities


# Example usage
if __name__ == "__main__":
    # Generate all facilities
    facilities = FacilityGenerator.generate_all_facilities()
    
    # Print generated facilities
    for i, facility in enumerate(facilities, 1):
        print(f"\nFacility {i}:")
        print(facility)
        print(f"Location: {facility.get_facility_name()}")
        print(f"Location: {facility.get_location()}")
        print(f"Availability slots: {facility.get_availability()}")
        print(f"Price: £{facility.get_price():,.2f}")
        print(f"Facilities: {facility.get_facilities()}")