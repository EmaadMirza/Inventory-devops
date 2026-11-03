"""Capture real localhost Jenkins pages using installed Chrome in an isolated context."""
import base64
from datetime import datetime, timezone
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

root = Path(__file__).resolve().parent.parent
password = (root / ".secrets/jenkins-admin-password").read_text().strip()
authorization = "Basic " + base64.b64encode(("emaad:" + password).encode()).decode()
base = "http://127.0.0.1:18081"
records = []
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    context = browser.new_context(viewport={"width":1440,"height":1000},
                                  extra_http_headers={"Authorization":authorization})
    page = context.new_page()
    response = page.goto(base + "/job/Mini-Inventory/2/", wait_until="networkidle")
    assert response.status == 200
    text = page.locator("body").inner_text()
    assert "Started by an SCM change" in text and "mini-inventory.jar" in text and "Success" in text
    page.screenshot(path=str(root / "evidence/jenkins-browser-1-build.png"), full_page=True)
    records.append({"url":page.url,"screenshot":"jenkins-browser-1-build.png","checks":["Success","SCM cause","archived JAR"]})
    page.locator('a[href="/job/Mini-Inventory/2/testReport"]').first.click()
    page.wait_for_load_state("networkidle")
    text = page.locator("body").inner_text()
    print("TEST PAGE:", text)
    assert "All 7 tests are passing" in text
    page.screenshot(path=str(root / "evidence/jenkins-browser-2-tests.png"), full_page=True)
    records.append({"url":page.url,"screenshot":"jenkins-browser-2-tests.png","checks":["7 tests passing","0 failed","0 skipped"]})
    page.goto(base + "/job/Mini-Inventory/", wait_until="networkidle")
    print("JOB CONFIG LINKS:", page.locator("a").evaluate_all('(links) => links.map(a=>({text:a.innerText,url:a.getAttribute("href")})).filter(a=>/config/i.test(a.text+" "+a.url))'))
    (root / ".lab/jenkins-job-dom.txt").write_text(page.locator("body").inner_text(),encoding="utf-8")
    page.locator('a[href="/job/Mini-Inventory/configure"]').click()
    try:
        page.wait_for_load_state("networkidle",timeout=15000)
    except PlaywrightTimeout:
        # Jenkins performs background form validation; inspect the rendered form itself.
        page.locator('form').first.wait_for(state="visible")
    text = page.locator("body").inner_text()
    (root / ".lab/jenkins-config-dom.txt").write_text(text,encoding="utf-8")
    print("CONFIG HEADINGS:",page.locator('h1,h2,h3').all_text_contents())
    print("CONFIG FORM:",text[-9000:])
    page.screenshot(path=str(root / "evidence/jenkins-browser-3-config.png"),full_page=True)
    records.append({"url":page.url,"screenshot":"jenkins-browser-3-config.png"})
    values = page.locator('input').evaluate_all('(els)=>els.map(e=>e.value)')
    assert 'https://github.com/EmaadMirza/Inventory-devops.git' in values
    assert '*/main' in values and 'Jenkinsfile' in values
    schedules = page.locator('textarea').evaluate_all('(els)=>els.map(e=>e.value)')
    assert '* * * * *' in schedules
    page.set_viewport_size({"width":1440,"height":1400})
    page.get_by_text('Pipeline',exact=True).last.evaluate("el=>el.scrollIntoView({block:'start'})")
    page.screenshot(path=str(root / 'evidence/jenkins-browser-4-pipeline.png'))
    records.append({"url":page.url,"screenshot":"jenkins-browser-4-pipeline.png","checks":["GitHub URL","main branch","Jenkinsfile"]})
    page.get_by_text('Triggers',exact=True).last.evaluate("el=>el.scrollIntoView({block:'start'})")
    page.screenshot(path=str(root / 'evidence/jenkins-browser-5-polling.png'))
    records.append({"url":page.url,"screenshot":"jenkins-browser-5-polling.png","checks":["once-per-minute SCM polling"]})
    (root / "evidence/jenkins-browser-provenance.json").write_text(json.dumps({
        "captured_utc":datetime.now(timezone.utc).isoformat(),
        "captured_local":datetime.now().astimezone().isoformat(),
        "method":"Playwright with installed Google Chrome, headless, isolated temporary context",
        "source":"Live Jenkins HTTP pages; no mocked responses or image alterations",
        "build_execution_date":"2026-11-03", "pages":records},indent=2),encoding="utf-8")
    browser.close()
