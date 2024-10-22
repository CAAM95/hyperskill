import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)
parser.add_argument("--principal", type=float, default=0.0)
parser.add_argument("--payment", type=float, default=0.0)
parser.add_argument("--interest", type=float, default=0.0)
parser.add_argument("--periods", type=float, default=0.0)
args = parser.parse_args()
values = [args.type, args.principal, args.payment, args.interest, args.periods]

def calc_monthly_payment(principal, num_months):
    return principal / num_months

def calc_months_till_payed(principal, payment):
    return principal / payment

def convert_interest(interest):
    return (interest / 100) / 12

def month_to_years(periods):
    if periods % 12 == 0:
        years = int(periods // 12)
        remaining_months = 0
        return years
    else:
        years = int(periods // 12)
        remaining_months = math.ceil(periods % 12)
        return years, remaining_months

def calc_annuity_payment(principal, interest, periods):
    monthly_interest = convert_interest(interest)
    return math.ceil(principal * ((monthly_interest * (1 + monthly_interest)**periods) / ((1 + monthly_interest)**periods - 1)))

def calc_principal(payment, interest, periods):
    monthly_interest = convert_interest(interest)
    return payment / ((monthly_interest * (1 + monthly_interest)**periods) / ((1 + monthly_interest)**periods - 1))


def calc_periods(principal, payment, interest):
    return math.log((payment)/(payment -  convert_interest(interest) * principal), 1 + convert_interest(interest))


def get_length(values):
    val_len = len(values)
    val_count = 0
    for i in values:
        if i == False:
            val_count += 1
    val_len -= val_count
    return val_len

def is_negative_check(values):
    for i in range(1, len(values)):
        if values[i] < 0:
            return True
    return False

def calc_diff_payments(principal, num_periods, interest, period_number):
    conv_interest = convert_interest(interest)
    diff_payment = (principal / num_periods) + conv_interest * (principal - (principal * (period_number - 1)) / num_periods)
    return math.ceil(diff_payment)

def calc_overpayment(payments, principal):
    return math.ceil(payments - principal)

def report_diff_payments(interest, periods, principal):
    sum_payments = 0
    for i in range(1, int(periods) + 1):
        diff_payment = calc_diff_payments(principal, periods, interest, i)
        sum_payments += diff_payment
        print('Month {}: payment is {}'.format(i, diff_payment))

    print("Overpayment = {}".format(calc_overpayment(sum_payments, args.principal)))

def report_annuity_payments(principal, interest, periods):
    loan_monthly_payment = calc_annuity_payment(principal, interest, periods)
    total_payments = loan_monthly_payment * periods
    print('Your annuity payment = {}!'.format(loan_monthly_payment))
    print('Overpayment = {}'.format(calc_overpayment(total_payments, principal)))

if get_length(values) < 4:
    print("Incorrect parameters - fewer than 4")
elif is_negative_check(values):
    print("Incorrect parameters - negative values")
elif args.type != "diff" and args.type != "annuity":
    print("Incorrect parameters - type must be diff or annuity")
elif args.type == "diff" and args.principal and args.payment:
    print("Incorrect parameters - diff cannot have principal and payment")
elif args.type == "annuity" and args.interest == False:
    print("Incorrect parameters - annuity must have interest")

def report_loan_principle(payment, periods, interest):
    loan_principal = math.floor(calc_principal(payment, interest, periods))
    total_payments = payment * periods
    print('Your loan principal = {}!'.format(loan_principal))
    print('Overpayment = {}'.format(calc_overpayment(total_payments, loan_principal)))

def report_loan_repayment(principal, payment, interest):
    years, months = month_to_years(calc_periods(principal, payment, interest))

    if months == 12:
        years += 1
        months = 0

    total_payments = years * 12 * payment

    if months > 1:
        print('It will take {} years and {} months to repay this loan!'.format(years, months))
    elif months == 1:
        print('It will take {} years and {} month to repay this loan!'.format(years, months))
    else:
        print('It will take {} years to repay this loan!'.format(years))

    print('Overpayment = {}'.format(calc_overpayment(total_payments, principal)))

if args.type == "diff" and args.interest and args.periods and args.principal:
    report_diff_payments(args.interest, args.periods, args.principal)
elif args.type == "annuity" and args.principal and args.interest and args.periods:
    report_annuity_payments(args.principal, args.interest, args.periods)
elif args.principal and args.payment and args.interest:
    report_loan_repayment(args.principal, args.payment, args.interest)
elif args.payment and args.interest and args.periods:
    report_loan_principle(args.payment, args.periods, args.interest)
