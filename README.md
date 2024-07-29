# ANPlusB

This tiny package provides a toolkit for
working with the `<An+B>` CSS microsyntax.


## Installation

This package is available [on PyPI][1]:

```shell
$ pip install a-n-plus-b
```


## Usage

This package only ever parses [the `<An+B>` microsyntax][2].
It does not support [the `of <selector>` syntax][3].

### Examples

```pycon
>>> from a_n_plus_b import ANPlusB
>>> ANPlusB(2, 1)
ANPlusB(2n+1)
>>> str(_)
'2n+1'
>>> ANPlusB(4)
ANPlusB(4)
>>> ANPlusB(4, 0)
ANPlusB(4n)
>>> {ANPlusB(1, 0), ANPlusB(True, False)}
{ANPlusB(n)}
```

```pycon
>>> from itertools import islice
>>> ANPlusB(3, 2)
ANPlusB(3n+2)
>>> values = _.values()
>>> values
_InfiniteRange(start = 2, step = 3)
>>> list(islice(values, 10))
[2, 5, 8, 11, 14, 17, 20, 23, 26, 29]
>>> 6405429723686292014 in values
True
```

```pycon
>>> instance = ANPlusB(4, -7)
>>> list(instance.indices(40))
[1, 5, 9, 13, 17, 21, 25, 29, 33, 37]
>>> list(instance.indices(40, from_last = True))
[40, 36, 32, 28, 24, 20, 16, 12, 8, 4]
>>> list(instance.indices(40, order = 'descending'))
[37, 33, 29, 25, 21, 17, 13, 9, 5, 1]
>>> list(instance.indices(40, from_last = True, order = 'ascending'))
[4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
```

```pycon
>>> ANPlusB.parse('odd')
ANPlusB(2n+1)
>>> ANPlusB.parse('even')
ANPlusB(2n)
>>> ANPlusB.parse('4')
ANPlusB(4)
>>> ANPlusB.parse('-1n')
ANPlusB(-n)
>>> ANPlusB.parse('+0n-8')
ANPlusB(-8)
>>> ANPlusB.parse('0n+0124')
ANPlusB(124)
```

```pycon
>>> ANPlusB.from_complex(5j - 2)
ANPlusB(5n-2)
```

```pycon
>>> from a_n_plus_b import n
>>> 2 * n
ANPlusB(2n)
>>> n * -3 - 1
ANPlusB(-3n-1)
>>> 4 - n * 9
ANPlusB(-9n+4)
```


## Contributing

Please see _[Contributing][4]_ for more information.


  [1]: https://pypi.org/project/a-n-plus-b
  [2]: https://drafts.csswg.org/css-syntax-3/#anb-microsyntax
  [3]: https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child#the_of_selector_syntax
  [4]: ./CONTRIBUTING.md
