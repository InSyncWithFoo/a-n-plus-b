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


def _text_starts_with_sign(example: tuple[str, Any]) -> bool:
	text, _ = example
	
	return text[0] in ('+', '-')


def _casing_scrambled(text: str) -> SearchStrategy[str]:
	lowercase = text.lower()
	uppercase = text.upper()
	
	substrategies = (sampled_from(chars) for chars in zip(lowercase, uppercase))
	
	return tuples(*substrategies).map(''.join)


def _variation_fragments(text: str) -> SearchStrategy[tuple[str, str, str]]:
	return tuples(
		whitespace_sequences_or_empty(),
		_casing_scrambled(text),
		whitespace_sequences_or_empty()
	)


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


def _odd_variations() -> SearchStrategy[str]:
	return _variation_fragments('odd').map(''.join)


def _even_variations() -> SearchStrategy[str]:
	return _variation_fragments('even').map(''.join)


def _non_integral_floats() -> SearchStrategy[float]:
	return floats().filter(lambda example: not example.is_integer())


def _operators() -> SearchStrategy[str]:
	return sampled_from(['+', '-'])


def _signs() -> SearchStrategy[str]:
	return just('') | _operators()


def _digits() -> SearchStrategy[int]:
	return integers(min_value = 0, max_value = 9)


def _steps() -> SearchStrategy[str]:
	return tuples(_signs(), lists(_digits(), max_size = 10).map(join)).map(join)


def _offsets() -> SearchStrategy[str]:
	return lists(_digits(), min_size = 1, max_size = 10).map(join)


class ParseANPlusBTestCases:
	
	@staticmethod
	@composite
	def valid(draw: DrawFn) -> tuple[str, tuple[int, int]]:
		step = draw(_steps())
		operator = draw(_signs())
		n = draw(sampled_from(['n', 'N']))
		
		if not step:
			a = 0
		elif step == '+':
			a = 1
		elif step == '-':
			a = -1
		else:
			a = int(step)
		
		if operator:
			offset = draw(_offsets())
			b = int(f'{operator}{offset}')
		else:
			offset = ''
			b = 0
		
		operator = draw(with_surrounding_whitespace(operator))
		text = draw(with_surrounding_whitespace(f'{step}{n}{operator}{offset}'))
		
		return text, (a, b)
	
	@staticmethod
	@composite
	def whitespace_after_a_sign(draw: DrawFn) -> str:
		valid_cases_starting_with_sign = ParseANPlusBTestCases.valid() \
			.filter(_text_starts_with_sign)
		valid_case = draw(valid_cases_starting_with_sign)[0]
		
		invalid_whitespace = draw(_whitespace_sequences())
		
		return f'{valid_case[0]}{invalid_whitespace}{valid_case[1:]}'


@given(
	one_of([
		_odd_variations().map(_tupled_with((2, 1))),
		_even_variations().map(_tupled_with((2, 0)))
	])
)
def test_parse_odd_even(text_and_expected):
	text, expected = text_and_expected
	instance = ANPlusB.parse(text)
	
	assert (instance.step, instance.offset) == expected


@given(
	tuples(_signs(), lists(_digits(), min_size = 1, max_size = 10).map(join)) \
		.map(join) \
		.flatmap(with_surrounding_whitespace)
)
def test_parse_integer(text):
	expected = int(text)
	
	instance = ANPlusB.parse(text)
	
	assert instance.step == 0
	assert instance.offset == expected


@given(whitespace_sequences_or_empty())
def test_parse_empty(text):
	with pytest.raises(EmptyInput):
		ANPlusB.parse(text)


@given(ParseANPlusBTestCases.valid())
@examples([
	(['+3n+2', (3, 2)]),
	(['+4n+0', (4, 0)]),
	(['+6n', (6, 0)]),
	(['+5n-0', (5, 0)]),
	(['+7n-1', (7, -1)]),
	
	(['3n+2', (3, 2)]),
	(['4n+0', (4, 0)]),
	(['6n', (6, 0)]),
	(['5n-0', (5, 0)]),
	(['7n-1', (7, -1)]),
	
	(['+0n+2', (0, 2)]),
	(['+0n+0', (0, 0)]),
	(['+0n', (0, 0)]),
	(['+0n-0', (0, 0)]),
	(['+0n-1', (0, -1)]),
	
	(['0n+2', (0, 2)]),
	(['0n+0', (0, 0)]),
	(['0n', (0, 0)]),
	(['0n-0', (0, 0)]),
	(['0n-1', (0, -1)]),
	
	(['-0n+2', (0, 2)]),
	(['-0n+0', (0, 0)]),
	(['-0n', (0, 0)]),
	(['-0n-0', (0, 0)]),
	(['-0n-1', (0, -1)]),
	
	(['-3n+2', (-3, 2)]),
	(['-4n+0', (-4, 0)]),
	(['-6n', (-6, 0)]),
	(['-5n-0', (-5, 0)]),
	(['-7n-1', (-7, -1)]),
])
def test_parse_a_n_plus_b(text_and_expected):
	text, expected = text_and_expected
	instance = ANPlusB.parse(text)
	
	assert (instance.step, instance.offset) == expected


@given(
	one_of([
		ParseANPlusBTestCases.whitespace_after_a_sign()
	])
)
@examples([
	'+ 3'
])
def test_parse_invalid(text):
	with pytest.raises(InputIsNotParsable):
		ANPlusB.parse(text)


@given(
	one_of([
		tuples(integers(), integers()).map(_make_complex),
		integers(),
		integers().map(float)
	])
)
def test_from_complex(value):
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
def test_from_complex_invalid(value):
	with pytest.raises(ComplexWithNonIntegerPart):
		ANPlusB.from_complex(value)
