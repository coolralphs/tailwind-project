from django import template
from django_countries import countries
from datetime import date, timedelta

register = template.Library()

@register.filter
def alphabet_counter(value):
    return chr(ord('A') + value - 1)

@register.filter
def unique_by(queryset, field_name):
    seen = set()
    result = []
    for obj in queryset:
        field_value = getattr(obj, field_name)
        if field_value not in seen:
            seen.add(field_value)
            result.append(obj)
    return result

@register.filter
def dictsorttwo(value, key):
    return dict(sorted(value.items(), key=lambda item: item[key]))

@register.filter
def get_fields(obj):
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]

@register.filter
def unique_countries(queryset, field_name):
    seen = set()
    result = []

    # Create a lookup dictionary with lowercased country names and codes
    country_dict = {name.lower(): code for code, name in countries}
    
    for obj in queryset:
        try:
            field_value = getattr(obj, field_name, "").strip().lower()  # Handle empty values

            # Try exact match first
            if field_value == "united states":
                country_code = "US"
            elif field_value in country_dict:
                country_code = country_dict[field_value]
            else:
                # If no match is found, return the full country name
                country_code = field_value.title()  # Capitalize first letter of the country name

            # Add the country code or full name to the result if it's not already in the set
            if country_code not in seen:
                seen.add(country_code)
                result.append(country_code)
        except:
            print("An exception occurred")

    return result

@register.filter
def is_within_stay(hotel, itinerary_date):
    """Check if the itinerary date falls within the hotel's check-in and check-out dates"""
    check_in = hotel.start_date
    check_out = hotel.end_date
    itinerary_date = itinerary_date

    return check_in <= itinerary_date < check_out

@register.filter
def date_difference_plus_one(start_date, end_date):
    """
    Calculates the difference in days between two dates and adds 1.
    """
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        return "Invalid date"
    
    difference = abs((end_date - start_date).days)
    return difference + 1

@register.filter
def date_difference(start_date, end_date):
    """
    Calculates the difference in days between two dates and adds 1.
    """
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        return "Invalid date"
    
    difference = abs((end_date - start_date).days)
    return difference

@register.filter(name='append_item')
def append_item(value, arg):
    temp = list(value)
    temp.append(arg)
    return temp