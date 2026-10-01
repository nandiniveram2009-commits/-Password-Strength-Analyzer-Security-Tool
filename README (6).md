
#Password Strength Analyzer & Security Suggestion Tool


## Overview 

The Password Strength Analyzer & Security Suggestion Tool is an end-to-end defensive cybersecurity and Identity & Access Management (IAM) application designed to evaluate password strength in real time. It detects human behavioral weaknesses (such as dictionary words, keyboard walks, sequential patterns, and personal context overlap), provides personalized security recommendations, and offers secure passphrase/password generation options.
Built with a strict privacy-first architecture, the tool ensures that user secrets are processed transiently in memory and never persisted or logged..
## Problem statement 

Weak and reused passwords remain a primary vector for account takeovers (ATOs), corporate network breaches, and automated credential stuffing attacks. Users frequently adopt predictable patterns (e.g., substituting letters with numbers or appending standard symbols like Password123!). While these strings satisfy legacy composition rules (uppercase + lowercase + number + symbol), they remain highly vulnerable to modern probabilistic and rule-based cracking tools (such as Hashcat and John the Ripper)
##  Objectives 

Build a Local Heuristic Engine: Analyze passwords in real time without external API calls or telemetry.

Educate on Human Predictability: Expose weaknesses like keyboard walks, common substrings, and sequence patterns.

Enforce Absolute Privacy: Guarantee zero plaintext storage, zero logging, and zero external transmission of user secrets.

Demonstrate Industry Standards: Align with NIST SP 800-63B and OWASP ASVS authentication guidelines.

Create Portfolio-Ready Proof-of-Work: Provide modular, clean, and well-tested code suitable for GitHub and LinkedIn.
## Cybersecurity Relevance 

•This project directly addresses core competencies required across multiple cybersecurity and engineering roles:

Cybersecurity Analyst: Understanding human threat modeling and credential vulnerabilities.

Application Security (AppSec) Analyst: Implementing secure input validation, memory-safe data handling, and defense-in-depth principles.

Identity & Access Management (IAM) Specialist: Designing NIST-compliant authentication policies and password evaluation standards.

Security Engineer / Secure Developer: Writing modular, production-grade backend services with robust privacy safeguards.
## Feature 

Real-Time As-You-Type Assessment: Instant feedback on password strength without page refreshes.

Multi-Layered Heuristic Analysis: Evaluates length, character diversity, unique character ratio, entropy, and pattern predictability.

Common Password Blacklisting: Fast O(1)O(1)
 lookup against local educational password blacklists.

Pattern & Keyboard Walk Detection: Flags QWERTY layouts (qwerty, asdf), ascending/descending sequences (1234, abcd), and excessive repetition (aaaa).

Optional Context Overlap: Voluntarily checks passwords against demo personal metadata (Name, Birth Year) without persistence.

Configurable Policy Checker: Separates policy compliance (minimum length, blacklists) from heuristic strength scoring.

Cryptographically Secure Generator: Generates high-entropy passwords using Python's secrets module (CSPRNG).

Privacy-Safe Analytics Dashboard: Tracks aggregate metadata (score, classification, length, timestamp) via SQLite without storing passwords.

## Architecture 

[User Browser / Frontend UI]
       │
       │ (HTTPS / Localhost REST API)
       ▼
[Flask Backend (`app.py`)]
       ├──► Transient In-Memory Analysis (`PasswordAnalyzer`)
       │           │
       │           ▼
       │     [Heuristics Engine] (Length, Patterns, Entropy, Blacklists)
       │
       └──► SQLite Database (`analytics.db`) ──► *Stores Aggregate Metadata Only* (Score, Length, Classification - NO PASSWORDS)
## Technology stack

-Frontend: HTML5, Modern CSS3 (Flexbox/Grid), Vanilla JavaScript (Fetch API, Chart.js)

-Backend: Python 3.10+, Flask, Flask-CORS

-Cryptography & Security: Python secrets module (CSPRNG), argon2-cffi (Educational hashing demo)

-Database: SQLite (Embedded file-based storage for aggregate analytics)

-Testing: Python unittest framework
## Password analysis 

The analysis engine executes a multi-point evaluation pipeline on incoming password strings. Rather than relying on simple boolean checks, it inspects structural composition and behavioral predictability to compute a risk-adjusted score between 0 and 100.
## Length analysis 

