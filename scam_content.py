"""Text for the scam-awareness sections. Edit here to change wording."""

# Teaching examples written for this app. They are NOT real adverts.
SCAM_EXAMPLES = [
    {
        "title": "The learnership you have to pay for",
        "example": "URGENT: Learnership 2026 at a big bank. Limited spots! Pay R350 registration fee to secure your place. WhatsApp 072 000 0000.",
        "flags": ["Asks for money", "Pressure to act fast", "WhatsApp only", "No official company link"],
        "lesson": "Real learnerships and jobs are never sold. If you must pay to apply, walk away.",
    },
    {
        "title": "Easy money from home",
        "example": "Earn R5,000 per week capturing data from home. No experience needed. Send your ID copy and bank details to start today.",
        "flags": ["Pay that sounds too good", "Wants ID and bank details straight away", "No company name"],
        "lesson": "An employer does not need your bank details before you have been hired and signed a contract.",
    },
    {
        "title": "The fake government vacancy",
        "example": "Department vacancies open now! Apply at gov-jobs-sa.com and pay a R200 admin fee.",
        "flags": ["Look-alike website, not a .gov.za address", "Admin fee"],
        "lesson": "Government posts are advertised on official .gov.za websites and never need a fee. Type the department's address yourself instead of clicking a link.",
    },
    {
        "title": "You have been selected (but you never applied)",
        "example": "Congratulations! You have been selected for a position. No interview needed. Reply with your ID and bank details to receive your contract.",
        "flags": ["Job you never applied for", "No interview", "Wants ID and bank details"],
        "lesson": "Be suspicious of any job offer for something you did not apply for.",
    },
    {
        "title": "The overseas job offer",
        "example": "Well-paid customer service jobs overseas! We pay your flight and accommodation. Send your passport copy now.",
        "flags": ["Overseas job with no clear employer", "Wants your passport quickly", "Free travel as bait"],
        "lesson": "Fake overseas offers are sometimes used to lure young people into forced labour. Never travel for a job you have not verified through official channels.",
    },
    {
        "title": "Interview on chat, then you must buy a kit",
        "example": "Your interview is on Telegram. To start you must buy your uniform and starter kit from our supplier for R800.",
        "flags": ["Interview only on a chat app", "You must buy a kit", "Pay a supplier chosen by them"],
        "lesson": "A genuine employer provides the equipment or tells you openly what it costs, and meets you properly.",
    },
]

REPORT_STEPS = [
    ("Stop and keep proof", "Stop replying. Do not pay or send anything more. Take screenshots of the ad and messages, and save the links, phone numbers and any proof of payment."),
    ("Call your bank if you paid or shared banking details", "Phone your bank straight away, using the number on the back of your card or in the official banking app, not a number from the message. Ask them to stop payments and secure your account. Never share an OTP or PIN."),
    ("Protect your identity if you sent your ID", "The Southern African Fraud Prevention Service offers Protective Registration to people whose identity may be at risk. Check safps.org.za for how it works."),
    ("Report it to the police", "Open a case at your nearest police station and keep the case number. In an emergency call 10111."),
    ("Report the ad and the impersonated company", "Report the post to the platform (Facebook, WhatsApp, Telegram or the job board). If the scammers used a real company's name, tell that company using the contact details on its official website."),
    ("Warn others", "Share a warning with friends and family so they do not fall for the same trick."),
]

REAL_JOB_SOURCES = [
    ("SAYouth.mobi", "Free support and opportunities for young job seekers.", "https://sayouth.mobi"),
    ("Public Service vacancies (DPSA)", "Government posts are advertised through the Department of Public Service and Administration.", "https://www.dpsa.gov.za"),
    ("Harambee Youth Employment Accelerator", "Programmes that link young people to work opportunities.", "https://www.harambee.co.za"),
]
REAL_JOB_NOTE = ("You can also go straight to the careers page of a company you know by typing its address yourself. "
                 "Established job boards are useful, but scam ads sometimes appear on them too, so still check each company.")
