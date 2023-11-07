## QUICKSTART

Use your favorite Python environment manager to install the requirements in requirements.txt. If you use
pipenv, the Pipfile and lock are available already.

Then:

* `playwright install`

Run tests:

* `pytest tests`

Check out the PyTest (command-line options)[https://docs.pytest.org/en/7.3.x/how-to/usage.html#usage].

### Question 2

Oddities:

* Date-picker doesn't like to pop up--it feels like you have to try multiple times whenever you want to
use it.
* Typing a station name doesn't always reveal an autocomplete selectbox.
* At least once, button highlighting failed to trigger on mouseover. I wasn't able to consistently repro
that, though.
* Dates are returned in a non-localized way, even though the months are in the right language.
* Page loads are slow, this may just be the site being in Portugal.

### Question 3

Improvements for Automated Testing:

* Test IDs. Test IDs. And more Test IDs.
* On this note, the Test IDs should follow a basic, intuitive pattern based on the DOM structure.
* There are a lot of typographical idiosyncrasies I'd clean up: "X Cancel", "Submit »" and "From " stand out.
* One improvement for general UX is that I might reword the English site a little.

#### Websites used

* https://playwright.dev/python/docs/api/class-page to remind of certain method names
* https://playwright.dev/python/docs/api/class-locator same as above
* https://stackoverflow.com/questions/64790747/using-playwright-for-python-how-to-i-read-the-content-of-an-input-box to remind me what input_value was called.
* https://docs.pytest.org/en/7.3.x/how-to/parametrize.html
