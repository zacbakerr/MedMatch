class PatientSearch:
    """A class representing a patient's search criteria for healthcare facilities."""
    def __init__(self, patient_location: str, condition_description: str, max_budget: float):
        self._patient_location = patient_location
        self._condition_description = condition_description
        self._max_budget = max_budget

    def get_location(self) -> str:
        return self._patient_location

    def get_condition(self) -> str:
        return self._condition_description

    def get_budget(self) -> float:
        return self._max_budget

    def set_location(self, location: str) -> None:
        self._patient_location = location

    def set_condition(self, condition: str) -> None:
        self._condition_description = condition

    def set_budget(self, budget: float) -> None:
        self._max_budget = budget


class HealthcareFacility:
    """A class representing a healthcare facility with its details."""
    def __init__(self, facility_name: str, location: str, availability: list[int], facilities: str, price: float):
        self._facility_name = facility_name
        self._location = location
        self._availability = availability
        self._facilities = facilities
        self._price = price

    def get_facility_name(self) -> str:
        return self._facility_name

    def get_location(self) -> str:
        return self._location

    def get_availability(self) -> int:
        return self._availability

    def get_facilities(self) -> str:
        return self._facilities

    def get_price(self) -> float:
        return self._price
    
    def set_facility_name(self, facility_name: str) -> None:
        self._facility_name = facility_name

    def set_location(self, location: str) -> None:
        self._location = location

    def set_availability(self, availability: int) -> None:
        self._availability = availability

    def set_facilities(self, facilities: str) -> None:
        self._facilities = facilities

    def set_price(self, price: float) -> None:
        self._price = price