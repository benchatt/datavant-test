import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime, timedelta
from constants.textlabels import Intl

TODAY = datetime.now()


@pytest.fixture()
def i18n() -> Intl:
    intl = Intl()
    return intl.text


@pytest.fixture()
def testcase() -> dict:
    return {
        "depart_station": "Lagos",
        "arrive_station": "Porto - Campanha",
        "depart_date": TODAY + timedelta(days=3),
        "return_date": TODAY + timedelta(days=5),
    }


@pytest.mark.parametrize("lg", ["en"])
def test_search_tickets(
    playwright: Playwright, i18n: Intl, testcase: dict, lg: str
) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"https://www.cp.pt/passageiros/{lg}/{i18n[lg]['buy-tickets']}")

    page.get_by_placeholder(i18n[lg]["from"]).click()
    page.get_by_placeholder(i18n[lg]["from"]).fill(testcase["depart_station"])
    page.get_by_placeholder(i18n[lg]["to"]).click()
    page.get_by_placeholder(i18n[lg]["to"]).fill(testcase["arrive_station"])

    depart_day = str(testcase["depart_date"].day)
    return_day = str(testcase["return_date"].day)
    page.get_by_placeholder(i18n[lg]["depart_date"], exact=True).click()
    if int(depart_day) < TODAY.day:
        page.get_by_title(i18n[lg]["next_month"]).click()
    page.locator("#datepicker-first_table").get_by_text(depart_day, exact=True).click()
    page.get_by_placeholder(i18n[lg]["return_date"], exact=True).click()
    if int(return_day) < TODAY.day:
        page.get_by_title(i18n[lg]["next_month"]).click()
    page.locator("#datepicker-second_table").get_by_text(return_day, exact=True).click()
    page.get_by_role("button", name=i18n[lg]["submit"]).click()

    page.wait_for_url("https://venda.cp.pt/bilheteira/comprar/escolher-viagem*")
    expect(
        page.locator("td").locator("span", has_text=i18n[lg]["service"])
    ).to_be_visible()
    expect(
        page.locator("td").locator("span", has_text=i18n[lg]["outbound"].upper())
    ).to_be_visible()
    expect(
        page.locator("td").locator("span", has_text=i18n[lg]["inbound"].upper())
    ).to_be_visible()
    page.get_by_role("button", name=i18n[lg]["cancel"]).click()

    page.wait_for_load_state()
    assert (
        page.get_by_placeholder(i18n[lg]["from"]).input_value()
        == testcase["depart_station"]
    )
    assert (
        page.get_by_placeholder(i18n[lg]["to"]).input_value()
        == testcase["arrive_station"]
    )
    assert (
        depart_day
        in page.get_by_placeholder(i18n[lg]["depart_date"], exact=True).input_value()
    )
    assert (
        return_day
        in page.get_by_placeholder(i18n[lg]["return_date"], exact=True).input_value()
    )
    expect(page.locator("ul").filter(has_text="Buy Tickets").nth(1)).to_be_visible()

    # ---------------------
    context.close()
    browser.close()
