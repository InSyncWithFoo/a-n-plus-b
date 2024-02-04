import pytest
from hypothesis import given, infer
from hypothesis.strategies import from_type, integers, SearchStrategy, tuples

from a_n_plus_b import ANPlusB, IncorrectUseOfConstructor
from . import a_n_plus_b_instances


_EqTestCase = tuple[ANPlusB, '_ANPlusBSubclass', bool]


class _ANPlusBSubclass(ANPlusB):
	pass


def _make_eq_test_case(example: tuple[int, int]) -> _EqTestCase:
	step, offset = example
	
	return ANPlusB(step, offset), _ANPlusBSubclass(step, offset), True


def _eq_test_group() -> SearchStrategy[_EqTestCase]:
	return tuples(integers(), integers()).map(_make_eq_test_case)


@given(integers(), integers())
def test_construction(step, offset):
	instance = ANPlusB(step, offset)
	
	assert instance.step == step
	assert instance.offset == offset


@given(integers())
def test_construction_single_argument(offset):
	instance = ANPlusB(offset)
	
	assert instance.step == 0
	assert instance.offset == offset


@given(infer)
def test_construction_invalid(text: str):
	with pytest.raises(IncorrectUseOfConstructor):
		ANPlusB(text)  # noqa


@pytest.mark.parametrize(('instance', 'expected'), [
	(ANPlusB(0, -2), '-2'),
	(ANPlusB(0, 0), '0'),
	(ANPlusB(0, 2), '2'),
	
	(ANPlusB(1, -3), 'n-3'),
	(ANPlusB(1, 0), 'n'),
	(ANPlusB(1, 3), 'n+3'),
	
	(ANPlusB(-1, -4), '-n-4'),
	(ANPlusB(-1, 0), '-n'),
	(ANPlusB(-1, 4), '-n+4'),
	
	(ANPlusB(3, 4), '3n+4'),
	(ANPlusB(3, 0), '3n'),
	(ANPlusB(3, -5), '3n-5'),
	
	(ANPlusB(-4, 5), '-4n+5'),
	(ANPlusB(-4, 0), '-4n'),
	(ANPlusB(-4, -6), '-4n-6')
])
def test_str(instance, expected):
	assert str(instance) == expected
	assert repr(instance) == f'{ANPlusB.__name__}({expected})'


@given(a_n_plus_b_instances())
def test_values(instance):
	a, b = instance.step, instance.offset
	
	for index, value in zip(range(10), instance.values()):
		assert value == a * index + b


@given(a_n_plus_b_instances(), integers(min_value = 0))
def test_values_contain_getitem(instance, index):
	a, b = instance.step, instance.offset
	value = instance.values()[index]
	
	assert value == a * index + b
	assert value in instance.values()


@given(
	a_n_plus_b_instances(),
	from_type(object).filter(lambda o: not isinstance(o, int))
)
def test_values_not_contain(instance, item):
	assert item not in instance.values()


@given(a_n_plus_b_instances(), integers(max_value = -1))
def test_getitem_invalid(instance, index):
	with pytest.raises(IndexError):
		_ = instance.values()[index]


@given(a_n_plus_b_instances())
def test_eq(this):
	a, b = this.step, this.offset
	that = ANPlusB(a, b)
	
	assert this == that
	assert hash(this) == hash(that) == hash((a, b))


@pytest.mark.parametrize(('this', 'that', 'expected'), [
	(ANPlusB(0, 0), _ANPlusBSubclass(0, 0), True),
	(_ANPlusBSubclass(0, 0), ANPlusB(0, 0), True),

])
def test_eq_subclass(this, that, expected):
	assert (this == that) is expected
