def income_taxes(income, params):
    """Calculate the income tax based on income and params.

    Args:
        income (pd.Series)
        params (pd.Series)

    Returns
        pd.Series: the income taxes

    """
    return params.income_tax * income


def wealth_taxes(wealth, params):
    """Calculate the wealth tax based on wealth and params.

    Args:
        wealth (pd.Series)
        params (pd.Series)

    Returns:
        pd.Series: the wealth taxes

    """
    return params.wealth_tax * wealth
