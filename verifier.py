"""Link and company-website checks for SafeStart SA.

verify(job_url, company_site, job_title, patterns) opens the job link and
(if given) the company's own website, then returns a dictionary:

    {"findings": [...], "score": 25, "page_text": "...", "matches": ["pay", ...]}

Each finding is a small dictionary: {"level": "bad", "text": "...", "points": 30}
  level  = "good", "info", "warn" or "bad"
  points = added to the risk score (negative numbers lower it)

Only the Python standard library is used, so there is nothing extra to install.
No automatic check can PROVE a job is real or fake. These are warning signs only.
"""
import ipaddress
import json
import re
import socket
from datetime import datetime, timezone
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

# Tests set this to True. Keep it False so users cannot make the app open
# addresses on their own network.
ALLOW_PRIVATE = False
TIMEOUT = 8  # seconds to wait for a website
MAX_BYTES = 600000  # never download more than this from one page

# ---------- Lists the checks use ----------
# Domains ending like this have the real name in the LAST THREE parts (shoprite.co.za).
TWO_PART_ENDINGS = ["co.za", "org.za", "gov.za", "ac.za", "net.za", "web.za", "edu.za", "co.uk", "com.ng", "co.ke"]

FREE_OR_SOCIAL_SITES = [
    "facebook.com", "fb.com", "wixsite.com", "blogspot.com", "wordpress.com", "weebly.com",
    "sites.google.com", "linktr.ee", "wa.me", "t.me", "telegram.me", "github.io", "netlify.app", "carrd.co",
]
FORM_SITES = ["forms.gle", "docs.google.com", "jotform.com", "typeform.com", "forms.office.com"]
LINK_SHORTENERS = ["bit.ly", "tinyurl.com", "ow.ly", "is.gd", "cutt.ly", "rb.gy", "t.co"]
FREE_EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com", "icloud.com"]

# Established job boards. A listing there is a good sign, but not a guarantee.
JOB_BOARDS = ["linkedin.com", "indeed.com", "pnet.co.za", "careers24.com", "careerjunction.co.za", "sayouth.mobi", "harambee.co.za"]

# Brand word -> the ONLY website that company really uses.
OFFICIAL_SITES = {
    "shoprite": "shoprite.co.za", "checkers": "checkers.co.za", "picknpay": "picknpay.co.za",
    "woolworths": "woolworths.co.za", "capitec": "capitecbank.co.za", "fnb": "fnb.co.za",
    "absa": "absa.co.za", "nedbank": "nedbank.co.za", "standardbank": "standardbank.co.za",
    "sasol": "sasol.com", "eskom": "eskom.co.za", "sars": "sars.gov.za",
    "vodacom": "vodacom.co.za", "mtn": "mtn.co.za", "telkom": "telkom.co.za",
}

CAREER_WORDS = ["career", "job", "vacanc", "work with us", "join us", "opportunit"]
GUESSED_CAREER_PATHS = ["/careers", "/jobs", "/vacancies"]
IGNORED_TITLE_WORDS = ["the", "and", "for", "with", "junior", "senior", "intern", "internship", "position", "vacancy"]


# ---------- Small helpers ----------
def add_finding(result, level, text, points=0):
    """Add one finding to the result."""
    result["findings"].append({"level": level, "text": text, "points": points})


def calculate_score(findings):
    """Add up the points. Good signs can only lower the total by 20."""
    bad_points = 0
    good_points = 0
    for finding in findings:
        if finding["points"] > 0:
            bad_points = bad_points + finding["points"]
        else:
            good_points = good_points + finding["points"]
    if good_points < -20:
        good_points = -20
    return bad_points + good_points


def normalize_url(url):
    """Make sure the link starts with https:// so we can open it."""
    url = (url or "").strip().strip("<>\"'")
    if url != "" and "://" not in url:
        url = "https://" + url
    return url


def find_urls(text):
    """Find all links inside a piece of text."""
    found = re.findall(r"(?:https?://|www\.)[^\s<>\"')]+", text or "", re.IGNORECASE)
    cleaned = []
    for link in found:
        cleaned.append(link.rstrip(".,;:!?"))  # remove punctuation stuck to the end
    return cleaned


def registered_domain(host):
    """'careers.shoprite.co.za' -> 'shoprite.co.za'."""
    host = (host or "").lower().strip(".")
    if re.fullmatch(r"[\d.]+", host):  # a number address like 41.2.3.4
        return host
    parts = host.split(".")
    last_two = ".".join(parts[-2:])
    if len(parts) >= 3 and last_two in TWO_PART_ENDINGS:
        return ".".join(parts[-3:])
    return last_two


def title_matches(job_title, page_text):
    """True if most of the important words in the job title appear on the page."""
    words = []
    for word in re.findall(r"[a-z0-9]+", job_title.lower()):
        if len(word) > 2 and word not in IGNORED_TITLE_WORDS:
            words.append(word)
    if len(words) == 0:
        return False
    found = 0
    for word in words:
        if word in page_text.lower():
            found = found + 1
    return found / len(words) >= 0.75


