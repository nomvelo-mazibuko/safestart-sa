"""SafeStart SA - a free work-readiness app for South African youth.

Screens
  1. Home          - three big buttons
  2. Scam checker  - paste an ad, check the link, tick red flags, get a risk rating
  3. Rights        - labour law lessons (the text lives in rights_content.py)
  4. Skills        - email writing tips and a 30-second typing test

Run on your computer:   flet run main.py
Run in the browser:     flet run --web main.py
"""
import asyncio
import os
import random
import re
import sys

import flet as ft

import rights_content
import verifier

# ---------- Colours ----------
TEAL = "#0F4C5C"
INK = "#1B2A30"
MUTED = "#5B6B71"
BACKGROUND = "#F2F6F7"
WHITE = "#FFFFFF"
RED = "#B3261E"
AMBER = "#B26A00"
GREEN = "#2E7D32"

# ---------- Scam checker data ----------
# Each red flag has: a key, the question shown to the user, how many risk points
# it is worth, and an optional pattern used to spot it automatically in text.
FLAGS = [
    {"key": "pay", "weight": 40,
     "text": "They asked me to pay for something (application, training, uniform, deposit)",
     "pattern": r"(application|registration|admin|training|processing|admission)\s+fee|\bdeposit\b|uniform|starter kit|pay\s+(r\s?\d|\d)"},
    {"key": "docs", "weight": 30,
     "text": "They want my ID copy, bank details or an OTP before an interview",
     "pattern": r"bank(ing)? details|bank account|\botp\b|\bpin\b|copy of (your )?id|id copy"},
    {"key": "no_interview", "weight": 25,
     "text": "I was offered the job without applying or without an interview",
     "pattern": r"no interview|hired immediately|instant(ly)? hired|you have been selected"},
    {"key": "high_pay", "weight": 20,
     "text": "The pay sounds too good for the work",
     "pattern": r"earn up to|r\s?\d[\d\s,]*\s*(per|a|/)\s*(day|week)|easy money|guaranteed income"},
    {"key": "company", "weight": 20,
     "text": "I can't find the company online or on the CIPC register",
     "pattern": None},
    {"key": "chat_only", "weight": 15,
     "text": "The interview or contact is only on WhatsApp or Telegram",
     "pattern": r"whatsapp|telegram"},
    {"key": "email", "weight": 15,
     "text": "Emails come from Gmail/Yahoo, or don't match the company website",
     "pattern": r"@(gmail|yahoo|hotmail|outlook)\.com"},
    {"key": "rush", "weight": 10,
     "text": "They are pressuring me to decide or pay quickly",
     "pattern": r"urgent|act now|limited (spots|positions)|apply today|immediate start"},
]

ADVICE_HIGH = [
    "Do not pay anything and do not send ID, bank details or OTPs.",
    "Registered private employment agencies may not charge job seekers fees.",
    "Stop contact and tell a friend or family member what happened.",
    "If you already paid or shared documents, contact your bank and SAPS.",
]
ADVICE_MEDIUM = [
    "Pause before sharing any documents or money.",
    "Search the company on the CIPC register and check its official website.",
    "Ask for an interview at the company's office or on a video call.",
    "Call the company using a number from its official website, not from the ad.",
]
ADVICE_LOW = [
    "Fewer warning signs, but no checker can guarantee an offer is real.",
    "Still verify the company before you share personal documents.",
    "A real employer never needs your PIN or OTP.",
]

# Icon and colour for each kind of finding from verifier.py
FINDING_STYLES = {
    "good": (ft.Icons.CHECK_CIRCLE, GREEN),
    "warn": (ft.Icons.WARNING_AMBER_ROUNDED, AMBER),
    "bad": (ft.Icons.CANCEL, RED),
    "info": (ft.Icons.INFO_OUTLINE, MUTED),
}

