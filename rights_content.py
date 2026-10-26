"""Content for the Know Your Rights screen.

To update the app when a law or amount changes, edit this file only.
General information only, not legal advice. Check labour.gov.za and ccma.org.za for the latest.
"""

CONTENT_UPDATED = "October 2026"

# National Minimum Wage: reviewed every year, usually from 1 March.
NMW_RATE = 30.23
NMW_FROM = "1 March 2026"

GROUPS = [
    ("The big picture", [
        {
            "title": "Your rights from day one",
            "law": "Constitution, section 23",
            "points": [
                "The Constitution gives every worker the right to fair labour practices, to join a trade union and to take part in lawful union activities.",
                "These rights apply from your first day, including during probation, and even if your agreement is only verbal.",
                "Most protections apply whether you work full-time, part-time, on a fixed-term contract, or through a labour broker. Some rules differ for people earning above a yearly 'earnings threshold' set by the Minister, so check labour.gov.za.",
                "Your employer cannot sign away your rights. A contract that offers less than the law requires does not override the law.",
            ],
        },
        {
            "title": "Which law covers what",
            "law": "The main labour laws",
            "points": [
                ("Basic Conditions of Employment Act (BCEA):", "contracts, hours, overtime, leave, notice and payslips."),
                ("National Minimum Wage Act:", "the lowest hourly pay an employer may pay."),
                ("Labour Relations Act (LRA):", "unions, fair dismissal, unfair treatment, retrenchment, and the CCMA."),
                ("Employment Equity Act (EEA):", "protection from unfair discrimination, including when applying for a job."),
                ("Unemployment Insurance Act (UIF):", "money if you lose your job or go on parental leave, or are ill."),
                ("Occupational Health and Safety Act (OHSA):", "a safe and healthy workplace."),
                ("Compensation for Occupational Injuries and Diseases Act (COIDA):", "help if you are hurt or made ill by your work."),
                ("Employment Services Act:", "protects job seekers from agencies that charge fees."),
                ("Skills Development Act:", "learnerships and workplace training."),
                ("Protected Disclosures Act:", "protects you if you report wrongdoing at work."),
            ],
        },
    ]),
    ("Getting hired", [
        {
            "title": "Applying for jobs safely",
            "law": "Employment Services Act, Employment Equity Act, POPIA",
            "points": [
                ("No fees:", "private employment agencies may not charge job seekers a fee. If anyone asks you to pay to get a job, treat it as a scam."),
                ("Fair hiring:", "you may not be turned down because of race, gender, pregnancy, age, disability, religion, sexual orientation, HIV status and similar grounds."),
                ("Medical tests:", "an employer may not make you take an HIV test without permission from the Labour Court, and other medical testing is restricted."),
                ("Your personal information:", "share your ID copy and details only with a real employer you are dealing with. Never share your bank PIN or an OTP. POPIA requires employers to protect your information."),
            ],
        },
        {
            "title": "Your contract and types of work",
            "law": "BCEA section 29, LRA sections 198 to 198D",
            "points": [
                ("Written terms:", "on your first day your employer must give you written details of your job: employer and employee names, job description, workplace, hours, pay, overtime rate, deductions, leave and notice period."),
                ("Read before you sign:", "never sign a blank or unclear document. Ask for your own copy."),
                ("Probation:", "must be a reasonable length. You should be told what is expected and be helped to improve."),
                ("Fixed-term contracts:", "if longer than three months, the employer generally needs a good reason for it. Without one you may be treated as a permanent employee. There are exceptions, such as certain training or work-experience programmes."),
                ("Part-time:", "if you work fewer than 24 hours a week you may not be treated worse than comparable full-time staff because of that."),
                ("Labour brokers (TES):", "after three months at a client, you must be treated no less favourably than the client's own staff doing the same job, unless there is a good reason."),
            ],
        },
        {
            "title": "Learnerships and internships",
            "law": "Skills Development Act",
            "points": [
                ("Learnerships:", "need a written agreement between you, the employer and a training provider. Ask whether it is registered with a SETA."),
                ("Allowance:", "learners must be paid at least the minimum learnership allowance set by the government, and you keep your normal workplace rights."),
                ("Internships:", "there is no single internship law, so get the duration, stipend and what you will learn in writing."),
                ("Red flag:", "any 'internship' or 'training' that asks you to pay, or that never pays or ends, needs checking."),
            ],
        },
    ]),
    ("Pay", [
        {
            "title": "Minimum wage and payslips",
            "law": "National Minimum Wage Act, BCEA",
            "points": [
                ("Minimum wage:", f"R{NMW_RATE:.2f} for each ordinary hour worked from {NMW_FROM}. It is reviewed every year, so check the current amount at labour.gov.za."),
                ("Who it covers:", "almost all workers, including domestic and farm workers. Learnerships and public works programmes have their own rates, and some sectors have higher minimums."),
                ("Payslip:", "you must get one every time you are paid, showing your pay, hours, deductions and UIF."),
                ("Paid on time:", "you must be paid weekly, every two weeks or monthly as agreed, on time and in full."),
            ],
        },
        {
            "title": "Deductions from your pay",
            "law": "BCEA section 34",
            "points": [
                "Your employer may only deduct money if the law, a court order or a collective agreement allows it, or if you agreed in writing to a specific deduction.",
                "For damage or loss, the employer must follow a fair process and give you a chance to explain, and the deduction may not be unreasonable or exceed 25% of your pay.",
                "Check your payslip every month. If something is deducted that you do not understand, ask in writing.",
            ],
        },
        {
            "title": "UIF (Unemployment Insurance)",
            "law": "Unemployment Insurance Act",
            "points": [
                ("How it works:", "you and your employer each pay 1% of your pay into the UIF. It should show on your payslip."),
                ("Who is covered:", "most employees who work more than 24 hours a month, including domestic workers."),
                ("What it pays:", "benefits when you lose your job, are ill, take parental or adoption leave, or when a breadwinner dies."),
                ("How to claim:", "ask your employer for a UI-19 form when your job ends. Claim through the Department of Employment and Labour or uFiling, ideally within 12 months."),
                ("If your employer does not pay:", "report it to the Department of Employment and Labour. Missing contributions are the employer's offence, but they can delay your claim, so act early."),
            ],
        },
    ]),
    ("Time at work", [
        {
            "title": "Hours, overtime and breaks",
            "law": "BCEA chapter 2",
            "points": [
                ("Ordinary hours:", "no more than 45 hours a week, and no more than 9 hours a day if you work five days a week or fewer (8 if more than five days)."),
                ("Overtime:", "needs your agreement, may not exceed 3 hours a day or 10 hours a week, and must be paid at least 1.5 times your normal wage (or agreed time off)."),
                ("Breaks:", "at least one hour after five hours of work, though this can be shortened to 30 minutes by agreement."),
                ("Rest:", "at least 12 hours between shifts and 36 hours in a row each week, normally including Sunday."),
                ("Sundays and public holidays:", "working them has higher pay. Ask HR how it is calculated."),
                ("Night work (6pm to 6am):", "must come with an allowance or shorter hours, and transport must be available."),
            ],
        },
        {
            "title": "Leave",
            "law": "BCEA chapter 3, Van Wyk v Minister of Employment and Labour (2025)",
            "points": [
                ("Annual leave:", "at least 21 consecutive days a year (about 1 day for every 17 days worked)."),
                ("Sick leave:", "30 days over a three-year cycle for a five-day week. In your first six months, 1 day for every 26 days worked. An employer may ask for a doctor's note if you are off for more than two days in a row, or twice in eight weeks."),
                ("Family responsibility leave:", "3 days a year for the birth or illness of your child, or the death of close family, if you have worked more than four months and work at least four days a week."),
                ("Parental leave:", "in October 2025 the Constitutional Court ruled that parents may share 4 months and 10 days of parental leave, including fathers, adoptive and commissioning parents. Employers do not have to pay it, but UIF benefits may apply. Parliament still has to update the law."),
                ("Pregnancy:", "you may not be dismissed or treated unfairly because you are pregnant."),
            ],
        },
    ]),
    ("Fairness and safety", [
        {
            "title": "Discrimination",
            "law": "Employment Equity Act",
            "points": [
                "You may not be treated unfairly because of race, gender, sex, pregnancy, marital status, family responsibility, ethnic or social origin, colour, sexual orientation, age, disability, religion, HIV status, conscience, belief, political opinion, culture, language or birth.",
                "This covers hiring, pay, promotion, training and dismissal.",
                "If it happens, you can refer the dispute to the CCMA within six months.",
            ],
        },
        {
            "title": "Harassment, bullying and gender-based violence",
            "law": "Code of Good Practice on Harassment, EEA, LRA",
            "points": [
                ("What counts:", "unwanted sexual attention, comments or touching, bullying, threats, and abuse because of who you are. It can happen in person, by message or online, and at work events."),
                ("What employers must do:", "have a harassment policy and a clear way to report, and act on complaints. They may be responsible if they ignore it."),
                ("What you can do:", "write down dates, times, what happened and who saw it. Keep messages and screenshots somewhere safe, not only on a work device. Report it to HR or a manager in writing."),
                ("If nothing is done:", "you can refer the matter to the CCMA. For sexual harassment and discrimination, the limit is six months."),
                ("Retaliation:", "you may not be punished for reporting. If you are in danger, contact the police or the GBV Command Centre on 0800 428 428."),
            ],
        },
        {
            "title": "Health, safety and injuries at work",
            "law": "OHSA, COIDA",
            "points": [
                ("A safe workplace:", "your employer must provide safe conditions, training and protective equipment where needed, at no cost to you."),
                ("Report hazards:", "tell your manager or health and safety representative. You may not be victimised for doing so."),
                ("Danger:", "you may remove yourself from an imminent danger and report it."),
                ("If you are hurt or made ill by work:", "tell your employer immediately, get medical help and keep a record. Employers must report work injuries and diseases to the Compensation Fund, which may pay medical costs and compensation."),
            ],
        },
        {
            "title": "Speaking up and unions",
            "law": "Protected Disclosures Act, LRA",
            "points": [
                ("Whistleblowing:", "if you report illegal or dangerous conduct in good faith and in the right way, you are protected from being punished or dismissed for it."),
                ("Unions:", "you have the right to join a union, and a union can represent you and help you with disputes."),
                ("Bargaining councils:", "in some sectors, a council sets minimum pay and conditions that may be better than the basics."),
                ("Strikes:", "are only protected if the legal steps are followed. Get advice from a union first."),
            ],
        },
    ]),
    ("Leaving a job", [
        {
            "title": "Resigning and notice",
            "law": "BCEA sections 37, 40 and 42",
            "points": [
                ("Notice period:", "one week if you have worked up to six months, two weeks from six months to a year, and four weeks after a year. A contract can ask for more but not less."),
                ("What you are owed:", "pay up to your last day, plus pay for leave you have not taken."),
                ("Certificate of service:", "on request your employer must give you a certificate with your job title, dates and pay."),
            ],
        },
        {
            "title": "Dismissal and retrenchment",
            "law": "Labour Relations Act",
            "points": [
                ("Fair dismissal:", "must be for a fair reason (misconduct, poor performance or the employer's operational needs) and follow a fair procedure. Small employers are covered too."),
                ("Automatically unfair:", "being dismissed because you are pregnant, joined a union, were discriminated against, reported wrongdoing or asserted your rights."),
                ("Retrenchment:", "the employer must consult you, and you are usually owed severance pay of at least one week's pay for every completed year of service."),
                ("Deadlines (count every day):", "30 days to refer an unfair dismissal to the CCMA, 90 days for an unfair labour practice (for example, an unfair demotion or suspension), and six months for discrimination."),
                ("Cost:", "the CCMA is free to use. It is not a place for lawyers at the first stage, so you can do it yourself."),
            ],
        },
    ]),
]

