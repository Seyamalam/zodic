#!/usr/bin/env python3
"""
Comprehensive Date and DateTime Validation Examples for Zodic v0.2.0

This file demonstrates all date/datetime validation features including:
- Date object validation
- DateTime object validation
- String parsing (ISO, common formats)
- Range validation (min/max dates)
- Timezone handling
- Real-world scenarios
"""

import zodic as z
from datetime import date, datetime, timedelta


def basic_date_validation():
    """Demonstrate basic date validation."""
    print("=== Basic Date Validation ===")
    
    # Simple date validation
    date_schema = z.date()
    
    # Date objects
    today = date.today()
    print(f"Today: {date_schema.parse(today)}")
    
    # Specific dates
    birthday = date(1990, 5, 15)
    print(f"Birthday: {date_schema.parse(birthday)}")
    
    # DateTime to date conversion
    now = datetime.now()
    print(f"DateTime to date: {date_schema.parse(now)}")
    
    print()


def date_string_parsing():
    """Demonstrate date string parsing."""
    print("=== Date String Parsing ===")
    
    date_schema = z.date()
    
    # ISO format (YYYY-MM-DD)
    iso_dates = [
        "2024-12-19",
        "2023-01-01",
        "2025-12-31"
    ]
    
    for date_str in iso_dates:
        parsed = date_schema.parse(date_str)
        print(f"ISO format '{date_str}': {parsed}")
    
    # Common formats
    common_formats = [
        "12/19/2024",  # MM/DD/YYYY
        "19/12/2024",  # DD/MM/YYYY
        "01/01/2025",  # MM/DD/YYYY
        "31/12/2025"   # DD/MM/YYYY
    ]
    
    for date_str in common_formats:
        try:
            parsed = date_schema.parse(date_str)
            print(f"Common format '{date_str}': {parsed}")
        except z.ZodError as e:
            print(f"❌ Failed to parse '{date_str}': {e}")
    
    print()


def date_range_validation():
    """Demonstrate date range validation."""
    print("=== Date Range Validation ===")
    
    # Date range for events
    event_date = (z.date()
                 .min(date(2024, 1, 1))
                 .max(date(2024, 12, 31)))
    
    print(f"Valid event date: {event_date.parse('2024-06-15')}")
    
    # Birth date validation (reasonable human age)
    birth_date = (z.date()
                 .min(date(1900, 1, 1))
                 .max(date.today()))
    
    print(f"Valid birth date: {birth_date.parse('1990-05-15')}")
    
    # Future date validation
    future_date = z.date().min(date.today())
    tomorrow = date.today() + timedelta(days=1)
    print(f"Future date: {future_date.parse(tomorrow)}")
    
    # Historical date validation
    historical_date = z.date().max(date(2000, 1, 1))
    print(f"Historical date: {historical_date.parse('1995-07-20')}")
    
    # Test invalid ranges
    print("\nInvalid date ranges:")
    try:
        event_date.parse("2023-12-31")  # Before range
    except z.ZodError as e:
        print(f"❌ Before range: {e}")
    
    try:
        birth_date.parse("2030-01-01")  # Future birth date
    except z.ZodError as e:
        print(f"❌ Future birth date: {e}")
    
    print()


def basic_datetime_validation():
    """Demonstrate basic datetime validation."""
    print("=== Basic DateTime Validation ===")
    
    # Simple datetime validation
    datetime_schema = z.datetime()
    
    # DateTime objects
    now = datetime.now()
    print(f"Current time: {datetime_schema.parse(now)}")
    
    # Specific datetime
    meeting_time = datetime(2024, 12, 19, 14, 30, 0)
    print(f"Meeting time: {datetime_schema.parse(meeting_time)}")
    
    print()


def datetime_string_parsing():
    """Demonstrate datetime string parsing."""
    print("=== DateTime String Parsing ===")
    
    datetime_schema = z.datetime()
    
    # ISO format datetime strings
    iso_datetimes = [
        "2024-12-19T14:30:00",
        "2023-01-01T00:00:00",
        "2024-06-15T12:45:30"
    ]
    
    for dt_str in iso_datetimes:
        parsed = datetime_schema.parse(dt_str)
        print(f"ISO datetime '{dt_str}': {parsed}")
    
    # Timezone-aware strings (converted to naive)
    timezone_datetimes = [
        "2024-12-19T14:30:00Z",
        "2024-12-19T14:30:00+00:00",
        "2024-12-19T14:30:00-05:00"
    ]
    
    for dt_str in timezone_datetimes:
        parsed = datetime_schema.parse(dt_str)
        print(f"Timezone datetime '{dt_str}': {parsed} (converted to naive)")
    
    # Common datetime formats
    common_datetimes = [
        "2024-12-19 14:30:00",
        "12/19/2024 14:30:00"
    ]
    
    for dt_str in common_datetimes:
        try:
            parsed = datetime_schema.parse(dt_str)
            print(f"Common datetime '{dt_str}': {parsed}")
        except z.ZodError as e:
            print(f"❌ Failed to parse '{dt_str}': {e}")
    
    print()


