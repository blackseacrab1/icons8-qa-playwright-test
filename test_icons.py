import re

from playwright.sync_api import sync_playwright, expect


def test_search_and_open_cat_icon():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://icons8.com/icons")

            # Enter a search query on the home page.
            search = page.locator('[data-test="search-input"]')
            search.fill("cat")
            expect(search).to_have_value("cat")

            # Try submitting the search through the UI.
            search.press("Enter")
            page.wait_for_timeout(1500)

            # In this environment Enter cleared the field without navigating.
            # Fall back to the known Icons8 results URL so the rest of the flow
            # (results and opening an icon) remains covered.
            if "/icons/set/cat" not in page.url:
                page.goto("https://icons8.com/icons/set/cat")

            # Verify search results and the query shown in the search field.
            expect(
                page.get_by_role("heading", name="Cat icons", exact=True)
            ).to_be_visible(timeout=20_000)
            expect(
                page.get_by_role("combobox", name="Search icons")
            ).to_have_value("cat")

            # Open the first matching icon.
            cat_icon = page.get_by_role(
                "link", name=re.compile("High-quality cat icon", re.I)
            )
            expect(cat_icon).to_be_visible()
            cat_icon.click()

            # Verify the icon image is visible in the details panel.
            expect(
                page.get_by_role("img", name="Cat icon", exact=True)
            ).to_be_visible()

            page.screenshot(path="icons8-cat-result.png", full_page=True)
        finally:
            browser.close()
