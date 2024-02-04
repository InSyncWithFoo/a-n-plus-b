# Project structure

There are two modules (one supporting, one `__init__`)
and three test files.


## Source code

The [`__init__.py`][2] file contains the main features of the package.
The private [`_grammar.py`][3] has a convenient pattern used for parsing.

Public classes, methods and functions must have docstrings.
Parameters of a method and errors it might raise, if any,
must be documented in its own docstring.


## Test files

Test cases for `ANPlusB`'s methods are divided into three files:

* [`test_alternate_constructors.py`][4] tests the
  `parse` and `from_complex` methods.
* [`test_indices.py`][5] tests the `indices` method.
* The rest are in [`test_other_methods.py`][6].

Most inputs are automatically generated using Hypothesis.
On the other hand, there are also concrete test cases.


## Type hinting

The code must pass mypy, Pyright and PyCharm type checking.
As stated in _[Code style]_, use comments as necessary.
For test files, test cases and "helper" functions may or
may not be type hinted. Regardless, good type hints
are always strongly and explicitly recommended.


  [1]: ./CODE_STYLE.md#for-python
  [2]: ./src/a_n_plus_b/__init__.py
  [3]: ./src/a_n_plus_b/_grammar.py
  [4]: ./tests/test_alternate_constructors.py
  [5]: ./tests/test_indices.py
  [6]: ./tests/test_other_methods.py
