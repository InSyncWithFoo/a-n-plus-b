'''
The main feature of the package: :class:`ANPlusB`.
'''

import math
import sys
from collections.abc import Iterator
from itertools import count
from typing import Any, Literal, overload

from ._grammar import a_n_plus_b, integer, Regex, whitespace


if sys.version_info >= (3, 11):
	from typing import Self
else:
	from typing_extensions import Self

_surrounding_whitespace = Regex(fr'\A{whitespace}+|{whitespace}+\Z')


def _normalize(text: str, /) -> str:
	'''
	Strip surrounding whitespace and
	convert ``text`` to lowercase.
	'''
	
	return _surrounding_whitespace.sub('', text).lower()


def _remove_whitespace(text: str, /) -> str:
	'''
	Remove all whitespace.
	'''
	
	return whitespace.sub('', text)


def _is_integer(value: float, /) -> bool:
	'''
	Check if ``value`` is an integer.
	'''
	
	return isinstance(value, int) or value.is_integer()


class IncorrectUseOfConstructor(TypeError):
	'''
	Raised when the main constructor
	is passed a single :class:`str` argument.
	'''
	
	def __init__(self, cls: type['ANPlusB'], /) -> None:
		'''
		:param cls: The class whose main constructor was called.
		'''
		
		super().__init__(f'Use {cls.__name__}.parse to parse a string')


class InvalidOrder(ValueError):
	'''
	Raised when an unrecognized order is
	passed to :meth:`ANPlusB.indices`.
	'''
	
	def __init__(self, value: object, /) -> None:
		'''
		:param value: The value passed to :meth:`ANPlusB.indices`.
		'''
		
		super().__init__(
			f'Expected one of: "ascending", "descending", "default", '
			f'got: {value!r}',
		)


class InvalidNumberOfChildren(ValueError):
	'''
	Raised when an invalid number of children is
	passed to :meth:`ANPlusB.indices`.
	'''
	
	def __init__(self, value: object, /) -> None:
		'''
		:param value: The value passed to :meth:`ANPlusB.indices`.
		'''
		
		super().__init__(
			f'Expected a non-negative number, '
			f'got: {value!r}',
		)


class ParseError(ValueError):
	'''
	Raised when an invalid input is passed to :meth:`ANPlusB.parse`.
	'''
	
	pass


class EmptyInput(ParseError):
	'''
	Raised when an empty input is passed to :meth:`ANPlusB.parse`.
	'''
	
	def __init__(self) -> None:
		super().__init__('Input is empty or only contains whitespace')


class InputIsNotParsable(ParseError):
	'''
	Raised when an input that is not parsable
	is passed to :meth:`ANPlusB.parse`.
	'''
	
	def __init__(self, text: str, /) -> None:
		'''
		:param text: The unparsable input.
		'''
		
		super().__init__(repr(text))


class ComplexWithNonIntegerPart(ValueError):
	'''
	Raised when a complex with non-integer parts
	is passed to :meth:`ANPlusB.from_complex`.
	'''
	
	def __init__(self, value: complex, /) -> None:
		'''
		:param value: The value passed to :meth:`ANPlusB.from_complex`.
		'''
		
		super().__init__(
			f'Expected a complex with integral imaginary and real parts, '
			f'got: {value!r}'
		)


class _InfiniteRange:
	'''
	Representation of all possible values
	an :class:`ANPlusB` instance may yield.

	Basically a thin wrapper around :class:`count`,
	providing a :class:`Sequence`-like interface.
	There is no ``__len__`` method, since ``len()``
	expects an :class:`int` which ``math.inf`` is not.
	'''
	
	__slots__ = ('_start', '_step')
	
	_start: int
	_step: int
	
	def __init__(self, start: int, step: int, /) -> None:
		r'''
		:param start: \
			The number to start counting from, also known as offset.
		:param step: \
			The distance between values.
		'''
		
		self._start = start
		self._step = step
	
	def __repr__(self) -> str:
		start, step = self._start, self._step
		
		return f'{self.__class__.__name__}({start = }, {step = })'
	
	def __iter__(self) -> Iterator[int]:
		return count(self._start, self._step)
	
	def __getitem__(self, item: int) -> int:
		'''
		Get the value at the given index.
		
		:param item: The index.
		:raise IndexError: If ``item`` is negative.
		'''
		
		# TODO: Support slices
		
		if item < 0:
			raise IndexError(item)
		
		return self._start + item * self._step
	
	def __contains__(self, item: object) -> bool:
		'''
		Check whether ``item`` is a possible value.
		'''
		
		if not isinstance(item, int):
			return False
		
		if self._step == 0:
			return item == self._start
		
		quotient, remainder = divmod(item - self._start, self._step)
		
		return quotient >= 0 and remainder == 0