# ---------- Opening websites safely ----------
class NoRedirect(HTTPRedirectHandler):
    """Stops Python following redirects automatically.
    We follow them ourselves in fetch() so we can check every address."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


opener = build_opener(NoRedirect)


def check_address_is_public(host):
    """Refuse addresses that belong to a private network (for safety)."""
    if ALLOW_PRIVATE:
        return
    for info in socket.getaddrinfo(host, None):
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise PermissionError("private address")


def fetch(url):
    """Open a web page. Returns (final_url, page_html). Raises an error if it fails."""
    for attempt in range(5):  # follow at most 5 redirects
        parts = urlparse(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise ValueError("not a web link")
        check_address_is_public(parts.hostname)

        request = Request(url, headers={"User-Agent": "Mozilla/5.0 (SafeStartSA link checker)"})
        try:
            response = opener.open(request, timeout=TIMEOUT)
        except HTTPError as error:
            location = error.headers.get("Location")
            if error.code in (301, 302, 303, 307, 308) and location:
                url = urljoin(url, location)  # go to the new address and loop again
                continue
            raise

        raw = response.read(MAX_BYTES)
        charset = response.headers.get_content_charset() or "utf-8"
        return url, raw.decode(charset, errors="ignore")
    raise ValueError("too many redirects")


def read_page(html):
    """Pull the title, the visible text and the links out of a page's HTML.
    Returns (title, text, links) where links is a list of (address, link_text)."""
    title = ""
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = unescape(title_match.group(1)).strip()

    # Throw away scripts and styles, they are not visible text
    html = re.sub(r"<(script|style|noscript).*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)

    links = []
    for address, inner in re.findall(r"<a\s[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html, re.IGNORECASE | re.DOTALL):
        links.append((address, re.sub(r"<[^>]+>", " ", inner).strip()))

    text = re.sub(r"<[^>]+>", " ", html)  # remove all tags
    text = unescape(re.sub(r"\s+", " ", text)).strip()
    return title, text, links


# ---------- The individual checks ----------
def check_lookalike(host, domain, result, label):
    """Warn if a web address contains a big brand name but is not that brand's real site."""
    squashed = host.replace("-", "").replace(".", "")
    for brand in OFFICIAL_SITES:
        real_site = OFFICIAL_SITES[brand]
        if brand in squashed and domain != real_site:
            add_finding(result, "bad", f"{label} looks like it is pretending to be {brand.title()}. The real site is {real_site}.", 40)
            return


def check_domain_age(domain, result):
    """Try to find out how old a website is. This is best effort and often fails for .co.za."""
    try:
        final_url, body = fetch("https://rdap.org/domain/" + domain)
        events = json.loads(body).get("events", [])
        created_text = None
        for event in events:
            if event.get("eventAction") == "registration":
                created_text = event["eventDate"]
        created = datetime.fromisoformat(created_text.replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - created).days
    except Exception:
        add_finding(result, "info", f"Could not check how old {domain} is. For .co.za sites, use a WHOIS lookup tool.")
        return

    if days < 90:
        add_finding(result, "bad", f"{domain} was registered only {days} days ago. Scam sites are often brand new.", 30)
    elif days < 365:
        add_finding(result, "warn", f"{domain} is less than a year old.", 15)
    else:
        add_finding(result, "good", f"{domain} has existed for about {days // 365} year(s).", -5)


