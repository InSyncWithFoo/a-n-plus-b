'''
Toolkit for working with the An+B CSS microsyntax.
'''

from typing import Final
from ._a_n_plus_b import (
	ANPlusB,
	ComplexWithNonIntegerPart,
	EmptyInput,
	IncorrectUseOfConstructor,
	InputIsNotParsable,
	InvalidNumberOfChildren,
	InvalidOrder,
	ParseError
)


__all__ = [  # noqa: RUF022
	'ANPlusB', 'n',
	'ComplexWithNonIntegerPart',
	'EmptyInput',
	'IncorrectUseOfConstructor',
	'InputIsNotParsable',
	'InvalidNumberOfChildren',
	'InvalidOrder',
	'ParseError'
]


n: Final = ANPlusB(1, 0)
'''
Helper object for creating :class:`ANPlusB` instances.
'''
