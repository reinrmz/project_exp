

class STATIC_TITLES:
    app_version = 'v1.0.0'
    page_title = 'Personal Expense Tracker'

    period_lkp = {
        "period_1": '1st (April-May-June)',
        "period_2": '2nd (July-August-September)',
        "period_3": '3rd (October-November-December)',
        "period_4": 'Annual (April)'
    }


class STATIC_PATHS:
    source_path = r"E:\Files\sample.xlsx"


class STATIC_FORMATTING:
    table_formatting = {
            'Income': "₱ {:,.2f}",
            'Deductible': "₱ {:,.2f}",
            'Taxable': "₱ {:,.2f}",
            'Payable': "₱ {:,.2f}"
        }
