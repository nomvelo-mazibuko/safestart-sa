"""The Tools screen: payslip checker, contract checker and the rights quiz."""
from datetime import date

import flet as ft

import checkers
import quiz_content
from ui import (AMBER, GREEN, INK, MUTED, RED, TEAL, make_card, make_heading,
                make_section_title, make_text)

MAX_CONTRACT_CHARS = 8000

LEVEL_STYLES = {
    "good": (ft.Icons.CHECK_CIRCLE, GREEN),
    "info": (ft.Icons.INFO_OUTLINE, MUTED),
    "warn": (ft.Icons.WARNING_AMBER_ROUNDED, AMBER),
    "bad": (ft.Icons.CANCEL, RED),
}


def result_row(level, text):
    """One line with an icon, used by all three tools."""
    icon, color = LEVEL_STYLES[level]
    return ft.Row(
        [ft.Icon(icon, color=color, size=20), ft.Text(text, size=14, color=INK, expand=True)],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def read_amount(text):
    """Turn what the user typed into a number. Empty means 0."""
    cleaned = (text or "").replace("R", "").replace(" ", "").replace(",", ".").strip()
    if cleaned == "":
        return 0.0
    return float(cleaned) 


# ---------- Payslip checker ----------
def make_payslip_checker(page):
    boxes = {}
    for key, label in [("gross", "Gross pay (R, before deductions)"),
                       ("uif", "UIF deducted (R)"),
                       ("paye", "Tax (PAYE) deducted (R)"),
                       ("other", "Other deductions (R)"),
                       ("net", "Net pay you received (R)")]:
        boxes[key] = ft.TextField(label=label, keyboard_type=ft.KeyboardType.NUMBER, max_length=12)
    answer_area = ft.Column(spacing=8)

    def check(e):
        try:
            gross = read_amount(boxes["gross"].value)
            uif = read_amount(boxes["uif"].value)
            paye = read_amount(boxes["paye"].value)
            other = read_amount(boxes["other"].value)
            net = read_amount(boxes["net"].value)
            findings = checkers.check_payslip(gross, uif, paye, other, net)
        except ValueError:
            answer_area.controls = [make_text("Enter positive numbers. Gross pay and net pay are required.", RED, 14)]
            page.update()
            return
        answer_area.controls = [result_row(level, text) for level, text in findings]
        page.update()

    lines = [
        ft.Text("Payslip checker", size=18, weight=ft.FontWeight.W_600, color=INK),
        make_text("Type the amounts from your payslip to look for obvious problems.", MUTED, 14),
    ]
    for key in boxes:
        lines.append(boxes[key])
    lines.append(ft.FilledButton(content="Check my payslip", on_click=check))
    lines.append(answer_area)
    return make_card(ft.Column(lines, spacing=10))


# ---------- Contract checker ----------
def make_contract_checker(page):
    contract_box = ft.TextField(
        label="Paste your contract or offer letter",
        multiline=True, min_lines=5, max_lines=10, max_length=MAX_CONTRACT_CHARS,
    )
    answer_area = ft.Column(spacing=8)

    def check(e):
        text = (contract_box.value or "").strip()
        if len(text) < 50:
            answer_area.controls = [make_text("Paste more of the contract so it can be checked.", RED, 14)]
            page.update()
            return
        result = checkers.check_contract(text)
        rows = []
        for warning in result["warnings"]:
            rows.append(result_row("warn", warning))
        for name in result["found"]:
            rows.append(result_row("good", f"Mentions: {name}"))
        for name in result["missing"]:
            rows.append(result_row("info", f"Not found: {name}. Ask where this is covered."))
        rows.append(make_text(
            "This only looks for key words. It cannot judge whether the terms are fair or legal. "
            "Ask a union, the Department of Employment and Labour or Legal Aid SA if you are unsure.", MUTED, 12))
        answer_area.controls = rows
        page.update()

    return make_card(ft.Column(
        [
            ft.Text("Contract checker", size=18, weight=ft.FontWeight.W_600, color=INK),
            make_text("Checks that the main written terms are mentioned and looks for worrying wording. "
                      "Your text is not saved.", MUTED, 14),
            contract_box,
            ft.FilledButton(content="Check my contract", on_click=check),
            answer_area,
        ],
        spacing=10,
    ))


# ---------- Rights quiz ----------
def make_quiz(page):
    groups = []  
    question_blocks = []
    number = 1
    for question in quiz_content.QUESTIONS:
        radios = []
        for position, option in enumerate(question["options"]):
            radios.append(ft.Radio(value=str(position), label=option))
        group = ft.RadioGroup(content=ft.Column(radios, spacing=0))
        groups.append(group)
        question_blocks.append(ft.Column(
            [ft.Text(f"{number}. {question['q']}", weight=ft.FontWeight.W_600, color=INK), group],
            spacing=4,
        ))
        number = number + 1

    result_area = ft.Column(spacing=8)

    def check_answers(e):
        if any(group.value is None for group in groups):
            result_area.controls = [make_text("Answer every question first.", RED, 14)]
            page.update()
            return
        score = 0
        review = []
        for i, question in enumerate(quiz_content.QUESTIONS):
            if int(groups[i].value) == question["answer"]:
                score = score + 1
            else:
                correct = question["options"][question["answer"]]
                review.append(result_row("warn", f"Question {i + 1}: the answer is '{correct}'. {question['why']}"))

        total = len(quiz_content.QUESTIONS)
        lines = [ft.Text(f"You scored {score} out of {total}", size=18, weight=ft.FontWeight.BOLD, color=INK)]
        lines.extend(review)
        if score >= quiz_content.PASS_MARK:
            badge = make_card(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.VERIFIED, color=GREEN, size=36),
                        ft.Text("SafeStart Rights Ready", size=20, weight=ft.FontWeight.BOLD, color=GREEN),
                        make_text(f"Completed on {date.today().strftime('%d %B %Y')} with {score}/{total}.", INK, 14),
                        make_text("This is a learning badge from SafeStart SA, not an official qualification.", MUTED, 12),
                    ],
                    spacing=4,
                ),
                border_color=GREEN,
            )
            lines.append(badge)
        else:
            lines.append(make_text(f"You need {quiz_content.PASS_MARK} correct for the badge. "
                                   "Read the Know Your Rights lessons and try again.", MUTED, 14))
        result_area.controls = lines
        page.update()

    def start_over(e):
        for group in groups:
            group.value = None
        result_area.controls = []
        page.update()

    content = [
        ft.Text("Rights quiz", size=18, weight=ft.FontWeight.W_600, color=INK),
        make_text("Test what you have learned. Score well to earn the badge.", MUTED, 14),
    ]
    content.extend(question_blocks)
    content.append(ft.Row([
        ft.FilledButton(content="Check answers", on_click=check_answers),
        ft.TextButton(content="Start over", on_click=start_over),
    ]))
    content.append(result_area)
    return make_card(ft.Column(content, spacing=12))


# ---------- The screen ----------
def tools_view(page, go_to_screen):
    return [
        make_heading("Tools"),
        make_text("Quick checks for your pay and your contract, and a quiz on your rights.", MUTED),
        make_payslip_checker(page),
        make_contract_checker(page),
        make_quiz(page),
    ]
