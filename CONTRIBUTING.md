# Contributing

All contributions are welcome, including typo fixes.
There might be a few `TODO` comments marking future intentions;
feel free to work on those.

See _[Code style][1]_ and _[Project structure][2]_
for more information on the project itself.


## Start

Clone this project with `git clone`, then install the package
in editable mode along with its `dev` dependencies:

```shell
$ pip install -e .[dev]
```

This will install all packages necessary for development.


## Run tests

Whenever you make a <em>fix</em>,
remember to run the tests with `pytest`.
If everything passes, you are good to go.

```shell
$ pytest
```

Otherwise, modify the tests as you go,
and make sure that those pass as well.


## Type hinting

The code must pass mypy, Pyright and PyCharm type checking.
If you don't use PyCharm, you may ignore it.
As stated in _[Code style]_, use comments as necessary.
For test files, test cases and "helper" functions may or
may not be type hinted. Regardless, good type hints
are always strongly and explicitly recommended.


  [1]: ./CODE_STYLE.md
  [2]: ./PROJECT_STRUCTURE.md
