from collections.abc import Callable, Iterable
from typing import Any, ParamSpec, TypeVar

from _pytest.mark import ParameterSet
from hypothesis import example
from hypothesis.strategies import integers, SearchStrategy, tuples

from a_n_plus_b import ANPlusB


_T = TypeVar('_T')
_P = ParamSpec('_P')

_Decorator = Callable[[Callable[_P, _T]], Callable[_P, _T]]

newlines = ['\r\n', '\r', '\n', '\f']
whitespace = ['\t', '\x20'] + newlines
blank = [''] + whitespace


def _make_a_n_plus_b(step_and_offset: tuple[int, int]) -> ANPlusB:
	step, offset = step_and_offset
	
	return ANPlusB(step, offset)


def join(whatever: Iterable[Any]) -> str:
	return ''.join(map(str, whatever))


# Originally from https://stackoverflow.com/a/70312417
def examples(
	parameter_sets: Iterable[ParameterSet | tuple[Any, ...] | Any]
) -> _Decorator[_P, _T]:
	parameter_sets = list(parameter_sets)
	
	def inner(test_case: Callable[_P, _T]) -> Callable[_P, _T]:
		for parameter_set in reversed(parameter_sets):
			if isinstance(parameter_set, ParameterSet):
				parameter_set = parameter_set.values
			
			if not isinstance(parameter_set, tuple):
				parameter_set = tuple([parameter_set])
			
			test_case = example(*parameter_set)(test_case)
		
		return test_case
	
	return inner


def a_n_plus_b_instances(
	step: SearchStrategy[int] = integers(),
	offset: SearchStrategy[int] = integers()
) -> SearchStrategy[ANPlusB]:
	return tuples(step, offset).map(_make_a_n_plus_b)
