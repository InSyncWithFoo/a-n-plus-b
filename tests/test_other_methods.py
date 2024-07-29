import pytest
from hypothesis import given, infer
from hypothesis.strategies import from_type, integers

from a_n_plus_b import ANPlusB, IncorrectUseOfConstructor
from . import a_n_plus_b_instances


_EqTestCase = tuple[ANPlusB, '_ANPlusBSubclass', bool]


class _ANPlusBSubclass(ANPlusB):
	pass


@given(integers(), integers())
def test_construction(step: int, offset: int) -> None:
	instance = ANPlusB(step, offset)
	
	assert instance.step == step
	assert instance.offset == offset


@given(integers())
def test_construction_single_argument(offset: int) -> None:
	instance = ANPlusB(offset)
	
	assert instance.step == 0
	assert instance.offset == offset


@given(infer)
def test_construction_invalid(text: str) -> None:
	with pytest.raises(IncorrectUseOfConstructor):
		ANPlusB(text)  # type: ignore  # noqa


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
def test_str(instance: ANPlusB, expected: str) -> None:
	assert str(instance) == expected
	assert repr(instance) == f'{ANPlusB.__name__}({expected})'


@given(a_n_plus_b_instances())
def test_values(instance: ANPlusB) -> None:
	a, b = instance.step, instance.offset
	
	for index, value in zip(range(10), instance.values()):
		assert value == a * index + b


@given(a_n_plus_b_instances(), integers(min_value = 0))
def test_values_contain_getitem(instance: ANPlusB, index: int) -> None:
	a, b = instance.step, instance.offset
	value = instance.values()[index]
	
	assert value == a * index + b
	assert value in instance.values()


@given(
	a_n_plus_b_instances(),
	from_type(object).filter(lambda o: not isinstance(o, int))
)
def test_values_not_contain(instance: ANPlusB, item: object) -> None:
	assert item not in instance.values()


@given(a_n_plus_b_instances(), integers(max_value = -1))
def test_getitem_invalid(instance: ANPlusB, index: int) -> None:
	with pytest.raises(IndexError):
		_ = instance.values()[index]


@given(a_n_plus_b_instances())
def test_eq(this: ANPlusB) -> None:
	a, b = this.step, this.offset
	that = ANPlusB(a, b)
	
	assert this == that
	assert hash(this) == hash(that) == hash((a, b))


@pytest.mark.parametrize(('this', 'that', 'expected'), [
	(ANPlusB(-2, -3), ANPlusB(-2, -3), True),
	(ANPlusB(-1, 0), ANPlusB(-1, 0), True),
	(ANPlusB(0, -5), ANPlusB(0, -5), True),
	(_ANPlusBSubclass(-4, -3), _ANPlusBSubclass(-4, -3), True),
	(_ANPlusBSubclass(-1, -2), _ANPlusBSubclass(-1, -2), True),
	(_ANPlusBSubclass(0, 0), _ANPlusBSubclass(0, 0), True),
	(ANPlusB(0, 0), _ANPlusBSubclass(0, 0), True),
	(_ANPlusBSubclass(0, 0), ANPlusB(0, 0), True),
	(ANPlusB(3, 4), ANPlusB(4, 3), False),
	(_ANPlusBSubclass(3, 4), _ANPlusBSubclass(4, 3), False),
	(ANPlusB(-2, -3), ANPlusB(-4, -5), False),
	(_ANPlusBSubclass(-1, -2), _ANPlusBSubclass(-3, -4), False),
])
def test_eq_subclass(this: ANPlusB, that: ANPlusB, expected: bool) -> None:
	assert (this == that) is expected
