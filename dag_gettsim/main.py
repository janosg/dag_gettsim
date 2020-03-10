import inspect
from functools import partial
from inspect import getfullargspec, getmembers

import networkx as nx
import pandas as pd

from dag_gettsim import aggregation, benefits, taxes


def tax_transfer(baseline_date, data, functions=None, params=None, targets="all"):
    """Simulate a tax and tranfers system specified in model_spec.

    Args:
        baseline_date (str): A date, e.g. '2019-01-01'. This is used to select a set of
            baseline parameters (and in the future baseline functions).
        data (dict): User provided dataset as dictionary of Series.
        functions (dict): Dictionary with user provided functions. The keys are the
            names of the function. The values are either callables or strings with
            absolute or relative import paths to a function. If functions have the
            same name as an existing gettsim function they override that function.
        params (dict): A pandas Series or dictionary with user provided parameters.
            Currently just mapping a parameter name to a parameter value, in the
            future we will need more metadata. If parameters have the same name as
            an existing parameter from the gettsim parameters database at the
            specified date they override that parameter.
        targets (list): List of strings with names of functions whose output is actually
            needed by the user. By default, all results are returned.

    Returns:
        dict: Dictionary of Series containing the target quantities.

    """
    user_params = {} if params is None else params
    user_functions = {} if functions is None else functions

    params = get_params(baseline_date, user_params)
    func_dict = create_function_dict(user_functions=user_functions, params=params)
    dag = create_dag(func_dict)
    results = execute_dag(func_dict, dag, data, targets)
    return results


def get_params(baseline_date, user_params):
    """Combine baseline parameters and user parameters.

    Currently this just generates baseline independent parameters for the toy model.
    In the long run it will load a database, query the baseline parameters and update
    or extend it with user parameters.

    Args:
        baseline_date (str): A date, e.g. '2019-01-01'
        user_params (dict or pd.Series): User provided parameters that override or
            extend the baseline parameters.

    Returns:
        pd.Series

    """
    params = {
        "income_tax": 0.2,
        "wealth_tax": 0.9,  # 90 % wealth tax is just to make Max happy ;-)
        "benefit_per_child": 2000,
        "benefit_cutoff": 30000,
    }

    if isinstance(user_params, pd.Series):
        user_params = user_params.to_dict()

    params.update(user_params)

    return pd.Series(params)


def create_function_dict(user_functions, params):
    """Create a dictionary of all functions that will appear in the DAG.

    Args:
        user_functions (dict): Dictionary with user provided functions. The keys are the
            names of the function. The values are either callables or strings with
            absolute or relative import paths to a function.

    Returns:
        dict: Dictionary mapping function names to callables.

    """
    func_dict = {}
    for module in taxes, benefits, aggregation:
        func_dict.update(dict(getmembers(module, inspect.isfunction)))

    func_dict.update(user_functions)

    partialed = {name: partial(func, params=params) for name, func in func_dict.items()}

    return partialed


def create_dag(func_dict):
    """Create a directed acyclic graph (DAG) capturing dependencies between functions.

    Args:
        func_dict (dict): Maps function names to functions.

    Returns:
        dict: The DAG, represented as a dictionary of lists that maps function names
            to a list of its data dependencies.

    """
    dag_dict = {name: getfullargspec(func).args for name, func in func_dict.items()}
    return nx.DiGraph(dag_dict).reverse()


def execute_dag(func_dict, dag, data, targets):
    """Naive serial scheduler for our tasks.

    We will probably use some existing scheduler instead. Interesting sources are:
    - https://ipython.org/ipython-doc/3/parallel/dag_dependencies.html
    - https://docs.dask.org/en/latest/graphs.html

    The main reason for writing an own implementation is to explore how difficult it
    would to avoid dask as a dependency.

    Args:
        func_dict (dict): Maps function names to functions.
        dag (nx.DiGraph)
        data (dict):
        targets (list):

    Returns:
        dict: Dictionary of pd.Series with the results.

    """
    results = data.copy()
    for task in nx.topological_sort(dag):
        if task not in results:
            if task in func_dict:
                kwargs = _dict_subset(results, dag.predecessors(task))
                results[task] = func_dict[task](**kwargs)
            else:
                raise KeyError(f"Missing variable or function: {task}")

    if targets != "all":
        results = _dict_subset(results, targets)
    return results


def _dict_subset(dictionary, keys):
    return {k: dictionary[k] for k in keys}
