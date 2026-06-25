# Pytest-BDD API Automation Framework Example

This is a small but real framework pattern for API automation using `pytest-bdd`.
It separates readable BDD scenarios from API calling code, business workflows, test data, and validations.

## Structure

```text
features/                       Gherkin feature files
tests/step_defs/                pytest-bdd step definitions only
src/api_automation/clients/     raw API clients
src/api_automation/services/    business workflows
src/api_automation/validators/  reusable assertions
src/api_automation/builders/    payload builders and test data helpers
src/api_automation/config/      environment configuration
src/api_automation/models/      shared context objects
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Run everything:

```bash
pytest
```

Run against a specific environment:

```bash
pytest --env=sit
pytest --env=uat
pytest --env=prod
```

Run only E2E tests:

```bash
pytest -m e2e
```

Run only functional API validation tests:

```bash
pytest -m api_validation
```

## CI/CD

### Jenkins

Jenkins pipeline file:

```text
Jenkinsfile
```

The Jenkins job has two parameters:

```text
TARGET_ENV: sit | uat | prod
PYTEST_MARKER: optional, for example e2e or api_validation
```

Recommended Jenkins plugins:

```text
Pipeline
Git
JUnit
HTML Publisher
Allure Jenkins Plugin
AnsiColor
```

Minimal Jenkins setup on macOS:

```bash
brew install jenkins-lts
brew services start jenkins-lts
```

Then open:

```text
http://localhost:8080
```

Get the initial admin password:

```bash
cat ~/.jenkins/secrets/initialAdminPassword
```

Basic job setup:

```text
1. Create New Item
2. Select Pipeline
3. Choose Pipeline script from SCM
4. Add your Git repository URL
5. Set Script Path to Jenkinsfile
6. Save and Build with Parameters
```

On Linux/Ubuntu, install Jenkins roughly like this:

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
```

Then install Jenkins from the official Jenkins package repository and start the service:

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

Open:

```text
http://<server-ip>:8080
```

CI output from Jenkins:

```text
reports/api_automation_report.html
reports/junit.xml
reports/logs/
reports/allure-results/
reports/allure-report/
```

If the Allure Jenkins plugin is installed, Jenkins will render the Allure report directly from `reports/allure-results/`.

### GitHub Actions

GitHub Actions workflow:

```text
.github/workflows/api-automation.yml
```

The pipeline runs automatically on pull requests and pushes to `main` or `master`.
It can also be triggered manually from GitHub Actions with:

```text
environment: sit | uat | prod
marker: e2e | api_validation | blank for all tests
```

CI installs the Allure CLI, runs pytest, generates the Allure HTML report automatically, and uploads these artifacts:

```text
pytest-html-report-<env>
junit-report-<env>
execution-logs-<env>
allure-results-<env>
allure-html-report-<env>
```

Optional GitHub repository secrets can override environment JSON values:

```text
API_BASE_URL
API_USERNAME
API_PASSWORD
API_TIMEOUT_SECONDS
```

## Reports And Logs

Reports are generated automatically after every run:

```text
reports/allure-results/              Allure result files with API attachments
reports/api_automation_report.html   Human-readable HTML report
reports/junit.xml                    CI-friendly JUnit report
reports/logs/pytest.log              Pytest execution log
reports/logs/api_automation_*.log    Per-run API request/response log
```

The framework automatically runs this command at the end of the pytest session when the Allure command-line tool is installed:

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

That creates:

```text
reports/allure-report/index.html
```

If the `allure` command is not installed, the tests still pass and `reports/allure-results/` is created. Install the Allure CLI once, then rerun pytest:

```bash
brew install allure
pytest --env=uat
```

To open an interactive report manually:

```bash
allure serve reports/allure-results
```

The framework also logs every API request and response from `BaseClient`.
Sensitive fields such as `password`, `Authorization`, tokens, card numbers, and SSNs are masked.

Example log line:

```text
API Request | method=POST url=https://dummyjson.com/auth/login headers={} body={"username": "emilys", "password": "***MASKED***"}
API Response | status_code=200 elapsed_ms=420.4 url=https://dummyjson.com/auth/login body={"accessToken": "***MASKED***"}
```

## Environment Config

Environment files live here:

```text
src/api_automation/config/environments/sit.json
src/api_automation/config/environments/uat.json
src/api_automation/config/environments/prod.json
```

Each file controls:

```json
{
  "base_url": "https://dummyjson.com",
  "timeout_seconds": 15,
  "username": "emilys",
  "password": "emilyspass"
}
```

You can override values at runtime with environment variables:

```bash
API_BASE_URL=https://example.com API_USERNAME=my_user API_PASSWORD=my_pass pytest --env=uat
```

## API Used

The sample uses the public DummyJSON API:

- `POST https://dummyjson.com/auth/login`
- `GET https://dummyjson.com/auth/me`
- `POST https://dummyjson.com/carts/add`

The cart API is used as a stand-in for a mutual fund order API so the framework stays runnable without private banking APIs.

## Main Rule

Step definitions should read like glue code. They should not contain raw `requests` calls or large assertion blocks.

```python
@when("the investor places a buy order")
def place_order(context, order_service):
    context.order_response = order_service.place_buy_order(context.access_token)
```

The actual work belongs in clients, services, builders, and validators.
