


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


def convexity_value(face, coupon_rate, maturity, ytm, frequency):
 
    
    periods = int(maturity * frequency)
    coupon_payment = face * coupon_rate / frequency
    yield_payment_period = ytm / frequency

    price = bond_price(face, coupon_rate, maturity, ytm, frequency)
    
    convexity_sum = 0

    for period in range(1, periods + 1):
        cash_flow = coupon_payment
        if period == periods:
            cash_flow = face + coupon_payment
        
        pv_cash_flow = cash_flow / (1 + yield_payment_period) ** period
        curvature_weight = period * (period + 1)
        convexity_sum += pv_cash_flow * curvature_weight/ ((1 + yield_payment_period) ** 2 * frequency ** 2)
    bond_convexity = convexity_sum / price

    return bond_convexity
print(convexity_value(1000, 0.05, 3, 0.05, 2))

price_up = bond_price(1000, 0.05, 3, 0.0501, 2)
price_down = bond_price(1000, 0.05, 3, 0.0499, 2)

price_0 = bond_price(1000, 0.05, 3, 0.05, 2)

convexity_numerator = (price_down + price_up - 2 * price_0) 


convexity_approx = convexity_numerator / (price_0 * 0.0001 ** 2)
print(convexity_approx)



shock_bp = 100

shock_decimal = shock_bp / 10000

ytm= 0.05

shocked_ytm = ytm + shock_decimal

base_price = bond_price(1000, 0.05, 3, ytm, 2)

shocked_price = bond_price(1000, 0.05, 3, shocked_ytm, 2)

price_change = shocked_price - base_price

print(f"Price change for a {shock_bp} basis point increase in yield: {price_change:.2f}")


spot_rates = [0.045, 0.046, 0.047, 0.048, 0.049, 0.050]  # Example spot rates for periods 1 to 6


def bond_price_curve(face, coupon_rate, maturity, spot_rates, frequency):
    periods = int(maturity * frequency)
    coupon_payment = face * coupon_rate / frequency
    price = 0

    if len(spot_rates) != periods:
        raise ValueError("spot_rates must have one rate per payment period")

    for period in range(1, periods + 1):
        cash_flow = coupon_payment
        if period == periods:
            cash_flow = face + coupon_payment
        spot_rate = spot_rates[period - 1]

        pv_cash_flow = cash_flow / (1 + spot_rate / frequency) ** period
        price += pv_cash_flow

    return price

flat_rates = [0.05] * 6  # Flat yield curve at 5% for all periods
price_flat_curve = bond_price_curve(1000, 0.05, 3, flat_rates, 2)
print(f"Price with flat yield curve: {price_flat_curve:.2f}")

spot_rates = [0.045, 0.046, 0.047, 0.048, 0.049, 0.050]
price_spot_curve = bond_price_curve(1000, 0.05, 3, spot_rates, 2)
print(f"Price with spot yield curve: {price_spot_curve:.2f}")

shocked_spot_rates = [0.055,0.056,0.057,0.058,0.059,0.060]
price_up = bond_price_curve(1000, 0.05, 3, shocked_spot_rates, 2)
print(f"Price with shocked yield curve: {price_up:.2f}")
curve_price_change = price_up - price_spot_curve
print(f"Price change due to shocked yield curve: {curve_price_change:.2f}")


shocked_spot_rates = [0.035,0.036,0.037,0.038,0.039,0.040]
price_down = bond_price_curve(1000, 0.05, 3, shocked_spot_rates, 2)
print(f"Price with shocked yield curve: {price_down:.2f}")
curve_price_change = price_down - price_spot_curve
print(f"Price change due to shocked yield curve: {curve_price_change:.2f}")

effective_duration = (price_down - price_up) / (price_spot_curve * 0.02)
print(f"Effective duration based on shocked yield curve: {effective_duration:.6f}")

curvature_numerator = (price_down + price_up - 2 * price_spot_curve)
effective_convexity = curvature_numerator / (price_spot_curve * 0.01 ** 2)
print(f"Effective convexity based on shocked yield curve: {effective_convexity:.6f}")