


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

    weighted_pv = 0

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



def modified_duration(face, coupon_rate, maturity, ytm, frequency):
    # This function calculates the modified duration of a bond.
    # The modified duration is calculated as the Macaulay duration divided by (1 + (ytm / frequency)).
    
    macaulay_dur = macaulay_duration(face, coupon_rate, maturity, ytm, frequency)
    mod_duration = macaulay_dur / (1 + (ytm / frequency))
    
    return mod_duration

mod_dur = modified_duration(1000, 0.05, 3, 0.05, 2)
print(mod_dur)


def dv01(face, coupon_rate, maturity, ytm, frequency):

    # This function calculates the DV01 (Dollar Value of 01) of a bond.
    # DV01 is the change in the price of a bond for a 1 basis point change in yield.
    
    original_price = bond_price(face, coupon_rate, maturity, ytm, frequency)
    
    # Calculate the price of the bond with a 1 basis point increase in yield
    new_ytm = ytm + 0.0001
    new_price = bond_price(face, coupon_rate, maturity, new_ytm, frequency)
    
    dv01_value = original_price - new_price
    
    return dv01_value

dv01_val = dv01(1000, 0.05, 3, 0.05, 2)
print(dv01_val)


def dv01_duration(face, coupon_rate, maturity, ytm, frequency):
    # This function calculates the DV01 using the modified duration of a bond.
    # DV01 can also be approximated as the product of the modified duration and the price of the bond, divided by 10000.
    
    mod_dur = modified_duration(face, coupon_rate, maturity, ytm, frequency)
    price = bond_price(face, coupon_rate, maturity, ytm, frequency)
    
    dv01_value = (mod_dur * price) / 10000
    
    return dv01_value 

dv01_duration_val = dv01_duration(1000, 0.05, 3, 0.05, 2)
print(dv01_duration_val)
