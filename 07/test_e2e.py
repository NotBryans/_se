import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def server():
    # Start Flask server in background for E2E testing
    proc = subprocess.Popen(["python", "app.py"])
    time.sleep(1.5)
    yield "http://127.0.0.1:5000"
    proc.terminate()
    proc.wait()

def test_e2e_add_task_in_headless_browser(server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(server)

        # Verify page header loaded
        assert page.locator("#app-title").inner_text() == "Task Manager"

        # Type a new task and click the Add button
        page.fill("#task-input", "Complete Playwright E2E Test")
        page.click("#add-btn")

        # Wait for the new task item to render in the DOM list
        page.wait_for_selector(".task-item")
        items = page.locator(".task-item").all_inner_texts()
        assert "Complete Playwright E2E Test" in items

        browser.close()