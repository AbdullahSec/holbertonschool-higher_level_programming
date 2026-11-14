"""Generate personalized invitation files from a template."""

def generate_invitations(template, attendees):
    """Create one invitation file for each attendee."""
    if not isinstance(template, str):
        print("Error: template must be a string.")
        return
    if not isinstance(attendees, list) or any(not isinstance(item, dict) for item in attendees):
        print("Error: attendees must be a list of dictionaries.")
        return
    if not template:
        print("Template is empty, no output files generated.")
        return
    if not attendees:
        print("No data provided, no output files generated.")
        return
    for number, attendee in enumerate(attendees, 1):
        result = template
        for key in ("name", "event_title", "event_date", "event_location"):
            value = attendee.get(key)
            result = result.replace("{" + key + "}", "N/A" if value is None else str(value))
        with open(f"output_{number}.txt", "w", encoding="utf-8") as output:
            output.write(result)
