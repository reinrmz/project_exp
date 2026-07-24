

class TAX_CALCULATOR:
    app_version = 'v1.0.1'

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
    
class GENERAL_FORMATTING:
    
    peso_format = '&#8369;'
