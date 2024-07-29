from hypothesis import given
from hypothesis.strategies import integers

from a_n_plus_b import ANPlusB, n
from . import a_n_plus_b_instances


def test_n_pos() -> None:
	instance_1 = +n
	instance_2 = n * 1
	
	assert instance_1 == instance_2
	
	assert instance_1.step == 1
	assert instance_1.offset == 0


def test_n_neg() -> None:
	instance_1 = -n
	instance_2 = n * -1
	
	assert instance_1 == instance_2
	
	assert instance_1.step == -1
	assert instance_1.offset == 0


@given(integers())
def test_n_add(b: int) -> None:
	instance_1 = n + b
	instance_2 = b + n
	
	assert isinstance(instance_1, ANPlusB)
	assert isinstance(instance_2, ANPlusB)
	
	assert instance_1 == instance_2
	
	assert instance_1.step == 1
	assert instance_1.offset == b


@given(integers())
def test_n_sub(inverted_b: int) -> None:
	b = inverted_b * -1
	instance = n - b
	
	assert isinstance(instance, ANPlusB)
	
	assert instance.step == 1
	assert instance.offset == inverted_b


@given(integers())
def test_n_rsub(b: int) -> None:
	instance = b - n
	
	assert isinstance(instance, ANPlusB)
	
	assert instance.step == -1
	assert instance.offset == b


@given(integers())
def test_n_mul(a: int) -> None:
	instance_1 = a * n
	instance_2 = n * a
	
	assert isinstance(instance_1, ANPlusB)
	assert isinstance(instance_2, ANPlusB)
	
	assert instance_1 == instance_2
	
	assert instance_1.step == a
	assert instance_1.offset == 0


@given(a_n_plus_b_instances())
def test_pos(instance: ANPlusB) -> None:
	instance_1 = +instance
	instance_2 = instance * 1
	
	assert instance == instance_1 == instance_2


@given(a_n_plus_b_instances())
def test_neg(instance: ANPlusB) -> None:
	negated_1 = -instance
	negated_2 = instance * -1
	
	assert isinstance(negated_1, ANPlusB)
	assert isinstance(negated_2, ANPlusB)
	
	assert negated_1 == negated_2
	assert instance == -negated_1
	
	assert instance.step == negated_1.step * -1
	assert instance.offset == negated_1.offset * -1


@given(a_n_plus_b_instances(), integers())
def test_add(instance: ANPlusB, c: int) -> None:
	a, b = instance.step, instance.offset
	new_instance_1 = instance + c
	new_instance_2 = c + instance
	
	assert isinstance(new_instance_1, ANPlusB)
	assert isinstance(new_instance_2, ANPlusB)
	
	assert new_instance_1 == new_instance_2
	
	assert new_instance_1.step == a
	assert new_instance_1.offset == b + c


@given(a_n_plus_b_instances(), integers())
def test_sub(instance: ANPlusB, c: int) -> None:
	a, b = instance.step, instance.offset
	new_instance = instance - c
	
	assert isinstance(new_instance, ANPlusB)
	
	assert new_instance.step == a
	assert new_instance.offset == b - c


@given(a_n_plus_b_instances(), integers())
def test_rsub(instance: ANPlusB, c: int) -> None:
	a, b = instance.step, instance.offset
	new_instance = c - instance
	
	assert isinstance(new_instance, ANPlusB)
	
	assert new_instance.step == -a
	assert new_instance.offset == c - b


@given(a_n_plus_b_instances(), integers())
def test_mul(instance: ANPlusB, c: int) -> None:
	a, b = instance.step, instance.offset
	new_instance_1 = instance * c
	new_instance_2 = c * instance
	
	assert isinstance(new_instance_1, ANPlusB)
	assert isinstance(new_instance_2, ANPlusB)
	
	assert new_instance_1 == new_instance_2
	
	assert new_instance_1.step == a * c
	assert new_instance_1.offset == b * c
