import re

def normalize_ghana_phone(phone: str) -> str | None:
    """
    Normalize Ghana phone numbers to 233XXXXXXXXX format.
    Returns None if invalid.
    """

    if not phone:
        return None

    # Remove spaces, hyphens, brackets
    phone = re.sub(r"[^\d+]", "", phone)

    # Handle +233XXXXXXXXX
    if phone.startswith("+233"):
        phone = phone[1:]

    # Handle 233XXXXXXXXX
    if phone.startswith("233") and len(phone) == 12:
        return phone

    # Handle 0XXXXXXXXX
    if phone.startswith("0") and len(phone) == 10:
        return "233" + phone[1:]

    # Handle XXXXXXXXX (missing leading 0)
    if len(phone) == 9:
        return "233" + phone

    return None