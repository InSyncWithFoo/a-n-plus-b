from collections.abc import Callable
from typing import Any, TypeVar

import pytest
from hypothesis import given
from hypothesis.strategies import (
	composite, DrawFn, floats, integers, just, lists,
	one_of, sampled_from, SearchStrategy, tuples
)

from a_n_plus_b import (
	ANPlusB, ComplexWithNonIntegerPart,
	EmptyInput, InputIsNotParsable
)
from . import examples, join, whitespace


_E = TypeVar('_E')
_T = TypeVar('_T')


def _make_complex(example: tuple[int | float, int | float]) -> complex:
	return complex(*example)


def _starts_with_sign(example: tuple[str, Any]) -> bool:
	text, _ = example
	
	return text[0] in ('+', '-')


def _casing_scrambled(text: str) -> SearchStrategy[str]:
	lowercase = text.lower()
	uppercase = text.upper()
	
	substrategies = (sampled_from(chars) for chars in zip(lowercase, uppercase))
	
	return tuples(*substrategies).map(''.join)


@composite
def _variations(draw: DrawFn, text: str) -> str:
	scrambled_text = draw(_casing_scrambled(text))
	
	return draw(with_surrounding_whitespace(scrambled_text))


def _tupled_with(value: _T) -> Callable[[_E], tuple[_E, _T]]:
	def tupled_with_given_value(example: _E) -> tuple[_E, _T]:
		return example, value
	
	return tupled_with_given_value


def _whitespace_sequences() -> SearchStrategy[str]:
	return lists(
		sampled_from(whitespace),
		min_size = 1, max_size = 10
	).map(''.join)


def whitespace_sequences_or_empty() -> SearchStrategy[str]:
	return _whitespace_sequences() | just('')


def with_surrounding_whitespace(text: str) -> SearchStrategy[str]:
	return tuples(
		whitespace_sequences_or_empty(),
		just(text),
		whitespace_sequences_or_empty()
	) \
		.map(join)


def _non_integral_floats() -> SearchStrategy[float]:
	return floats().filter(lambda example: not example.is_integer())


def _operators() -> SearchStrategy[str]:
	return sampled_from(['+', '-'])


def _signs() -> SearchStrategy[str]:
	return just('') | _operators()


def _digits() -> SearchStrategy[int]:
	return integers(min_value = 0, max_value = 9)


@composite
def _integers_with_potentially_superfluous_sign(
	draw: DrawFn,
	max_size: int = 10
) -> str:
	sign = draw(_signs())
	digits = draw(lists(_digits(), min_size = 1, max_size = max_size).map(join))
	
	return draw(with_surrounding_whitespace(sign + digits))


@composite
def _a_values(draw: DrawFn, max_size: int = 10) -> str:
	sign = draw(_signs())
	digits = draw(lists(_digits(), max_size = max_size).map(join))
	
	return sign + digits


def _b_values(max_size: int = 10) -> SearchStrategy[str]:
	return lists(_digits(), min_size = 1, max_size = max_size).map(join)


class ParseANPlusBTestCases:
	
	@staticmethod
	@composite
	def valid(draw: DrawFn) -> tuple[str, tuple[int, int]]:
		a = draw(_a_values())
		n = draw(sampled_from(['n', 'N']))
		operator = draw(_signs())
		
		if not a:
			step = 0
		elif a == '+':
			step = 1
		elif a == '-':
			step = -1
		else:
			step = int(a)
		
		if operator:
			b = draw(_b_values())
			offset = int(f'{operator}{b}')
		else:
			b = ''
			offset = 0
		
		operator = draw(with_surrounding_whitespace(operator))
		text = draw(with_surrounding_whitespace(f'{a}{n}{operator}{b}'))
		
		return text, (step, offset)
	
	@staticmethod
	@composite
	def whitespace_after_a_sign(draw: DrawFn) -> str:
		valid_cases = ParseANPlusBTestCases.valid().filter(_starts_with_sign)
		valid_input = draw(valid_cases)[0]
		
		a_sign, rest = valid_input[0], valid_input[1:]
		invalid_whitespace = draw(_whitespace_sequences())
		
		return f'{a_sign}{invalid_whitespace}{rest}'
	
	@staticmethod
	@composite
	def missing_b(draw: DrawFn) -> str:
		a = draw(_a_values())
		n = draw(sampled_from(['n', 'N']))
		operator = draw(_operators())
		
		operator = draw(with_surrounding_whitespace(operator))
		
		return draw(with_surrounding_whitespace(f'{a}{n}{operator}'))
	
	@staticmethod
	@composite
	def missing_operator(draw: DrawFn) -> str:
		a = draw(_a_values())
		n = draw(sampled_from(['n', 'N']))
		b = draw(_b_values())
		
		b = draw(with_surrounding_whitespace(b))
		
		return draw(with_surrounding_whitespace(f'{a}{n}{b}'))


