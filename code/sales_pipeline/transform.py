"""
transform.py — the **T** in ETL.

Transform is where messy input becomes numbers you can do arithmetic on. Every
function in here takes values in and returns a value out: no `input()`, no
`print()`, no files. That is what makes them easy to unit test and easy to reuse
from *any* report.

The one rule that matters: **never crash on bad data.** A single row with a price
of `"N/A"` must not take down a report covering hundreds of good rows. When a value
cannot be read, coerce it to zero and keep going.

Your job: implement the seven functions below so the Unit Tests in
tests/test_unit.py all pass. Each docstring says exactly what the function should
return, gives worked examples, and ends with a **How to build it** section — read
that before you start typing. Replace the `# TODO` line (and the `pass`) with your
code.

Write them in the order the README's build order table gives. Nothing later needs
anything you have not written yet.
"""


def clean_currency(value) -> float:
    """Convert a raw price into a float, using 0.0 when it cannot be read.

    Prices arrive in several shapes, and some do not arrive at all. Strip the
    decoration (`$` and `,`) before handing the text to `float()`.

    Examples:

    input:  "$12.50"     output: 12.5
    input:  "15.00"      output: 15.0
    input:  "$1,200.00"  output: 1200.0
    input:  15.0         output: 15.0
    input:  None         output: 0.0
    input:  ""           output: 0.0
    input:  "N/A"        output: 0.0

    How to build it:

    - Handle `None` first, on its own line, before you touch the value at all.
    - `str(value)` makes everything after it work whether the price arrived as
      text or as a float. Then chain `.replace()` twice to drop the `$` and the
      `,`, and finish with `.strip()`.
    - Wrap the `float()` call in `try` / `except ValueError`, and return `0.0`
      from the `except`. That is the line that stops one `"N/A"` from killing a
      report of 400 good rows.
    """
    # TODO: your code here
    try:
        if isinstance(value, str):
            value = value.replace("$", "").replace(",", "")
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def clean_quantity(value) -> int:
    """Convert a raw quantity into an int, using 0 when it cannot be read.

    Examples:

    input:  "4"     output: 4
    input:  4       output: 4
    input:  " 7 "   output: 7
    input:  "0"     output: 0
    input:  None    output: 0
    input:  ""      output: 0
    input:  "one"   output: 0

    How to build it:

    - Exactly the same shape as `clean_currency`: guard `None`, then `try` the
      conversion and return `0` from `except ValueError`.
    - There is no decoration to strip off a quantity, so this one is shorter —
      `int(str(value).strip())` is the whole conversion.
    - Do not try to translate `"one"` into `1`. A word in a number field is bad
      data, and bad data becomes `0`.
    """
    # TODO: your code here
    if value is None:
        return 0
    try:
        return int(str(value).strip())
    except ValueError:
        return 0

def clean_sales_data(raw_data: list[dict]) -> list[dict]:
    """Clean every raw row and add the revenue it earned.

    Each cleaned row keeps `date` and `item` as they arrived, replaces `price` and
    `qty` with real numbers, and gains one new key, `total_revenue` (price × qty).

    Example:

    input:  [{"date": "2023-10-01", "item": "Widget A", "price": "$12.50", "qty": "4"}]
    output: [{'date': '2023-10-01', 'item': 'Widget A', 'price': 12.5, 'qty': 4,
              'total_revenue': 50.0}]

    How to build it:

    - **Call the functions you already wrote.** The cleaning here is
      `clean_currency(row["price"])` and `clean_quantity(row["qty"])` — nothing
      more. If you catch yourself typing `.replace("$", "")` in this function, you
      are re-doing work that already has a home, and now there are two places to
      fix when the rules change.
    - The shape is: empty list before the loop, one new dictionary built per row,
      `append` it, `return` the list after the loop.
    - Build a **new** dictionary rather than editing `row` in place, so the raw
      data stays untouched for anyone who wants to compare against it.
    - Add `total_revenue` *after* that dictionary exists, so you can multiply the
      cleaned `price` and `qty` you just stored instead of cleaning the raw values
      a second time.
    """
    # TODO: your code here
    cleaned_data = []

    for row in raw_data:
        cleaned_row = {
            "date": row["date"],
            "item": row["item"],
            "price": clean_currency(row["price"]),
            "qty": clean_quantity(row["qty"])
        }

        cleaned_row["total_revenue"] = (
            cleaned_row["price"] * cleaned_row["qty"]
        )

        cleaned_data.append(cleaned_row)

    return cleaned_data