def check_job_link(url, company_site, result, patterns):
    host = (urlparse(url).hostname or "").lower()
    domain = registered_domain(host)

    # 1. Things we can tell just from the address
    if re.fullmatch(r"[\d.]+", host):
        add_finding(result, "bad", "The link uses a number address instead of a company name.", 30)
    if "xn--" in host:
        add_finding(result, "bad", "The link uses disguised special characters in its web address.", 30)
    if url.startswith("http://"):
        add_finding(result, "warn", "The link is not secure (http, not https).", 10)
    if domain in LINK_SHORTENERS:
        add_finding(result, "warn", "This is a shortened link, so the real destination is hidden. Ask for the full link.", 15)
    if domain in FREE_OR_SOCIAL_SITES:
        add_finding(result, "warn", f"{domain} is a free or social site, not an official company website. Real employers post jobs on their own site or a known job board.", 20)
    if domain in FORM_SITES:
        add_finding(result, "warn", "The link goes to an online form. Never put ID numbers or bank details in it.", 15)
    check_lookalike(host, domain, result, "This web address")

    # 2. Try to open it
    try:
        final_url, html = fetch(url)
    except PermissionError:
        add_finding(result, "bad", "That link points to a private address and was not opened.", 30)
        return
    except HTTPError as error:
        add_finding(result, "warn", f"The site answered with an error ({error.code}). The job page may have been removed.", 15)
        return
    except (URLError, socket.gaierror, TimeoutError, ValueError) as error:
        reason = str(getattr(error, "reason", error))
        if "CERTIFICATE" in reason.upper():
            add_finding(result, "bad", "The site's security certificate is invalid. Do not enter any details.", 25)
        else:
            add_finding(result, "bad", "Could not open this link. The site may not exist, or your internet may be off.", 15)
        return

    final_host = (urlparse(final_url).hostname or "").lower()
    final_domain = registered_domain(final_host)
    if final_domain != domain:
        add_finding(result, "warn", f"The link redirected to a different site ({final_domain}).", 10)
        check_lookalike(final_host, final_domain, result, "The site it redirected to")
    add_finding(result, "good", "The link opened and the site responded.", 0)

    # 3. What kind of site is it?
    if final_domain.endswith("gov.za"):
        add_finding(result, "good", "This is a South African government (.gov.za) website. These are hard to fake.", -20)
    elif final_domain in JOB_BOARDS:
        add_finding(result, "info", f"This is on {final_domain}, an established job board. Scam ads still sometimes appear there, so also check the company's own website.")
    elif domain not in FREE_OR_SOCIAL_SITES:
        check_domain_age(final_domain, result)

    # 4. Read the page itself
    title, text, links = read_page(html)
    result["page_text"] = title + " " + text
    if len(text) < 200:
        add_finding(result, "info", "The page shows very little text. Jobs may load with JavaScript, so we could not read them.")

    for key in patterns:
        if re.search(patterns[key], result["page_text"].lower()):
            result["matches"].append(key)
    if len(result["matches"]) > 0:
        add_finding(result, "warn", f"The page text matches {len(result['matches'])} red flag(s) from the list below. We ticked them for you.")

    for email_domain in re.findall(r"[\w.+-]+@([\w-]+\.[\w.-]+)", html):
        if email_domain.lower() in FREE_EMAIL_DOMAINS:
            add_finding(result, "warn", f"The page lists a free email address ({email_domain.lower()}). Companies normally use an email that matches their website.")
            break

    # 5. Is the job link on the company's own website?
    if company_site != "":
        company_domain = registered_domain(urlparse(company_site).hostname or "")
        if final_domain == company_domain:
            add_finding(result, "good", "The job link is on the company's own website.", -10)
        elif final_domain not in JOB_BOARDS:
            add_finding(result, "warn", f"The job link ({final_domain}) is not on the company's own website ({company_domain}).", 15)


def check_company_site(url, job_title, result):
    host = (urlparse(url).hostname or "").lower()
    domain = registered_domain(host)
    check_lookalike(host, domain, result, "The company website you entered")

    try:
        final_url, html = fetch(url)
    except Exception:
        add_finding(result, "warn", "Could not open the company website you entered. Check the spelling of the address.", 10)
        return
    add_finding(result, "good", f"The company website ({domain}) opened.", 0)

    title, home_text, links = read_page(html)

    # Find the careers page: look for links with career words in them
    career_pages = []
    for address, link_text in links:
        looks_like_careers = False
        for word in CAREER_WORDS:
            if word in address.lower() or word in link_text.lower():
                looks_like_careers = True
        full_address = urljoin(final_url, address)
        same_site = registered_domain(urlparse(full_address).hostname or "") == domain
        if looks_like_careers and same_site and full_address not in career_pages:
            career_pages.append(full_address)
    career_pages = career_pages[:3]  # do not open too many pages

    if len(career_pages) == 0:  # no link found, so guess common addresses
        for path in GUESSED_CAREER_PATHS:
            career_pages.append(urljoin(final_url, path))

    all_texts = [home_text]
    opened_a_careers_page = False
    for page in career_pages:
        try:
            page_url, page_html = fetch(page)
            page_title, page_text, page_links = read_page(page_html)
            all_texts.append(page_text)
            opened_a_careers_page = True
        except Exception:
            continue  # that page did not work, try the next one

    if job_title == "":
        add_finding(result, "info", "Add the job title to check whether it is listed on the company's careers page.")
        return

    for text in all_texts:
        if title_matches(job_title, text):
            add_finding(result, "good", f"\"{job_title}\" appears on the company's own website.", -25)
            return

    total_length = 0
    for text in all_texts:
        total_length = total_length + len(text)
    if opened_a_careers_page and total_length > 400:
        add_finding(result, "warn", f"\"{job_title}\" was not found on the company's careers pages. It may be closed, or it may be fake. Phone the company using the number on its website.", 20)
    else:
        add_finding(result, "info", "Could not read the company's careers pages (they may need JavaScript). Open the website yourself and look for the job.")


# ---------- The function the app calls ----------
def verify(job_url, company_site="", job_title="", patterns=None):
    """Run all the checks and return the result dictionary."""
    if patterns is None:
        patterns = {}
    result = {"findings": [], "score": 0, "page_text": "", "matches": []}
    job_url = normalize_url(job_url)
    company_site = normalize_url(company_site)

    if job_url != "":
        check_job_link(job_url, company_site, result, patterns)
    if company_site != "":
        check_company_site(company_site, job_title.strip(), result)
    if job_url == "" and company_site == "":
        add_finding(result, "info", "Add a job link or the company's website to run the online checks.")

    result["score"] = calculate_score(result["findings"])
    return result
