# sites/services.py
def calculate_site_status(site):
    """
    Example rules – customize for your NOC
    """
    if not site.is_active:
        return "DOWN"

    # placeholder for real checks
    if site.phase == "P1":
        return "GREEN"
    else:
        return "PURPLE"
