"""Plain functions for the contract checker and the payslip checker.
They return results as data, and the Tools screen shows them.
"""
import re

# ---------- Contract checker ----------
# (name of the term, pattern that suggests it is mentioned)
CONTRACT_TERMS = [
    ("Job title or duties", r"job title|position|duties|job description|\brole\b"),
    ("Pay (salary or hourly rate)", r"salary|remuneration|wage|rate of pay|per month|per hour"),
    ("Working hours", r"hours of work|working hours|per week|\bhours\b"),
    ("Overtime", r"overtime"),
    ("Leave", r"\bleave\b"),
    ("Notice period", r"notice"),
    ("Place of work", r"place of work|workplace|location|premises"),
    ("Start date", r"commenc|start date|effective date"),
    ("Deductions", r"deduction"),
    ("UIF", r"\buif\b|unemployment insurance"),
]

# (pattern, warning message)
CONTRACT_WARNINGS = [
    (r"non-?refundable|\bdeposit\b|pay.{0,25}\bfee\b",
     "The contract mentions you paying money. Ask exactly what for, and why."),
    (r"waive|waiver of (your )?rights|no (annual |sick )?leave",
     "It seems to remove a right (such as leave). A contract cannot take away your legal rights."),
    (r"forfeit",
     "It mentions you forfeiting money or benefits. Ask for the exact conditions."),
    (r"unpaid (trial|work|probation|internship)",
     "It mentions unpaid work. Check this against the minimum wage rules."),
    (r"terminat\w*.{0,40}without (notice|reason)",
     "It lets the employer end the job without notice or reason. Dismissal still has to be fair under the law."),
]


def check_contract(text):
    """Return {'found': [...], 'missing': [...], 'warnings': [...]} for the pasted contract."""
    lower = (text or "").lower()
    found = []
    missing = []
    for name, pattern in CONTRACT_TERMS:
        if re.search(pattern, lower):
            found.append(name)
        else:
            missing.append(name)
    warnings = []
    for pattern, message in CONTRACT_WARNINGS:
        if re.search(pattern, lower):
            warnings.append(message)
    return {"found": found, "missing": missing, "warnings": warnings}


# ---------- Payslip checker ----------
def check_payslip(gross, uif, paye, other, net):
    """Check a payslip. Returns a list of (level, message) where level is
    'good', 'info', 'warn' or 'bad'. Raises ValueError for impossible numbers."""
    for amount in (gross, uif, paye, other, net):
        if amount < 0:
            raise ValueError("negative amount")
    if gross <= 0:
        raise ValueError("gross pay must be above zero")

    results = []
    total_deductions = uif + paye + other

    expected_net = gross - total_deductions
    if abs(expected_net - net) > 1:
        results.append(("warn", f"The numbers do not add up. Gross pay minus deductions is R{expected_net:,.2f}, "
                                f"but you entered R{net:,.2f} as net pay. Ask for an explanation and a corrected payslip."))
    else:
        results.append(("good", "Gross pay minus deductions matches your net pay."))

    if uif == 0:
        results.append(("warn", "No UIF is deducted. Most employees who work more than 24 hours a month must be registered "
                                "for UIF, so ask HR why."))
    else:
        expected_uif = gross * 0.01
        if abs(uif - expected_uif) > max(2, expected_uif * 0.15):
            results.append(("info", f"UIF is usually about 1% of pay (about R{expected_uif:,.2f} here, and capped for high earners). "
                                    f"Yours is R{uif:,.2f}. Ask how it was calculated."))
        else:
            results.append(("good", "The UIF deduction is close to the usual 1%."))

    if other / gross > 0.10:
        results.append(("warn", "'Other' deductions are more than 10% of your pay. Ask for each deduction in writing, "
                                "because an employer may only deduct money the law allows or that you agreed to in writing."))

    share = total_deductions / gross
    if share > 0.25:
        results.append(("info", f"Deductions take {share * 100:.0f}% of your gross pay. Tax (PAYE) and UIF are normal, "
                                "but check what makes up the rest."))

    if paye == 0 and gross > 8000:
        results.append(("info", "No tax (PAYE) is deducted. Tax depends on your income and tax number, so ask HR to explain."))

    results.append(("info", "This checker looks for obvious problems only. It cannot confirm your tax is correct."))
    return results