def calculate_total_revenue(cleaned_data: list[dict]) -> float:
    """Add up the revenue of every cleaned row.

    This is an accumulator: start the running total at 0 and add each row to it.

    Example:

    input:  [{'total_revenue': 50.0, ...}, {'total_revenue': 30.0, ...}]
    output: 80.0

    How to build it:

    - The accumulator pattern in three parts: a `total` variable *before* the
      loop, `+=` *inside* it, `return` *after* it. Declaring `total` inside the
      loop resets it every pass — a classic way to end up with just the last row.
    - Start at `0`, not `1`. You are summing, not multiplying, so an empty list
      should come back `0.0`.
    - Nothing needs cleaning here. These rows already went through
      `clean_sales_data`, so `row["total_revenue"]` is a number you can trust.
    """
    # TODO: your code here
    total = 0                    

    for row in cleaned_data:     
        total += row["total_revenue"]        

    return total                 


def summarize_by_item(cleaned_data: list[dict]) -> list[dict]:
    """Roll the row-level data up to one entry per item.

    This is the *group by* that every analytics tool does for you and that you
    should be able to do by hand once: use a dictionary keyed by item name as the
    accumulator, then turn its values back into a list.

    The result is sorted by revenue, highest first. Ties break alphabetically by
    item name so the order is always the same for the same data.

    Example:

    output: [{'item': 'Gizmo Pro', 'units_sold': 1, 'revenue': 1200.0},
             {'item': 'Widget A', 'units_sold': 10, 'revenue': 125.0}]

    How to build it:

    - The accumulator is a **dictionary keyed by item name**, not a list. That is
      the whole trick: it lets you find the running total for "Widget A" instantly,
      no matter where its rows appear in the data.
    - For each row, do two separate things. First, if the item is not in your
      dictionary yet, add it with zeros. Second — not in an `else` — `+=` the row's
      `qty` and `total_revenue` into it. Keeping *create* and *update* apart is what
      makes the first row for an item behave like every other row.
    - After the loop, `totals.values()` holds your entries. Wrap that in `sorted()`
      to get a list back in the order you want.
    - Sorting by one key descending and another ascending sounds fiddly, but
      negating the number does it:
      `key=lambda entry: (-entry["revenue"], entry["item"])`. The tuple reads as
      "sort by revenue, biggest first, and use the name to break ties."
    """
    # TODO: your code here
    totals = {}

    for row in cleaned_data:
        item = row["item"]

        if item not in totals:
            totals[item] = {
                "item": item,
                "units_sold": 0,
                "revenue": 0.0
            }

        totals[item]["units_sold"] += row["qty"]
        totals[item]["revenue"] += row["total_revenue"]

    return sorted(
        totals.values(),
        key=lambda entry: (-entry["revenue"], entry["item"])
    )


def summarize_by_day(cleaned_data: list[dict]) -> list[dict]:
    """Roll the row-level data up to one entry per day."""

    totals = {}

    for row in cleaned_data:
        date = row["date"]

        if date not in totals:
            totals[date] = {
                "date": date,
                "units_sold": 0,
                "revenue": 0.0
            }

        totals[date]["units_sold"] += row["qty"]
        totals[date]["revenue"] += row["total_revenue"]

    return sorted(
        totals.values(),
        key=lambda entry: entry["date"]
    )

def find_top_entry(summary: list[dict], field: str = "revenue") -> dict:
    """Return the entry of `summary` with the largest value in `field`."""

    if not summary:
        return {}

    best = summary[0]

    for entry in summary:
        if entry[field] > best[field]:
            best = entry

    return best