# ---------- Skills data ----------
EMAIL_TIPS = [
    "Write a clear subject line: the role you want and your name.",
    "Greet by name (Dear Ms Naidoo). Use 'Dear Hiring Manager' only if you can't find one.",
    "Keep it short: who you are, what you want, what is attached.",
    "Use a professional email address, such as name.surname@gmail.com.",
    "Check spelling and attachments before you press send.",
    "End with 'Kind regards' and your full name and phone number.",
]

EMAIL_EXAMPLE = (
    "Subject: Application for Junior Accountant position - Thandi Nkosi\n\n"
    "Dear Mr Dlamini,\n\n"
    "I am applying for the Junior Accountant position advertised on [where you saw it]. "
    "I recently completed my BCom Accounting at [university] and I am eager to apply my skills.\n\n"
    "I have attached my CV and academic record. I would welcome the chance to discuss "
    "how I can contribute to your team.\n\n"
    "Kind regards,\nThandi Nkosi\n082 000 0000"
)

TYPING_PASSAGES = [
    "A good first impression at work starts with being on time and being ready to learn. "
    "Ask questions when you are not sure and write down what you are told so that you can "
    "remember it later. Small habits like these show your manager that you care about the job.",
    "When you apply for a job always read the advert carefully before you send your details. "
    "Real employers do not ask you to pay money to be hired and they will never need your bank "
    "pin. If something feels wrong take a moment and check with someone you trust.",
]
TYPING_TEST_SECONDS = 30


# ---------- Small building blocks used by every screen ----------
def make_card(content, border_color="#D9E2E5"):
    """A white box with a thin border."""
    return ft.Container(
        content=content,
        bgcolor=WHITE,
        padding=16,
        border_radius=10,
        border=ft.Border.all(1, border_color),
    )


def make_heading(text):
    return ft.Text(text, size=24, weight=ft.FontWeight.BOLD, color=INK)


def make_section_title(text):
    return ft.Text(text, size=18, weight=ft.FontWeight.W_600, color=TEAL)


def make_text(text, color=INK, size=15):
    return ft.Text(text, size=size, color=color)


