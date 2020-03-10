def benefits(income, n_children, params):
    """Calculate benefits according to income, number of children and params.

    Args:
        income (pd.Series)
        n_children (pd.Series): Same length as income.
        params (pd.series): Must contain "benefit_per_child" and "benefit_cutoff"

    Returns:
        pd.Series: The benefits.

    """
    raw_benefits = n_children * params.benefit_per_child
    benefits = raw_benefits.where(income <= params.benefit_cutoff, 0)
    return benefits
