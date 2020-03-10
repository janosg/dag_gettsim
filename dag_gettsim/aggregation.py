def disposable_income(income, wealth, income_taxes, wealth_taxes, benefits, params):
    """Calculate disposable income.

    Args:
        income (pd.Series)
        taxes (pd.Series)
        benefits (pd.Series)
        params (pd.Series)

    Returns:
        disposable_income (pd.Series)

    """
    return income + wealth - income_taxes - wealth_taxes + benefits