@given(
	one_of([
		_variations('odd').map(_tupled_with((2, 1))),
		_variations('even').map(_tupled_with((2, 0)))
	])
)
def test_parse_odd_even(text_and_expected: tuple[str, tuple[int, int]]) -> None:
	text, expected = text_and_expected
	instance = ANPlusB.parse(text)
	
	assert (instance.step, instance.offset) == expected


@given(_integers_with_potentially_superfluous_sign())
def test_parse_integer(text: str) -> None:
	expected = int(text)
	
	instance = ANPlusB.parse(text)
	
	assert instance.step == 0
	assert instance.offset == expected


@given(whitespace_sequences_or_empty())
def test_parse_empty(text: str) -> None:
	with pytest.raises(EmptyInput):
		ANPlusB.parse(text)


@given(ParseANPlusBTestCases.valid())
@examples([
	tuple([('+3n+2', (3, 2))]),
	tuple([('+4n+0', (4, 0))]),
	tuple([('+6n', (6, 0))]),
	tuple([('+5n-0', (5, 0))]),
	tuple([('+7n-1', (7, -1))]),
	
	tuple([('3n+2', (3, 2))]),
	tuple([('4n+0', (4, 0))]),
	tuple([('6n', (6, 0))]),
	tuple([('5n-0', (5, 0))]),
	tuple([('7n-1', (7, -1))]),
	
	tuple([('+0n+2', (0, 2))]),
	tuple([('+0n+0', (0, 0))]),
	tuple([('+0n', (0, 0))]),
	tuple([('+0n-0', (0, 0))]),
	tuple([('+0n-1', (0, -1))]),
	
	tuple([('0n+2', (0, 2))]),
	tuple([('0n+0', (0, 0))]),
	tuple([('0n', (0, 0))]),
	tuple([('0n-0', (0, 0))]),
	tuple([('0n-1', (0, -1))]),
	
	tuple([('-0n+2', (0, 2))]),
	tuple([('-0n+0', (0, 0))]),
	tuple([('-0n', (0, 0))]),
	tuple([('-0n-0', (0, 0))]),
	tuple([('-0n-1', (0, -1))]),
	
	tuple([('-3n+2', (-3, 2))]),
	tuple([('-4n+0', (-4, 0))]),
	tuple([('-6n', (-6, 0))]),
	tuple([('-5n-0', (-5, 0))]),
	tuple([('-7n-1', (-7, -1))])
])
def test_parse_a_n_plus_b(
	text_and_expected: tuple[str, tuple[int, int]]
) -> None:
	text, expected = text_and_expected
	instance = ANPlusB.parse(text)
	
	assert (instance.step, instance.offset) == expected


@given(
	one_of([
		ParseANPlusBTestCases.whitespace_after_a_sign(),
		ParseANPlusBTestCases.missing_b(),
		ParseANPlusBTestCases.missing_operator()
	])
)
def test_parse_invalid(text: str) -> None:
	with pytest.raises(InputIsNotParsable):
		ANPlusB.parse(text)


@given(
	one_of([
		tuples(integers(), integers()).map(_make_complex),
		integers(),
		integers().map(float)
	])
)
def test_from_complex(value: int | float | complex) -> None:
	instance = ANPlusB.from_complex(value)
	expected = (int(value.imag), int(value.real))
	
	assert (instance.step, instance.offset) == expected


@given(
	one_of([
		tuples(_non_integral_floats(), integers()),
		tuples(integers(), _non_integral_floats()),
		tuples(_non_integral_floats(), _non_integral_floats())
	]) \
		.map(_make_complex)
)
def test_from_complex_invalid(value: complex) -> None:
	with pytest.raises(ComplexWithNonIntegerPart):
		ANPlusB.from_complex(value)
