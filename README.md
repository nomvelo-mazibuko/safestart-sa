# SafeStart SA

A free work-readiness app for South African youth, built with Python and Flet.

- **Job scam checker:** spots warning signs in job ads and checks the job link against the company's own website.
- **Know your rights:** plain-language South African labour law lessons and a minimum-wage calculator.
- **Skills hub:** email-writing tips and a typing test.

The app collects no personal data. It gives general information, not legal advice.

## Run it on your computer

    pip install -r requirements-server.txt
    python main.py            # desktop window
    flet run --web main.py    # in the browser

## Files

- `main.py` - screens and buttons
- `verifier.py` - link and company-website checks
- `rights_content.py` - labour law text (update the minimum wage here each March)
- `requirements-server.txt` - packages for hosting on Render
- `render.yaml` - Render hosting settings

Built by SafeStart Labs for the FNB App of the Year Hackathon 2026.
