# dag_gettsim

## Introduction

This is a small toy package to explore the use of Directed Acyclic Graphs (DAGs) in [gettsim](https://github.com/iza-institute-of-labor-economics/gettsim). It is only meant as an illustration and has no practical use whatsoever.

There is an accompanying [tutorial](https://github.com/janosg/dag_gettsim_tutorial) repository. We opted for a separate repository, to make the distinction between gettsim code and user code very explicit.

This is based on ideas by [Tobias Raabe](https://github.com/tobiasraabe), [Hans-Martin von Gaudecker](https://github.com/hmgaudecker) and [Janoś Gabler](https://github.com/janosg).

## Installation

Currently only local installation is possible. Open a terminal in the root folder and type:

`conda env create -f environment.yml`
`pip install -e .`

## Some Design Choices

### Data Arguments / Data Storage

I suggest that internally, we store data as dictionary of pandas Series, not as a DataFrame. This is easier for Data that is needed on different aggregation levels (household vs. individual). Then, theoretically, data arguments could be anything (numpy array, pandas Series, DataFrames), but I would suggest we always use Series.

### Function Outputs

Anything that could be a data argument can also be a function output. So I suggest we require all functions to return pandas Series, but we could be more flexible if necessary.

### How Parameters are Handled

All functions take one argument called params, which is a pandas Series. The Series contains all parameters that are needed for the model that is being estimated. This is a huge reduction compared to the full parameter database, but probably much more than what is actually needed inside a single function.

Some functions might not even need parameters. I would still pass in the params almost everywhere in case a user wants to replace the function by something that needs params with minimal changes to the rest.

### How functions are specified

I decided to have a dictionary of functions (which in the long run could be paths to functions that are then imported using importlib) instead of a flat list of functions. This basically allows to rename functions before passing them to gettsim. I make heavy use of this in the tutorial and really like it!

## To-Do

- Implement garbage collection in `execute_dag` (should be quite easy)
- Implement a parallel scheduler and experiment with existing ones
- Make model specifications yaml and json compatible. Currently the user provided functions have to be in a dictionary. We should also allow for paths to functions that are then imported using [importlib](https://docs.python.org/3/library/importlib.html)
- Implement a better parameter backend (e.g. Database) and allow to store metadata (units, ...) for parameters

## Lessons learned

- Whenever you are tempted to write a function that does something with a DAG, check if networkx has already implemented your function.

## Open Questions

- Do we really have to distinguish between new_functions, obsolete_functions and overriden_functions. I think it is enough to provide one dictionary with new functions. If something is new or overriden can be determined automatically. If something should be ignored can be determined from the targets.
- Should all functions have the params argument or should this be optional? A try except block around the partial step would make it optional.

