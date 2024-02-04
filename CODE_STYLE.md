# Code style

I believe code must be beautiful.
By "beautiful", I mean "beautiful to me".

In addition to the rules listed below,
there are a few things to remember:

* Format the files manually if necessary.
* Some rules are not documented here.
* Follow existing code when in doubt.

These rules are not concrete. For instance,
Python code examples in this file have their indentation
set to 2 spaces as a compromise between [Python](#for-python)
and [Markdown](#for-markdown)'s rules.

View this file in source mode for best experience.


## For Python

I don't like [PEP 8][1] (for the most part).
This means _[black][2]_ and other PEP-8-enforcing tools
should not be used.


### Formatting styles

* Indentation:
  * Use tabs.
  * Preferably displayed as 4 spaces.

* Nesting:
  * 3 levels is considered high.
  * Use 4 frugally and try your best to avoid 5.
  
  See also: *[Why You Shouldn't Nest Your Code][3]*

* Line length:
  * A line must not be longer than 80 characters,
    with tabs count as 4.
  * Wrapping long lines is recommended,
    even if the length does not exceed 80.

* Quotes:
  * Prefer single quotes wherever possible,
    even when writing docstrings.

* Operators:
  * Use spaces around keyword arguments and operators.

* Empty lines:
  * Group multiple related lines to make mono-blocks.
    Separate such blocks with blank lines.
    For example:
  
    ```python
    if foo > bar:
      bar = Qux()
      bar.do_this()
    
      something_else.do_that()
    
    else:
      subprocess.run('rm -rf /', shell = True)
    ```


### Semantic styles

* Naming:
  * Use:
    * `snake_case`: functions, variables and modules
    * `PascalCase`: classes
    * `ALL_CAPS`: enum members and constants
  
  * Do not name things `utils`, `helper`, `base` or `abstract`.
    Give more meaningful names when possible; [it is always possible][4].
    
    See also: *[Naming Things in Code][5]*

* Variable scope:
  * Limit them wherever applicable.

* Comments:
  * A comment must be at least two spaces away
    from the nearest non-empty character.
    
    When the same line has no other contents,
    the comment should be a comment for and
    have the same indentation as the statement(s)
    right below it.

    For example:

    ```python
    print('Lorem ipsum')  # This is a comment
    
    # This is also a comment
    foo = Bar()
    foo.qux()
    
    def function():
      # This too
      lorem = ipsum.dolor().sit(amet)
    ```

  * Only use comments to explain something
    that cannot otherwise be adequately made
    clear by simply refactoring the code.
    
    See also: *[Don't Write Comments][6]*
  
  * `# noqa`, `# type: ignore` and the like
    are exempt from the second rule.
    Use `# noqa` for warnings issued by PyCharm
    (as well as other IDEs), and `# type: ignore`
    for those issued by type checkers.


### For test files

* The rules for test files are less strict
  than that of package files. The changes
  include, but not limited to:
  
  * The 80 line width rule might be ignored.
  * Global variables are of no concern.
  * "Helper" code may be nested a bit deeper.


## For Markdown

See the source code of this page for an example.

* Indentation:
  * Use 2 spaces.

* Code blocks:
  * Use code fences.

* Wrapping:
  * Try to split paragraph to lines of even length.
    Make lines short, but not too short.
    If disparity cannot be avoided,
    then so be it.
    
    At the same time, try to preserve spaces
    between phrases, link text and the like.

* Links:
  * All links should be grouped at the end
    of the page as a link reference definitions
    block, with numbers as link labels.
  
    The numbers must be ordered strictly
    in ascending order, both in labels and
    in definitions. Indent the whole group
    to level 1 (2 spaces). 

* Headers:
  * Use at most one level-1 header,
    which must be at the very top if it exists.
    There must be no preceding blank lines.

* Empty lines:
  * Use 2 blank lines before headers.
  * Use 1 blank lines after headers.
  * Use 1 blank line after blocks.
  * Use 2 blank lines before the links block.
  * Use 1 empty lines between list items
    if they have sub-blocks.


## For JSON

* Indentation:
  * Use tabs.
  * Preferably displayed as 4 spaces.

* Casing:
  * Use `snake_case`.


## For TOML

* Indentation:
  * Use 2 spaces.

* Quotes:
  * Use double quotes.


## For YAML

* Indentation:
  * Use 2 spaces.


## For all files

* Use UTF-8 encoding.
* Use Unix-style line endings.
* End a file with a blank line.


  [1]: https://peps.python.org/pep-0008/
  [2]: https://github.com/psf/black
  [3]: https://www.youtube.com/watch?v=CFRhGnuXG-4
  [4]: https://letmegooglethat.com/?q=%E2%80%9CBe+kind+whenever+possible.+It+is+always+possible.%E2%80%9D
  [5]: https://www.youtube.com/watch?v=-J3wNP6u5YU
  [6]: https://www.youtube.com/watch?v=Bf7vDBBOBUA
