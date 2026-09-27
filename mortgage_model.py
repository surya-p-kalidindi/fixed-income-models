# 1. mortgage_schedule function definition

def mortgage_schedule(principal, annual_rate, years):
    frequency = 12
    months = int(years * frequency)
    monthly_rate = annual_rate / frequency

    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

    schedule = []
    balance = principal

    for month in range(1, months + 1):
        beginning_balance = balance
        scheduled_interest = beginning_balance * monthly_rate
        scheduled_principal = payment - scheduled_interest
        ending_balance = beginning_balance - scheduled_principal
        balance = ending_balance

        schedule.append({
            "month": month,
            "beginning_balance": beginning_balance,
            "scheduled_interest": scheduled_interest,
            "scheduled_principal": scheduled_principal,
            "ending_balance": ending_balance,
        })

    return schedule


def mortgage_schedule_with_prepayment(
    principal,
    annual_rate,
    years,
    cpr
):
    frequency = 12
    smm = 1 - (1 - cpr) ** (1 / frequency)

    original_schedule = mortgage_schedule(
        principal,
        annual_rate,
        years
    )

    schedule = []
    survivor_factor = 1.0

    for original_row in original_schedule:
        month = original_row["month"]

        beginning_balance = (
            original_row["beginning_balance"]
            * survivor_factor
        )

        scheduled_interest = (
            original_row["scheduled_interest"]
            * survivor_factor
        )

        scheduled_principal = (
            original_row["scheduled_principal"]
            * survivor_factor
        )

        balance_after_scheduled_principal = (
            original_row["ending_balance"]
            * survivor_factor
        )

        prepayment = (
            balance_after_scheduled_principal
            * smm
        )

        ending_balance = (
            balance_after_scheduled_principal
            - prepayment
        )

        if abs(ending_balance) < 0.01:
            ending_balance = 0.0

        schedule.append({
            "month": month,
            "survivor_factor": survivor_factor,
            "beginning_balance": beginning_balance,
            "scheduled_interest": scheduled_interest,
            "scheduled_principal": scheduled_principal,
            "balance_after_scheduled_principal":
                balance_after_scheduled_principal,
            "prepayment": prepayment,
            "ending_balance": ending_balance,
        })

        survivor_factor *= (1 - smm)

    return schedule

base_schedule = mortgage_schedule(
    principal=400000,
    annual_rate=0.06,
    years=30
)

zero_cpr_schedule = mortgage_schedule_with_prepayment(
    principal=400000,
    annual_rate=0.06,
    years=30,
    cpr=0.0
)

assert len(zero_cpr_schedule) == len(base_schedule)

fields_to_compare = [
    "beginning_balance",
    "scheduled_interest",
    "scheduled_principal",
    "ending_balance",
]

assert all(
    abs(base_row[field] - cpr_row[field]) < 0.01
    for base_row, cpr_row in zip(base_schedule, zero_cpr_schedule)
    for field in fields_to_compare
)

# 2. Sprint 2 validation checks
schedule = mortgage_schedule(
    principal=400000,
    annual_rate=0.06,
    years=30
)


prepayment_schedule = mortgage_schedule_with_prepayment(
    principal=400000,
    annual_rate=0.06,
    years=30,
    cpr=0.06
)

total_principal_with_prepayment = sum(
    row["scheduled_principal"] + row["prepayment"]
    for row in prepayment_schedule
)

assert abs(
    total_principal_with_prepayment - 400000
) < 0.01

assert abs(
    prepayment_schedule[-1]["ending_balance"]
) < 0.01

print("CPR and SMM prepayment assertions passed")

# Ending balance is zero
assert abs(schedule[-1]["ending_balance"]) < 0.01

# Total principal equals the original balance
total_principal = sum(
    row["scheduled_principal"] for row in schedule
)

assert abs(total_principal - 400000) < 0.01

# Total cash flow equals fixed payment × number of months
monthly_payment = (
    schedule[0]["scheduled_interest"]
    + schedule[0]["scheduled_principal"]
)

total_interest = sum(
    row["scheduled_interest"] for row in schedule
)

total_cash_flow = total_interest + total_principal

assert abs(
    total_cash_flow - monthly_payment * len(schedule)
) < 0.01

print("Level-pay mortgage assertions passed")