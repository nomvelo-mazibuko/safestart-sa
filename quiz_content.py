"""Questions for the Rights quiz. 'answer' is the position (starting at 0) of the correct option."""
import rights_content

QUESTIONS = [
    {"q": "What is the normal maximum number of ordinary working hours per week?",
     "options": ["40", "45", "50", "60"], "answer": 1,
     "why": "The BCEA sets ordinary hours at no more than 45 a week."},
    {"q": "How much notice must you give after working for more than a year?",
     "options": ["1 week", "2 weeks", "4 weeks", "3 months"], "answer": 2,
     "why": "By law it is 1 week up to 6 months, 2 weeks up to a year, and 4 weeks after a year. A contract may ask for more but not less."},
    {"q": "What is the lowest overtime pay rate?",
     "options": ["The normal rate", "1.5 times the normal rate", "Double the normal rate", "There is no minimum"], "answer": 1,
     "why": "Overtime must be paid at least 1.5 times your normal wage, or you can agree to paid time off."},
    {"q": "A recruiter says you must pay R300 to secure the job. What should you do?",
     "options": ["Pay quickly before it is gone", "Pay half now", "Treat it as a scam and walk away", "Ask for a discount"], "answer": 2,
     "why": "Private employment agencies may not charge job seekers, and real employers do not sell jobs."},
    {"q": "How long do you generally have to refer an unfair dismissal to the CCMA?",
     "options": ["7 days", "30 days", "6 months", "2 years"], "answer": 1,
     "why": "You usually have 30 days from the dismissal, so act quickly. Discrimination disputes have a longer limit."},
    {"q": "How much of your pay does each of you (you and your employer) normally pay into UIF?",
     "options": ["0.1%", "1%", "5%", "10%"], "answer": 1,
     "why": "Employees and employers each contribute 1%."},
    {"q": f"What is the national minimum wage per ordinary hour from {rights_content.NMW_FROM}?",
     "options": ["R20.00", f"R{rights_content.NMW_RATE:.2f}", "R45.00", "R60.00"], "answer": 1,
     "why": "The minimum wage is reviewed every year, so check labour.gov.za for the current amount."},
    {"q": "Your employer asks for your bank PIN and an OTP to 'set up your salary'. What do you do?",
     "options": ["Share them privately", "Share only the OTP", "Never share them", "Share them if they are polite"], "answer": 2,
     "why": "A real employer never needs your PIN or OTP. You only give banking account details, never these codes."},
]
PASS_MARK = 6  