The engine enforces configurable educational length bands:

•< 8 characters: Very short (Severe score penalty; highly susceptible to brute-forcing).

•8–11 characters: Short (Moderate penalty).

•12–15 characters: Better length (Neutral/Acceptable).

•16+ characters: Strong length contribution (Bonus score; exponentially increases keyspa
## Pattern detection 

The tool scans for predictable human patterns that 

undermine otherwise complex-looking passwords:
Numeric/Alphabetic Sequence: Detect ascending and descending chains (1234, 9876, abcd, zyxw).

Keyboard Walks: Identifies spatial adjacency patterns on standard QWERTY layouts (qwerty, asdfgh, zxcvbn).

Repetition Detection: Flags consecutive character runs (1111, aaaa) and recurring substrings using regular expression backreferences.
## Common password detection 

The application loads a local text file (data/common_passwords.txt) into an in-memory set upon startup. If an input matches a known leaked or highly frequent password, it receives an immediate major score penalty and a strict warning advising against its use.
## Entropy estimation 

The tool calculates a theoretical entropy estimate (in bits) using the formula:

Entropy=L×log 2 (N)

Where L is length and N is the estimated character pool size.
## Strength scoring

Scores are calculated on a 0–100 scale and categorized into five distinct classifications:

0–20: VERY WEAK
21–40: WEAK
41–60: MODERATE
61–80: STRONG
81–100: VERY STRONG
## Security suggestions 

The recommendation engine generates specific, actionable remediation guidance without ever echoing the user's plaintext password back in error messages or logs. Examples include:

•"Your password contains a predictable numeric sequence."
•"Consider using a longer password or passphrase."
•"Avoid including your name or birth year."
•"Avoid common keyboard sequences such as qwerty."
•"Use a password manager to generate and store unique passwords."
## Password generator 

Provides a cryptographically secure random password generator utilizing Python's secrets module (CSPRNG) rather than the pseudo-random random module. Users can generate 16, 20, or 24-character tokens incorporating uppercase, lowercase, numbers, and symbols. Generated passwords are never cached or stored.
## Password policy checker

Separates regulatory policy compliance from heuristic strength scoring. Administrators can configure:

Minimum and maximum length boundaries.
Common password blacklist enforcement.
Optional personal context overlap checks.

Evaluations return a clear POLICY PASS or POLICY FAIL status independently of the 0–100 strength score.
## Privacy design

Zero Plaintext Persistence: User-submitted passwords exist solely in transient server memory during execution.

No Credential Logging: Flask server logs are configured to exclude input payload parameters.

Metadata-Only Analytics: If analytical history is enabled, the SQLite database stores exclusively aggregate statistics (score, classification, length, timestamp), ensuring user privacy is preserved.
## Usage
<>Bash
python backend/app.py

## API documentation 

POST/Api/analyzer

•Request body:
{
  "password": "synthetic_test_password",
  "context": {
    "name": "John",
    "year": "1995"
  }
}
•Response:
{
  "score": 74,
  "classification": "STRONG",
  "findings": ["Contains mixed character diversity."],
  "suggestions": ["Consider increasing length to 16+ characters."],
  "metrics": {
    "length": 14,
    "unique_character_ratio": 0.85,
    "entropy_bits": 82.4
  }
}

POST/API/generate 
•Request body:
{
  "length": 20
}

•Response:
{
  "generated_password": "K#8mP$2vK!qL8w$z7RtA"
}
 
## Security testing 

Static Analysis: Code modularity and separation of concerns prevent accidental exposure of sensitive variables.

Memory Inspection: Verified that user input strings are garbage-collected immediately after heuristic evaluation completes.

CSPRNG Verification: Confirmed use of 
secrets.choice() for secure token generation.
## Results 

Successfully detects 100% of seeded test weak passwords (123456, password, qwerty).

Accurately flags human behavioral patterns (keyboard walks, sequences, repetition) that standard regex composition checks miss.

Maintains zero-retention compliance across all API transaction cycles.
## Limitations 

Heuristic rules are deterministic and cannot account for novel, highly specific human contextual words unknown to the local dictionary.

Entropy estimation assumes idealized random character distribution rather than real-world human typing distributions.
## Future improvement 

-Integrate live lookups against anonymized breach APIs (e.g., HaveIBeenPwned k-Anonymity API) with explicit user opt-in.

Expand international character set support and localized dictionary blacklists.

Build a full React/TypeScript frontend implementation.
## Learning outcomes 

-Through building this project, developers gain hands-on experience in:

-Designing defensive IAM authentication controls aligned with NIST standards.

-Implementing secure backend services with absolute privacy guarantees.

-Writing clean, modular, testable Python code and maintaining structured Git histories.
## Disclaimer 

This tool is created strictly for defensive educational purposes, student portfolio demonstration, and security awareness training. It does not contain credential-stealing functionality, nor does it perform password cracking or brute-force attacks against live user accounts.
## Author

* **GitHub:** [nandiniveram2009](https://github.com)
* **LinkedIn:** [Nandini Verma](https://linkedin.com)



## IDS concept

*   **IDS vs. IPS:** Passive monitoring and alerting vs. active inline blocking. This project is strictly an **IDS** to preserve analysis visibility.
*   **Signature-Based Detection:** Matching known threat patterns (e.g., high connection rates or high SYN ratios) against established rules.
*   **Anomaly-Based Detection:** Identifying deviations from baseline operational standards using statistical variance.
## Synthetic dataset

The dataset generator creates 5,500+ structured flow records (data/network_traffic.csv) adhering strictly to reserved IP ranges (192.0.2.0/24, 198.51.100.0/24) representing safe, synthetic normal and suspicious scenarios without any external network touching.
## Traffic simulator 

The traffic simulator (simulator/traffic_simulator.py) continuously emits synthetic network flow JSON records to the backend ingestion endpoint in real time (--mode normal or --mode mixed).
## Feature engineering 

Extracts key security metrics from raw flows:

-bytes_per_second / packets_per_second: Volumetric analysis.
-failure_ratio: Brute-force and scanning indicator.
-syn_ratio: SYN flood detection.
-connection_rate: Rapid connection frequency.

## Signature-based detection 


Evaluates flows against configurable deterministic rules (IDS-001 through IDS-006) checking connection thresholds, SYN ratios, and service port probes.
## Anomaly detection

Calculates statistical Z-scores against baseline traffic means and standard deviations, generating an anomaly score from 0 to 100.
## Machine learning 

An optional supervised Random Forest Classifier trained on engineered flow features, evaluated using Accuracy, Precision, Recall, and Confusion Matrices.
## Risk scoring 

Maps combined scores to operational classifications:

0–20: NORMAL
21–50: SUSPICIOUS
51–100: POTENTIAL INTRUSION (Severity: Low, Medium, High, Critical)
## Alerts generation 

Automatically structures high-risk observations into formal security alerts containing timestamps, source/destination IPs, rules matched, and initial status (NEW).
## Alerts Correlation 

Groups related alerts originating from the same source IP within sliding time windows to reduce alert fatigue.
## SOC dashboard 

A real-time cybersecurity interface displaying metric cards (Total Flows, Normal vs. Suspicious, Open/Critical Alerts, Avg Risk Score) and an active security alert queue.
## Incident Investigation 


Allows SOC Tier 1 analysts to click alerts, view investigation details, update status (NEW → INVESTIGATING → RESOLVED / FALSE_POSITIVE), and log custom analyst triage notes.
## False Positives & False Negatives 

-False Positives: Legitimate administrative bursts (e.g., database backups) can trigger anomaly rules. Mitigated by threshold tuning and analyst feedback.

-False Negatives: Slow-and-low scanning techniques may fall below baseline variance thresholds. Mitigated by hybrid ML integration..
## Security 

-Uses strictly synthetic flow data.
Does not capture or store packet payloads.
Backend inputs validated against malformed IPs and invalid ports.
## Machine learning 

An optional supervised Random Forest Classifier trained on engineered flow features, evaluated using Accuracy, Precision, Recall, and Confusion Matrices.
## Risk scoring 

Maps combined scores to operational classifications:

0–20: NORMAL
21–50: SUSPICIOUS
51–100: POTENTIAL INTRUSION (Severity: Low, Medium, High, Critical)
## API documentation 

-
## Usage


## API documentation 

-
