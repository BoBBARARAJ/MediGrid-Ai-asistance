def check_warnings(medicines):
    warnings = []
    for medicine in medicines:
        name = medicine["name"].lower()
        if "warfarin" in name:
            warnings.append("Warfarin may have important drug interactions.")
        if "insulin" in name:
            warnings.append("Insulin can cause low blood sugar.")
        if "aspirin" in name:
            warnings.append("Aspirin may increase bleeding risk.")
    return warnings
