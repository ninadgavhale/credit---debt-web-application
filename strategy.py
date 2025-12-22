def snowball(debts):
    return sorted(debts, key=lambda d: d["amount"])

def avalanche(debts):
    return sorted(debts, key=lambda d: d["interest"], reverse=True)
