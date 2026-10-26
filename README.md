# SafeStart SA

A free work-readiness app for South African youth, built with Python and Flet.

- **Job scam checker:** spots warning signs in job ads, checks the job link against the company's own website, and lets you share a warning. Includes scam examples, a "what to do if scammed" guide and places to find real opportunities.
- **Know your rights:** plain-language South African labour law lessons, a minimum-wage calculator, sources and a "before you sign" checklist.
- **Tools:** payslip checker, contract checker and a rights quiz with a learning badge.
- **Skills hub:** email tips, typing test, CV tips and interview practice.

The app collects no personal data. It gives general information, not legal advice.
Results are warning signs, not proof.

## Run it on your computer

    python -m venv venv
    venv\Scripts\activate            (Mac/Linux: source venv/bin/activate)
    pip install -r requirements-server.txt
    python main.py                   (desktop window)
    flet run --web main.py           (in the browser)

## Run the tests

    python -m unittest discover -s tests -v

## Files

| File | What it does |
|---|---|
| `main.py` | Home, scam checker, rights and skills screens, and the app shell |
| `tools.py` | Payslip checker, contract checker and rights quiz screen |
| `verifier.py` | Link and company-website checks, with safety limits |
| `ratelimit.py` | Limits how often the link checker can be used |
| `checkers.py` | Logic for the contract and payslip checkers |
| `ui.py` | Colours and shared building blocks |
| `settings.py` | Feedback link and "reviewed by" note |
| `rights_content.py` | Labour law lessons and the minimum wage (update each March) |
| `scam_content.py` | Scam examples, reporting steps, real job sources |
| `skills_content.py` | CV and interview content |
| `quiz_content.py` | Quiz questions |
| `tests/` | Automated tests |
| `requirements.txt`, `requirements-server.txt` | Pinned packages |
| `render.yaml` | Render hosting settings |
| `.github/` | Automatic tests and update alerts on GitHub |
| `SECURITY.md` | How to report a problem |

Built by SafeStart Labs for the FNB App of the Year Hackathon 2026.