def datetime_range_validation():
    """Demonstrate datetime range validation."""
    print("=== DateTime Range Validation ===")
    
    # Business hours validation
    business_start = datetime(2024, 1, 1, 9, 0, 0)
    business_end = datetime(2024, 12, 31, 17, 0, 0)
    
    business_datetime = (z.datetime()
                        .min(business_start)
                        .max(business_end))
    
    meeting_time = datetime(2024, 6, 15, 14, 30, 0)
    print(f"Business meeting: {business_datetime.parse(meeting_time)}")
    
    # Event scheduling (next 30 days)
    now = datetime.now()
    future_limit = now + timedelta(days=30)
    
    event_datetime = (z.datetime()
                     .min(now)
                     .max(future_limit))
    
    next_week = now + timedelta(days=7)
    print(f"Event next week: {event_datetime.parse(next_week)}")
    
    # Log entry validation (past only)
    log_datetime = z.datetime().max(datetime.now())
    yesterday = datetime.now() - timedelta(days=1)
    print(f"Log entry: {log_datetime.parse(yesterday)}")
    
    print()


def real_world_date_examples():
    """Demonstrate real-world date validation scenarios."""
    print("=== Real-World Date Examples ===")
    
    # User registration (must be 18+)
    def calculate_age(birth_date):
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    adult_birth_date = z.date().refine(
        lambda d: calculate_age(d) >= 18,
        "Must be 18 years or older"
    )
    
    adult_birthday = date(2000, 1, 1)
    print(f"Adult birth date: {adult_birth_date.parse(adult_birthday)}")
    
    # Credit card expiration (future dates only)
    card_expiry = z.date().min(date.today())
    future_expiry = date(2026, 12, 31)
    print(f"Card expiry: {card_expiry.parse(future_expiry)}")
    
    # Project deadline (within next year)
    project_deadline = (z.date()
                       .min(date.today())
                       .max(date.today() + timedelta(days=365)))
    
    deadline = date.today() + timedelta(days=90)
    print(f"Project deadline: {project_deadline.parse(deadline)}")
    
    # Appointment scheduling
    def is_weekday(d):
        return d.weekday() < 5  # Monday=0, Sunday=6
    
    weekday_appointment = z.date().refine(
        is_weekday,
        "Appointments only available on weekdays"
    )
    
    # Find next Monday
    today = date.today()
    days_ahead = 0 - today.weekday()  # Monday is 0
    if days_ahead <= 0:
        days_ahead += 7
    next_monday = today + timedelta(days_ahead)
    
    print(f"Weekday appointment: {weekday_appointment.parse(next_monday)}")
    
    print()


def real_world_datetime_examples():
    """Demonstrate real-world datetime validation scenarios."""
    print("=== Real-World DateTime Examples ===")
    
    # Meeting scheduling (business hours only)
    def is_business_hours(dt):
        return 9 <= dt.hour <= 17 and dt.weekday() < 5
    
    business_meeting = z.datetime().refine(
        is_business_hours,
        "Meetings only during business hours (9 AM - 5 PM, weekdays)"
    )
    
    # Next business day at 2 PM
    today = datetime.now()
    days_ahead = 1
    while (today + timedelta(days=days_ahead)).weekday() >= 5:
        days_ahead += 1
    
    next_business_day = (today + timedelta(days=days_ahead)).replace(hour=14, minute=0, second=0, microsecond=0)
    print(f"Business meeting: {business_meeting.parse(next_business_day)}")
    
    # Server maintenance window (off-hours)
    def is_maintenance_window(dt):
        # Maintenance between 2 AM and 4 AM
        return 2 <= dt.hour <= 4
    
    maintenance_time = z.datetime().refine(
        is_maintenance_window,
        "Maintenance only between 2 AM and 4 AM"
    )
    
    maintenance_slot = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
    print(f"Maintenance window: {maintenance_time.parse(maintenance_slot)}")
    
    # Event registration deadline
    event_date = datetime(2024, 12, 25, 18, 0, 0)
    registration_deadline = z.datetime().max(event_date - timedelta(days=7))
    
    early_registration = event_date - timedelta(days=14)
    print(f"Early registration: {registration_deadline.parse(early_registration)}")
    
    # Log timestamp validation (recent entries only)
    recent_log = z.datetime().min(datetime.now() - timedelta(hours=24))
    recent_entry = datetime.now() - timedelta(hours=2)
    print(f"Recent log entry: {recent_log.parse(recent_entry)}")
    
    print()


