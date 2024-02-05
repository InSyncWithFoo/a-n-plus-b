from collections.abc import Iterable
from itertools import product
from typing import cast, Literal

import pytest
from _pytest.mark import ParameterSet
from hypothesis import assume, given
from hypothesis.strategies import (
	booleans, composite, DrawFn, from_type, integers, just,
	one_of, sampled_from, SearchStrategy, tuples
)

from a_n_plus_b import ANPlusB, InvalidNumberOfChildren, InvalidOrder
from . import a_n_plus_b_instances, examples


_Order = Literal['ascending', 'descending', 'default']
_TestCase = tuple[ANPlusB, tuple[int, bool, _Order], Iterable[int]]


def _ascending(values: Iterable[int]) -> Iterable[int]:
	return sorted(values)


def _descending(indices: Iterable[int]) -> Iterable[int]:
	return sorted(indices, reverse = True)


def _from_last(indices: Iterable[int], population: int) -> Iterable[int]:
	return [population - index + 1 for index in indices]


def _sign(value: int, /) -> Literal['negative', 'positive', 'zero']:
	if value < 0:
		return 'negative'
	
	if value > 0:
		return 'positive'
	
	return 'zero'


def _describe(test_case: _TestCase) -> str:
	instance, (_population, from_last, order), _expected = test_case
	step, offset = instance.step, instance.offset
	
	descriptions = [
		f'{_sign(step)} step',
		f'{_sign(offset)} offset',
		'from last' if from_last else 'from first',
		order
	]
	
	return ', '.join(descriptions)


def _orders() -> SearchStrategy[_Order]:
	return cast(
		SearchStrategy[_Order],
		sampled_from(['ascending', 'descending', 'default'])
	)


def _non_positive_step_and_offset_test_cases() -> SearchStrategy[_TestCase]:
	strategy = tuples(
		a_n_plus_b_instances(
			integers(max_value = 0),
			integers(max_value = 0)
		),
		tuples(integers(min_value = 0), booleans(), _orders()),
		just(list[int]())
	)
	
	return cast(SearchStrategy[_TestCase], strategy)


@composite
def _zero_step_test_cases(draw: DrawFn) -> _TestCase:
	argument_sets = tuples(integers(min_value = 0), booleans(), _orders())
	
	instance = draw(a_n_plus_b_instances(just(0), integers()))
	population, from_last, order = draw(argument_sets)
	
	b = instance.offset
	
	index = population - b + 1 if from_last else b
	expected = [index] if 1 <= b <= population else list[int]()
	
	return instance, (population, from_last, order), expected


@composite
def _non_positive_step_zero_offset_test_cases(draw: DrawFn) -> _TestCase:
	argument_sets = tuples(integers(min_value = 0), booleans(), _orders())
	
	instance = draw(a_n_plus_b_instances(integers(max_value = -1), just(0)))
	arguments = draw(argument_sets)
	
	return instance, arguments, list[int]()


def _test_case_group(
	instance: ANPlusB,
	population: int,
	base_case_expected: Iterable[int]
) -> list[ParameterSet]:
	test_cases: list[ParameterSet] = []
	from_last_and_order_matrix = product(
		[False, True],
		['default', 'ascending', 'descending']
	)
	
	for from_last, order in from_last_and_order_matrix:
		expected = base_case_expected
		
		if from_last:
			expected = _from_last(base_case_expected, population)
		
		if order == 'ascending':
			expected = _ascending(expected)
		elif order == 'descending':
			expected = _descending(expected)
		
		test_case = (instance, (population, from_last, order), expected)
		test_cases.append(
			pytest.param(
				test_case,
				id = _describe(cast(_TestCase, test_case))
			)
		)
	
	return test_cases


@given(
	one_of([
		_non_positive_step_and_offset_test_cases(),
		_zero_step_test_cases(),
		_non_positive_step_zero_offset_test_cases()
	])
)
@examples([
	*_test_case_group(ANPlusB(3, 0), 100, list(range(3, 101, 3))),
	
	*_test_case_group(ANPlusB(-2, 6), 10, [6, 4, 2]),
	*_test_case_group(ANPlusB(-1, 4), 8, [4, 3, 2, 1]),
	*_test_case_group(ANPlusB(-3, 8), 18, [8, 5, 2]),
	
	*_test_case_group(ANPlusB(4, -5), 20, [3, 7, 11, 15, 19]),
	*_test_case_group(ANPlusB(5, -2), 12, [3, 8]),
	
	*_test_case_group(ANPlusB(2, 1), 15, [1, 3, 5, 7, 9, 11, 13, 15]),
	*_test_case_group(ANPlusB(3, 1), 10, [1, 4, 7, 10]),
	*_test_case_group(ANPlusB(1, 4), 11, [4, 5, 6, 7, 8, 9, 10, 11])
])
def test_indices(instance_arguments_expected: _TestCase):
	instance, arguments, expected = instance_arguments_expected
	population, from_last, order = arguments
	
	indices = instance.indices(population, from_last = from_last, order = order)
	
	assert list(indices) == expected


@given(
	a_n_plus_b_instances(),
	integers(), booleans(), from_type(str)
)
def test_indices_invalid_order(instance, population, from_last, order):
	assume(order not in ('ascending', 'descending', 'default'))
	
	with pytest.raises(InvalidOrder):
		instance.indices(population, from_last = from_last, order = order)


@given(
	a_n_plus_b_instances(),
	integers(max_value = -1), booleans(), _orders()
)
def test_indices_invalid_number_of_children(
	instance, population, from_last, order
):
	with pytest.raises(InvalidNumberOfChildren):
		instance.indices(population, from_last = from_last, order = order)
