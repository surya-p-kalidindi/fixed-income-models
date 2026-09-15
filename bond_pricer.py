


def bond_price(face, coupon_rate, maturity, ytm, frequency):
    periods = int(maturity * frequency)
    coupon_payment = face*coupon_rate/frequency
    periodic_yield = ytm/frequency
    PV = 0

    for period in range(1,periods+1):
      cash_flow = coupon_payment
      if period == periods:
           cash_flow = face + coupon_payment
        
      PV += cash_flow /(1+periodic_yield) ** period

    return PV

price = bond_price(1000, 0.05, 3, 0.05, 2)
print(price)


def yield_to_maturity(face, annual_coupon_rate, maturity, market_price, frequency):

    lower_yield = 0.00
    upper_yield = 0.20

    for iteration in range(100):
        trial_yield = (lower_yield+upper_yield)/2
        caluculated_price = bond_price(face,annual_coupon_rate,maturity,trial_yield,frequency)

        if caluculated_price > market_price:
            lower_yield = trial_yield
        else:
             upper_yield = trial_yield

    return trial_yield

ytm = yield_to_maturity(1000, 0.05, 3, 1000, 2)
print(f"{ytm:.4%}")


def macaulay_duration(face, coupon_rate, maturity, ytm, frequency):
    periods = int(maturity * frequency)

    pv = 0

    weignted_pv = 0

    coupon_payment = face * coupon_rate / frequency

    periodic_yield = ytm / frequency

    for period in range(1, periods + 1):
        cash_flow = coupon_payment

        time_in_years = period/frequency

        if period == periods:
           cash_flow = face + coupon_payment

        pv += cash_flow / (1 + periodic_yield) ** period

        weighted_pv += cash_flow / (1 + periodic_yield) ** period * time_in_years
    
    duration = weighted_pv/pv

    return duration

dur = macaulay_duration(1000, 0.05, 3, 0.05, 2)
print(dur)