class ANPlusB:
	'''
	Implementation of `Section 6. The An+B microsyntax
	<https://drafts.csswg.org/css-syntax-3/#anb-microsyntax>`_.
	'''
	
	__slots__ = ('_step', '_offset')
	
	_step: int
	_offset: int
	
	@overload
	def __new__(cls, offset: int, /) -> Self:
		...
	
	@overload
	def __new__(cls, step: int, offset: int, /) -> Self:
		...
	
	def __new__(cls, step: int, offset: int | None = None, /) -> Self:
		'''
		If only one argument is passed, that argument would be
		interpreted as ``offset`` and ``step`` would be ``0``.
		That is, ``ANPlusB(3)`` is the same as ``ANPlusB(0, 3)``.

		:param step: The step, also known as ``a``.
		:param offset: The offset, also known as ``b``.
		'''
		
		if isinstance(step, str):
			raise IncorrectUseOfConstructor(cls)
		
		instance = super().__new__(cls)
		
		if offset is None:
			step, offset = 0, step
		
		instance._step = step
		instance._offset = offset
		
		return instance
	
	def __str__(self) -> str:
		'''
		Implementation of `Section 9.1. Serializing <an+b>
		<https://drafts.csswg.org/css-syntax-3/#serializing-anb>`_.
		'''
		
		a, b = self._step, self._offset
		
		if a == 0:
			return str(b)
		
		result = ''
		
		if a == 1:
			result += 'n'
		elif a == -1:
			result += '-n'
		else:
			result += f'{a}n'
		
		if b > 0:
			result += f'+{b}'
		elif b < 0:
			result += str(b)
		
		return result
	
	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({self})'
	
	def __pos__(self) -> Self:
		'''
		``+(an + b)`` is equivalent to ``an + b``. 
		'''
		
		return self
	
	def __neg__(self) -> Self:
		'''
		``-(an + b)`` is equivalent to ``-an - b``.
		'''
		
		return self.__class__(-self._step, -self._offset)
	
	def __add__(self, other: int) -> Self:
		'''
		``(an + b) + c`` is equivalent to ``an + (b + c)``. 
		'''
		
		return self.__class__(self._step, self._offset + other)
	
	def __radd__(self, other: int) -> Self:
		'''
		``c + (an + b)`` is equivalent to ``an + (b + c)``. 
		'''
		
		return self + other
	
	def __sub__(self, other: int) -> Self:
		'''
		``(an + b) - c`` is equivalent to ``an + (b - c)``. 
		'''
		
		return self + -other
	
	def __rsub__(self, other: int) -> Self:
		'''
		``c - (an + b)`` is equivalent to ``-an + (c - b)``. 
		'''
		
		return -self + other
	
	def __mul__(self, other: int) -> Self:
		'''
		``(an + b) * c`` is equivalent to ``(ac) * n + (bc)``.
		'''
		
		return self.__class__(self._step * other, self._offset * other)
	
	def __rmul__(self, other: int) -> Self:
		'''
		``c * (an + b)`` is equivalent to ``(ac) * n + (bc)``. 
		'''
		
		return self * other
	
	def __eq__(self, other: object) -> bool:
		'''
		Two instances of :class:`ANPlusB` are equal
		if their steps and offsets are equal.
		'''
		
		if not isinstance(other, self.__class__):
			return NotImplemented
		
		return (self._step, self._offset) == (other._step, other._offset)
	
	def __hash__(self) -> int:
		return hash((self._step, self._offset))
	
	@property
	def step(self) -> int:
		'''
		The step, also known as ``a``.
		'''
		
		return self._step
	
	@property
	def offset(self) -> int:
		'''
		The offset, also known as ``b``.
		'''
		
		return self._offset
	
	def _indices(
		self, population: int, /, *,
		from_last: bool = False,
		order: str = 'default'
	) -> Iterator[int]:
		a, b = self._step, self._offset
		
		if population == 0:
			return
		
		if a <= 0 and b <= 0:
			return
		
		if a == 0:
			index = population - b + 1 if from_last else b
			yield from [index] if 1 <= index <= population else []
			return
		
		if a < 0:
			# 0 -> an -> -inf | 0 -> n -> inf
			#
			# n min <=> an + b max <=> n = 0 <=> an + b = b
			
			start = b
			stop = 0
		
		else:
			# (a > 0)
			# 1 <= an + b <= p
			# 1 - b <= an <= p - b
			#
			# n min <=> an = 1 - b <=> n = (1 - b) / a
			
			min_n = max(0, math.ceil((1 - b) / a))
			
			start = a * min_n + b
			stop = population + 1
		
		indices: Any = range(start, stop, a)
		default_order = 'descending' if a < 0 else 'ascending'
		
		if order == 'default':
			reverse_order = False
		elif order == default_order:
			reverse_order = from_last
		else:
			reverse_order = not from_last
		
		if reverse_order:
			indices = reversed(indices)
		
		for index in indices:
			yield population - index + 1 if from_last else index
	
	@overload
	def indices(
		self, population: int, *,
		from_last: Literal[False] = ...,
		order: Literal['ascending', 'descending', 'default'] = 'default'
	) -> Iterator[int]:
		...
	
	@overload
	def indices(
		self, population: int, *,
		from_last: bool = False,
		order: str
	) -> Iterator[int]:
		...
	
	def indices(
		self, population: int, *,
		from_last: bool = False,
		order: str = 'default'
	) -> Iterator[int]:
		r'''
		Yield the 1-based indices of the children a selector
		with only a ``:nth-child()``/``:nth-last-child()``
		pseudo-class whose argument is the serialization of
		this ``ANPlusB`` object would match if it were to be
		applied to an element with ``population`` children.

		:param population: The number of children.
		:param from_last: Whether to start from the last index.
		:param order: \
			The order in which to yield the indices.
			``ascending`` means the first index yielded will be the smallest.
			``descending`` means the first index yielded will be the greatest.
			``default`` means the first index yielded will
			correspond to the minimum value of ``n``.
		'''
		
		if order not in ('ascending', 'descending', 'default'):
			raise InvalidOrder(order)
		
		if population < 0:
			raise InvalidNumberOfChildren(population)
		
		return self._indices(
			population,
			from_last = from_last,
			order = order
		)
	
	def values(self) -> _InfiniteRange:
		'''
		Return an iterable that yield possible values
		as ``n`` goes from 0 to infinity.
		'''
		
		return _InfiniteRange(self._offset, self._step)
	
	@classmethod
	def parse(cls, text: str, /) -> Self:
		'''
		Parse the given text and returns an ``ANPlusB`` instance.
		
		Surrounding whitespace (spaces, tabs, carriage returns,
		newlines, form feeds) are tolerated.
		However, there must be no whitespace between
		the digits of ``a`` (or ``n``) and its sign, if any.
		
		:param text: The text to parse.
		:raise EmptyInput: If the input is empty or only contains whitespace.
		:raise InputIsNotParsable: If the text is not parsable.
		'''
		
		text = _normalize(text)
		
		if not text:
			raise EmptyInput
		
		if text == 'even':
			return cls(2, 0)
		
		if text == 'odd':
			return cls(2, 1)
		
		if integer.fullmatch(text):
			return cls(int(text))
		
		match = a_n_plus_b.fullmatch(text)
		
		if not match:
			raise InputIsNotParsable(text)
		
		a, b = match['a'], _remove_whitespace(match['b'] or '')
		
		if not a:
			step = 0
		elif a == '+':
			step = 1
		elif a == '-':
			step = -1
		else:
			step = int(a)
		
		offset = int(b) if b else 0
		
		return cls(step, offset)
	
	@classmethod
	def from_complex(cls, value: complex, /) -> Self:
		'''
		Convert a complex number to an ``ANPlusB`` instance.

		For readability, ``value`` should be written in the form ``2j + 3``.
		'''
		
		imaginary, real = value.imag, value.real
		
		if not _is_integer(imaginary) or not _is_integer(real):
			raise ComplexWithNonIntegerPart(value)
		
		return cls(int(imaginary), int(real))