# ---------- Screen 1: Home ----------
def home_view(page, go_to_screen):
    def make_tile(icon, title, description, screen_number):
        def on_tile_click(e):
            go_to_screen(screen_number)

        row = ft.Row(
            [
                ft.Icon(icon, color=TEAL, size=30),
                ft.Column(
                    [
                        ft.Text(title, size=17, weight=ft.FontWeight.W_600, color=INK),
                        ft.Text(description, size=14, color=MUTED),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=14,
        )
        return ft.Container(content=make_card(row), on_click=on_tile_click)

    return [
        ft.Text("SafeStart SA", size=30, weight=ft.FontWeight.BOLD, color=TEAL),
        make_text("Free tools to spot fake job offers, know your rights and feel ready for work.", MUTED),
        make_tile(ft.Icons.SHIELD_OUTLINED, "Check a job offer", "Paste an ad and see how risky it looks.", 1),
        make_tile(ft.Icons.GAVEL_OUTLINED, "Know your rights", "Plain-language lessons before your first job.", 2),
        make_tile(ft.Icons.KEYBOARD_OUTLINED, "Build your skills", "Email writing tips and a typing test.", 3),
        make_text("SafeStart SA gives general information, not legal advice.", MUTED, 12),
    ]


# ---------- Screen 2: Scam checker ----------
def scam_view(page, go_to_screen):
    # The input boxes
    ad_box = ft.TextField(label="Paste the job ad, email or WhatsApp message",
                          multiline=True, min_lines=4, max_lines=8)
    link_box = ft.TextField(label="Link to the job (optional)", hint_text="https://...")
    company_box = ft.TextField(label="Company's official website (optional)",
                               hint_text="Type it yourself, don't copy it from the ad")
    title_box = ft.TextField(label="Job title (optional)", hint_text="e.g. Junior Accountant")

    # One checkbox for every red flag. We keep them in a dictionary: key -> checkbox
    checkboxes = {}
    for flag in FLAGS:
        checkboxes[flag["key"]] = ft.Checkbox(label=flag["text"])

    # Areas of the screen that we fill in later
    online_results_area = ft.Column(spacing=8)
    final_result_area = ft.Column()

    # This remembers the score from the online check between button presses
    memory = {"online_score": 0, "online_check_done": False}

    def scan_the_ad(e):
        """Look for red flags in the pasted text and tick the matching boxes."""
        ad_text = (ad_box.value or "").lower()
        found_count = 0
        for flag in FLAGS:
            if flag["pattern"] is not None and re.search(flag["pattern"], ad_text):
                checkboxes[flag["key"]].value = True
                found_count = found_count + 1

        # Copy the first link from the ad into the link box
        links_in_ad = verifier.find_urls(ad_box.value or "")
        link_was_copied = len(links_in_ad) > 0 and (link_box.value or "").strip() == ""
        if link_was_copied:
            link_box.value = links_in_ad[0]

        if found_count > 0:
            message = f"Scan found {found_count} possible warning sign(s) and ticked them. "
        else:
            message = "The scan found nothing obvious. "
        if link_was_copied:
            message = message + "We copied the link from the ad. Press 'Verify link and company' next. "
        message = message + "Review the list, then press 'Check result'."

        final_result_area.controls = [make_text(message, MUTED, 14)]
        page.update()

    async def verify_online(e):
        """Open the link and the company website (this can take a few seconds)."""
        # On GitHub Pages the app runs inside the browser, which is not allowed to
        # open other websites, so the online check cannot work there.
        if sys.platform == "emscripten":
            online_results_area.controls = [make_text(
                "The online link check needs the server version of SafeStart SA. "
                "You can still scan the ad text and tick the boxes below.", AMBER, 14)]
            page.update()
            return

        job_link = (link_box.value or "").strip()
        company_site = (company_box.value or "").strip()
        if job_link == "" and company_site == "":
            online_results_area.controls = [make_text("Add a job link or the company's website first.", RED, 14)]
            page.update()
            return

        # Show a spinner while we wait
        spinner = ft.ProgressRing(width=20, height=20, stroke_width=3)
        online_results_area.controls = [
            ft.Row([spinner, make_text("Checking the link and the company website...", MUTED, 14)])
        ]
        page.update()

        # Run the slow check in the background so the app does not freeze
        patterns = {}
        for flag in FLAGS:
            if flag["pattern"] is not None:
                patterns[flag["key"]] = flag["pattern"]
        result = await asyncio.to_thread(verifier.verify, job_link, company_site, title_box.value or "", patterns)

        # Tick the boxes for red flags found on the page
        for key in result["matches"]:
            checkboxes[key].value = True
        memory["online_score"] = result["score"]
        memory["online_check_done"] = True

        # Show every finding with its icon
        rows = [ft.Text("Online check", size=17, weight=ft.FontWeight.W_600, color=INK)]
        for finding in result["findings"]:
            icon, color = FINDING_STYLES[finding["level"]]
            rows.append(ft.Row(
                [ft.Icon(icon, color=color, size=20), ft.Text(finding["text"], size=14, color=INK, expand=True)],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ))
        rows.append(make_text(
            "These checks look for warning signs. They cannot prove a job is real or fake. "
            "When in doubt, phone the company on the number from its own website.", MUTED, 12))
        online_results_area.controls = [make_card(ft.Column(rows, spacing=8))]
        page.update()

    async def open_cipc(e):
        await ft.UrlLauncher().launch_url("https://www.cipc.co.za")

    def show_result(e):
        """Add up the points from the ticked boxes and the online check."""
        score = memory["online_score"]
        for flag in FLAGS:
            if checkboxes[flag["key"]].value:
                score = score + flag["weight"]
        if score < 0:
            score = 0

        if score >= 40:
            title, color, tips = "High risk: likely a scam", RED, ADVICE_HIGH
        elif score >= 15:
            title, color, tips = "Be careful: verify before you continue", AMBER, ADVICE_MEDIUM
        else:
            title, color, tips = "Low risk, but stay alert", GREEN, ADVICE_LOW

        lines = [ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=color)]
        for tip in tips:
            lines.append(make_text("\u2022 " + tip))
        if not memory["online_check_done"]:
            lines.append(make_text("You have not run the online check yet. Add the job link or the "
                                   "company website for a better result.", MUTED, 13))
        lines.append(ft.Button(content="Check company on CIPC", icon=ft.Icons.OPEN_IN_NEW, on_click=open_cipc))

        final_result_area.controls = [make_card(ft.Column(lines, spacing=8), border_color=color)]
        page.update()

    def start_over(e):
        for box in [ad_box, link_box, company_box, title_box]:
            box.value = ""
        for key in checkboxes:
            checkboxes[key].value = False
        memory["online_score"] = 0
        memory["online_check_done"] = False
        online_results_area.controls = []
        final_result_area.controls = []
        page.update()

    # Put the screen together, top to bottom
    screen = [
        make_heading("Job scam checker"),
        make_text("Paste the message, check the link against the company's real website, and get a risk rating.", MUTED),
        ad_box,
        ft.Button(content="Scan my ad", icon=ft.Icons.SEARCH, on_click=scan_the_ad),
        ft.Divider(),
        make_text("Check the link", INK, 16),
        link_box,
        company_box,
        title_box,
        ft.Button(content="Verify link and company", icon=ft.Icons.VERIFIED_USER_OUTLINED, on_click=verify_online),
        online_results_area,
        ft.Divider(),
        make_text("Does any of this apply?", INK, 16),
    ]
    for flag in FLAGS:
        screen.append(checkboxes[flag["key"]])
    screen.append(ft.Row([
        ft.FilledButton(content="Check result", on_click=show_result),
        ft.TextButton(content="Start over", on_click=start_over),
    ]))
    screen.append(final_result_area)
    return screen


# ---------- Screen 3: Know your rights ----------
def make_point(point):
    """A point is either plain text, or a pair: (bold start, rest of the sentence)."""
    if isinstance(point, tuple):
        bold_part, rest = point
        return ft.Text(
            spans=[
                ft.TextSpan(bold_part + " ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.TextSpan(rest),
            ],
            size=15, color=INK,
        )
    return make_text(point)


def make_lesson(lesson):
    """One lesson that opens and closes when tapped."""
    point_texts = []
    for point in lesson["points"]:
        point_texts.append(make_point(point))
    content = ft.Container(
        content=ft.Column(point_texts, spacing=10),
        padding=ft.Padding.only(left=16, right=16, bottom=14),
    )
    return ft.ExpansionTile(
        title=ft.Text(lesson["title"], weight=ft.FontWeight.W_600, color=INK),
        subtitle=ft.Text(lesson["law"], size=12, color=MUTED),
        controls=[content],
    )


def make_pay_checker(page):
    """The 'Is my pay legal?' calculator."""
    pay_box = ft.TextField(label="Your pay per month (R, before deductions)", keyboard_type=ft.KeyboardType.NUMBER)
    hours_box = ft.TextField(label="Ordinary hours you work per week", keyboard_type=ft.KeyboardType.NUMBER, value="45")
    answer_area = ft.Column(spacing=6)

    def check_pay(e):
        try:
            monthly_pay = float((pay_box.value or "").replace(",", ".").replace(" ", ""))
            weekly_hours = float((hours_box.value or "").replace(",", "."))
        except ValueError:
            answer_area.controls = [make_text("Enter your monthly pay and weekly hours as numbers.", RED, 14)]
            page.update()
            return
        if monthly_pay <= 0 or weekly_hours <= 0 or weekly_hours > 80:
            answer_area.controls = [make_text("Enter realistic numbers for pay and hours.", RED, 14)]
            page.update()
            return

        hours_per_month = weekly_hours * 52 / 12  # 52 weeks in a year, 12 months
        hourly_rate = monthly_pay / hours_per_month
        minimum_monthly = rights_content.NMW_RATE * hours_per_month

        if hourly_rate < rights_content.NMW_RATE:
            answer_area.controls = [
                ft.Text(f"About R{hourly_rate:.2f} an hour. This is below the minimum.",
                        size=16, weight=ft.FontWeight.BOLD, color=RED),
                make_text(f"For {weekly_hours:g} hours a week the minimum is about R{minimum_monthly:,.2f} a month "
                          f"(R{rights_content.NMW_RATE:.2f} an hour from {rights_content.NMW_FROM}). "
                          "Ask your employer to explain, then contact the Department of Employment and Labour."),
            ]
        else:
            answer_area.controls = [
                ft.Text(f"About R{hourly_rate:.2f} an hour. This is at or above the minimum.",
                        size=16, weight=ft.FontWeight.BOLD, color=GREEN),
                make_text("Learnerships, public works programmes and some sectors have different rates, "
                          "and overtime is paid on top.", MUTED, 13),
            ]
        page.update()

    return make_card(ft.Column(
        [
            ft.Text("Is my pay legal?", size=18, weight=ft.FontWeight.W_600, color=INK),
            make_text(f"Minimum wage: R{rights_content.NMW_RATE:.2f} an hour from {rights_content.NMW_FROM}.", MUTED, 14),
            pay_box,
            hours_box,
            ft.FilledButton(content="Check my pay", on_click=check_pay),
            answer_area,
        ],
        spacing=10,
    ))


def make_help_row(name, description, web_address):
    """A tappable row that opens a website."""
    async def open_website(e):
        await ft.UrlLauncher().launch_url(web_address)

    return ft.ListTile(
        title=ft.Text(name, weight=ft.FontWeight.W_600, color=INK),
        subtitle=ft.Text(description, color=MUTED),
        trailing=ft.Icon(ft.Icons.OPEN_IN_NEW, color=TEAL),
        on_click=open_website,
    )


def rights_view(page, go_to_screen):
    screen = [
        make_heading("Know your rights"),
        make_text("Plain-language guide to South African labour law for first-time workers.", MUTED),
        make_pay_checker(page),
    ]

    # The lessons, grouped by topic
    for group_name, lessons in rights_content.GROUPS:
        lesson_tiles = []
        for lesson in lessons:
            lesson_tiles.append(make_lesson(lesson))
        screen.append(make_section_title(group_name))
        screen.append(make_card(ft.Column(lesson_tiles, spacing=0)))

    # What to do if something goes wrong
    steps = []
    number = 1
    for step_title, step_text in rights_content.IF_WRONG_STEPS:
        steps.append(ft.Column(
            [ft.Text(f"{number}. {step_title}", weight=ft.FontWeight.W_600, color=INK), make_text(step_text)],
            spacing=2,
        ))
        number = number + 1
    screen.append(make_section_title("If something goes wrong"))
    screen.append(make_card(ft.Column(steps, spacing=12)))

    # Links to free help
    help_rows = []
    for name, description, web_address in rights_content.HELP_LINKS:
        help_rows.append(make_help_row(name, description, web_address))
    screen.append(make_section_title("Where to get free help"))
    screen.append(make_card(ft.Column(help_rows, spacing=0)))

    # Checklist
    checklist = []
    for item in rights_content.BEFORE_YOU_SIGN:
        checklist.append(ft.Checkbox(label=item))
    screen.append(make_section_title("Before you sign"))
    screen.append(make_card(ft.Column(checklist, spacing=2)))

    screen.append(make_text(
        f"Last updated {rights_content.CONTENT_UPDATED}. This is general information, not legal advice. "
        "Laws and amounts change, so confirm the latest details with the Department of Employment "
        "and Labour or the CCMA.", MUTED, 12))
    return screen


# ---------- Screen 4: Skills ----------
def skills_view(page, go_to_screen):
    # --- Email tips card ---
    email_lines = [ft.Text("Writing a professional email", size=18, weight=ft.FontWeight.W_600, color=INK)]
    for tip in EMAIL_TIPS:
        email_lines.append(make_text("\u2022 " + tip))
    email_lines.append(ft.ExpansionTile(
        title=ft.Text("See an example email"),
        controls=[ft.Container(content=ft.Text(EMAIL_EXAMPLE, selectable=True, color=INK), padding=12)],
    ))

    # --- Typing test card ---
    passage_text = ft.Text("Press Start to get a passage.", size=16, color=INK)
    timer_text = ft.Text(f"{TYPING_TEST_SECONDS}s", size=22, weight=ft.FontWeight.BOLD, color=TEAL)
    typing_box = ft.TextField(multiline=True, min_lines=3, max_lines=5, disabled=True,
                              hint_text="Type here once the test starts")
    result_text = ft.Text("", size=16, weight=ft.FontWeight.W_600, color=INK)
    start_button = ft.FilledButton(content="Start typing test")

    async def run_typing_test(e):
        passage = random.choice(TYPING_PASSAGES)
        passage_text.value = passage
        typing_box.value = ""
        typing_box.disabled = False
        result_text.value = ""
        start_button.disabled = True
        page.update()
        await typing_box.focus()

        try:
            # Count down one second at a time
            for seconds_left in range(TYPING_TEST_SECONDS, 0, -1):
                timer_text.value = f"{seconds_left}s"
                timer_text.update()
                await asyncio.sleep(1)

            # Time is up: compare what was typed with the passage, word by word
            typed_words = (typing_box.value or "").split()
            passage_words = passage.split()
            correct_words = 0
            for i in range(min(len(typed_words), len(passage_words))):
                if typed_words[i] == passage_words[i]:
                    correct_words = correct_words + 1

            words_per_minute = round(correct_words * 60 / TYPING_TEST_SECONDS)
            if len(typed_words) > 0:
                accuracy = round(100 * correct_words / len(typed_words))
            else:
                accuracy = 0

            timer_text.value = "Time!"
            typing_box.disabled = True
            start_button.disabled = False
            start_button.content = "Try again"
            result_text.value = f"{words_per_minute} words per minute, {accuracy}% accuracy"
            page.update()
        except Exception:
            return  # the person left this screen in the middle of the test

    start_button.on_click = run_typing_test

    typing_lines = [
        ft.Text("Typing test", size=18, weight=ft.FontWeight.W_600, color=INK),
        make_text(f"Type the passage for {TYPING_TEST_SECONDS} seconds.", MUTED, 14),
        timer_text, passage_text, typing_box, start_button, result_text,
    ]

    return [
        make_heading("Build your skills"),
        make_card(ft.Column(email_lines, spacing=8)),
        make_card(ft.Column(typing_lines, spacing=10)),
    ]


# ---------- The app itself ----------
# The four screens, in the same order as the buttons at the bottom
SCREENS = [home_view, scam_view, rights_view, skills_view]


def main(page: ft.Page):
    page.title = "SafeStart SA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=TEAL)
    page.bgcolor = BACKGROUND
    page.padding = 0

    content_area = ft.Container(expand=True, padding=16)

    def show_screen(number):
        """Build the chosen screen and put it on the page."""
        build_screen = SCREENS[number]
        content_area.content = ft.Column(build_screen(page, go_to_screen), scroll=ft.ScrollMode.AUTO, spacing=12, expand=True)
        page.update()

    def go_to_screen(number):
        """Used by the Home buttons: move the bottom bar AND show the screen."""
        nav_bar.selected_index = number
        show_screen(number)

    def on_nav_change(e):
        show_screen(e.control.selected_index)

    nav_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SHIELD_OUTLINED, label="Scam check"),
            ft.NavigationBarDestination(icon=ft.Icons.GAVEL_OUTLINED, label="Rights"),
            ft.NavigationBarDestination(icon=ft.Icons.KEYBOARD_OUTLINED, label="Skills"),
        ],
    )
    page.navigation_bar = nav_bar
    page.add(ft.SafeArea(content_area, expand=True))
    show_screen(0)


if __name__ == "__main__":
    port = os.getenv("PORT")  # hosting services set PORT for us
    if port:
        ft.run(main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(port))
    else:
        ft.run(main)
