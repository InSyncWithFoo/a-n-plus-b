'''
Helper singleton for creating :class:`ANPlusB` objects. 
'''

from __future__ import annotations

from ._a_n_plus_b import ANPlusB


class _N:
	'''
	The type of the ``n`` symbol, implementing various magic methods.
	'''
	
	def __add__(self, other: int) -> ANPlusB:
		return ANPlusB(1, other)
	
	def __radd__(self, other: int) -> ANPlusB:
		return self + other
	
	def __sub__(self, other: int) -> ANPlusB:
		return self + -other
	
	def __mul__(self, other: int) -> ANPlusB:
		return ANPlusB(other, 0)
	
	def __rmul__(self, other: int) -> ANPlusB:
		return self * other


n = _N()