BEFORE_YOU_SIGN = [
    "I checked the company on its own website and the CIPC register.",
    "I did not pay anything to get the job.",
    "I have a written contract with my job title, pay, hours and notice period.",
    "My pay is at least the national minimum wage for my hours.",
    "The contract says what leave I get.",
    "UIF will be deducted and my payslip will show it.",
    "I know who to report to if something goes wrong.",
    "I kept a copy of everything I signed.",
]

IF_WRONG_STEPS = [
    ("Write it down", "Note the dates, times, names and what was said or done. Keep your contract, payslips and messages."),
    ("Raise it in writing", "Email HR or your manager so there is a record. Stay calm and factual."),
    ("Check the deadline", "Dismissal disputes must reach the CCMA within 30 days. Do not wait."),
    ("Go to the right place", "Pay, leave or UIF: the Department of Employment and Labour. Dismissal, unfair treatment or discrimination: the CCMA. A union or Legal Aid SA can help too."),
]

HELP_LINKS = [
    ("Department of Employment and Labour", "Pay, leave, UIF and unsafe workplaces. Visit a labour centre.", "https://www.labour.gov.za"),
    ("CCMA", "Dismissals, unfair treatment and discrimination. Free. Toll-free 0861 161 616.", "https://www.ccma.org.za"),
    ("Legal Aid South Africa", "Free legal help if you cannot afford a lawyer.", "https://legal-aid.co.za"),
    ("SAYouth.mobi", "Free support for young job seekers. Call 0800 727272.", "https://sayouth.mobi"),
]

SOURCES = [
    "Department of Employment and Labour (labour.gov.za): Basic Conditions of Employment Act, National Minimum Wage Act, Unemployment Insurance Act, Employment Equity Act and related guides.",
    "Commission for Conciliation, Mediation and Arbitration (ccma.org.za): dismissal and unfair labour practice referrals and time limits.",
    "Constitutional Court, Van Wyk v Minister of Employment and Labour (October 2025): shared parental leave.",
    "Always check the Department of Employment and Labour for the latest amounts, because they change.",
]