from collections.abc import Callable, Iterable
from typing import Any

from _pytest.mark import ParameterSet
from hypothesis import example
from hypothesis.strategies import composite, DrawFn, integers, SearchStrategy

from a_n_plus_b import ANPlusB


type _Decorator[**P, T] = Callable[[Callable[P, T]], Callable[P, T]]

newlines = ['\r\n', '\r', '\n', '\f']
whitespace = ['\t', ' ', *newlines]
blank = ['', *whitespace]


def join(whatever: Iterable[Any]) -> str:
	return ''.join(map(str, whatever))


# Originally from https://stackoverflow.com/a/70312417
def examples[**P, T](
	parameter_sets: Iterable[ParameterSet | tuple[Any, ...] | Any]
) -> _Decorator[P, T]:
	parameter_sets = list(parameter_sets)
	
	def inner(test_case: Callable[P, T]) -> Callable[P, T]:
		for parameter_set in reversed(parameter_sets):
			if isinstance(parameter_set, ParameterSet):
				parameter_set = parameter_set.values
			
			if not isinstance(parameter_set, tuple):
				parameter_set = tuple([parameter_set])
			
			test_case = example(*parameter_set)(test_case)
		
		return test_case
	
	return inner


@composite
def a_n_plus_b_instances(
	draw: DrawFn,
	steps: SearchStrategy[int] = integers(),
	offsets: SearchStrategy[int] = integers()
) -> ANPlusB:
	return ANPlusB(draw(steps), draw(offsets))
