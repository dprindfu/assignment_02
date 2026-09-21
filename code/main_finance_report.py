"""
main_finance_report.py — the Finance department's report.

Finance cares about the audit trail: every transaction, and what the whole day
earned.

This file is an *interface*, not a library. Notice how little it does: it calls
the pipeline in order and arranges the output. Every calculation lives in
`sales_pipeline.transform`, every bit of formatting lives in
`sales_pipeline.display`. If you find yourself doing arithmetic in this file,
that logic belongs in the package instead — where it can be unit tested and where
Marketing can reuse it.

Before running:  pip install -r requirements.txt

    python code/main_finance_report.py        # the fixed sample data
    python code/main_finance_report.py 42     # the generated data for seed 42
"""

import sys

# --- Reading the dataset seed ----------------------------------------------------
#
# This block is GIVEN to you, in this report only. It is plumbing, not the lesson —
# but read it, because the next two reports need it and you will be writing it
# yourself by then.
#
# `sys.argv` is the list of words typed on the command line. sys.argv[0] is the
# script name, so an argument the user typed is sys.argv[1]. It arrives as a
# *string*, so it needs int(). A missing argument — or a blank one, which is what
# VS Code sends when you clear the seed prompt — means "use the sample data".
# See README Reference #7.

seed = None
if len(sys.argv) > 1 and sys.argv[1].strip() != "":
    seed = int(sys.argv[1])

from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    calculate_total_revenue,
    print_sales_table,
)


print("=== FINANCE: Daily Sales Detail ===")
print()


raw_data = get_raw_sales_data(seed)

clean_data = clean_sales_data(raw_data)
total_revenue = calculate_total_revenue(clean_data)


print_sales_table(clean_data)
print()
print(f"Total Pipeline Revenue: ${total_revenue:,.2f}")