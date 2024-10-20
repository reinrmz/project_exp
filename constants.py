

class TAX_CALCULATOR:
    app_version = 'v1.0.0'

    period_lkp = {
        "period_1": '1st (April-May-June)',
        "period_2": '2nd (July-August-September)',
        "period_3": '3rd (October-November-December)',
        "period_4": 'Annual (April)'
    }

    table_formatting = {
            'Income': "₱ {:,.2f}",
            'Deductible': "₱ {:,.2f}",
            'Taxable': "₱ {:,.2f}",
            'Payable': "₱ {:,.2f}"
        }
    
class EXPENSE_TRACKER:
    app_version = 'v1.0.0'
    source_path = r"E:\Files\sample.xlsx"
    sheet_name = 'income and expenses'

class GENERAL_FORMATTING:
    
    peso_format = '&#8369;'