def date_transformations():
    """Demonstrate date transformations."""
    print("=== Date Transformations ===")
    
    # Convert to start of month
    month_start = z.date().transform(lambda d: d.replace(day=1))
    print(f"Month start: {month_start.parse('2024-12-19')}")
    
    # Convert to end of year
    year_end = z.date().transform(lambda d: d.replace(month=12, day=31))
    print(f"Year end: {year_end.parse('2024-06-15')}")
    
    # Add business days
    def add_business_days(d, days=5):
        current = d
        added = 0
        while added < days:
            current += timedelta(days=1)
            if current.weekday() < 5:  # Weekday
                added += 1
        return current
    
    business_days_later = z.date().transform(lambda d: add_business_days(d, 5))
    print(f"5 business days later: {business_days_later.parse(date.today())}")
    
    print()


def datetime_transformations():
    """Demonstrate datetime transformations."""
    print("=== DateTime Transformations ===")
    
    # Round to nearest hour
    round_hour = z.datetime().transform(
        lambda dt: dt.replace(minute=0, second=0, microsecond=0)
    )
    print(f"Rounded to hour: {round_hour.parse('2024-12-19T14:45:30')}")
    
    # Convert to UTC (simplified - just for demo)
    to_utc = z.datetime().transform(
        lambda dt: dt.replace(tzinfo=None)  # In real app, would handle timezone conversion
    )
    print(f"To UTC: {to_utc.parse('2024-12-19T14:30:00')}")
    
    # Start of day
    start_of_day = z.datetime().transform(
        lambda dt: dt.replace(hour=0, minute=0, second=0, microsecond=0)
    )
    print(f"Start of day: {start_of_day.parse('2024-12-19T14:30:00')}")
    
    # End of day
    end_of_day = z.datetime().transform(
        lambda dt: dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    )
    print(f"End of day: {end_of_day.parse('2024-12-19T14:30:00')}")
    
    print()


def error_handling_examples():
    """Demonstrate date/datetime validation error handling."""
    print("=== Date/DateTime Error Handling ===")
    
    # Complex date schema
    complex_date = (z.date()
                   .min(date(2024, 1, 1))
                   .max(date(2024, 12, 31))
                   .refine(lambda d: d.weekday() < 5, "Must be a weekday"))
    
    date_test_cases = [
        "2023-12-31",  # Before range
        "2025-01-01",  # After range
        "2024-06-15",  # Saturday (weekend)
        "2024-06-17",  # Monday (valid)
    ]
    
    for test in date_test_cases:
        result = complex_date.safe_parse(test)
        if result["success"]:
            print(f"✅ Valid date: {result['data']}")
        else:
            print(f"❌ Invalid date '{test}': {result['error']}")
    
    # Invalid date strings
    invalid_dates = [
        "not-a-date",
        "2024-13-01",  # Invalid month
        "2024-02-30",  # Invalid day
        "2023-02-29",  # Not a leap year
    ]
    
    date_schema = z.date()
    for invalid in invalid_dates:
        result = date_schema.safe_parse(invalid)
        if not result["success"]:
            print(f"❌ Invalid date string '{invalid}': {result['error']}")
    
    print()


def main():
    """Run all date/datetime validation examples."""
    print("Zodic Date and DateTime Validation Examples")
    print("=" * 60)
    
    basic_date_validation()
    date_string_parsing()
    date_range_validation()
    basic_datetime_validation()
    datetime_string_parsing()
    datetime_range_validation()
    real_world_date_examples()
    real_world_datetime_examples()
    date_transformations()
    datetime_transformations()
    error_handling_examples()
    
    print("=" * 60)
    print("All date/datetime validation examples completed!")


if __name__ == "__main__":
    main()