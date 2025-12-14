def calculate_emi(principal, annual_rate, months):
    if annual_rate == 0:
        return principal / months

    r = annual_rate / (12 * 100)
    emi = (principal * r * (1 + r) ** months) / ((1 + r) ** months - 1)
    return round(emi, 2)
