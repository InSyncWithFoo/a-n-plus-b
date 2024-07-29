from hypothesis import given
from hypothesis.strategies import integers, sampled_from

from a_n_plus_b import ANPlusB, n


@given(integers())
def test_add(b: int) -> None:
	instance_1 = n + b
	instance_2 = b + n
	
	assert isinstance(instance_1, ANPlusB)
	assert isinstance(instance_2, ANPlusB)
	
	assert instance_1 == instance_2
	
	assert instance_1.step == 1
	assert instance_1.offset == b


@given(integers())
def test_sub(inverted_b: int) -> None:
	b = inverted_b * -1
	instance = n - b

	assert isinstance(instance, ANPlusB)
	assert instance.step == 1
	assert instance.offset == inverted_b


@given(integers())
def test_mul(a: int) -> None:
	instance_1 = a * n
	instance_2 = n * a
	
	assert isinstance(instance_1, ANPlusB)
	assert isinstance(instance_2, ANPlusB)

	assert instance_1 == instance_2
	
	assert instance_1.step == a
	assert instance_1.offset == 0


@given(
	integers(min_value = 0), sampled_from([1, -1]), 
	integers(min_value = 0), sampled_from([1, -1])
)
def test_math(
	absolute_a: int, a_sign: int,
	absolute_b: int, b_sign: int
) -> None:
	a = absolute_a * a_sign
	b = absolute_b * b_sign
	
	instance_1 = a * n + b
	instance_2 = n * a + b
	instance_3 = b + a * n
	instance_4 = b + n * a
	
	for instance in [instance_1, instance_2, instance_3, instance_4]:
		assert isinstance(instance, ANPlusB)
	
	assert instance_1 == instance_2 == instance_3 == instance_4
	
	assert instance_1.step == a
	assert instance_1.offset == b
