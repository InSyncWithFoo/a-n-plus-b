'''
Helper singleton for creating :class:`ANPlusB` objects. 
'''

from __future__ import annotations

from ._a_n_plus_b import ANPlusB


class _N:
	'''
	The type of the ``n`` symbol, implementing various magic methods.
	'''
	
	def __pos__(self) -> ANPlusB:
		'''
		``+n`` is equivalent to ``1n``. 
		'''
		
		return self * 1
	
	def __neg__(self) -> ANPlusB:
		'''
		``-n`` is equivalent to ``-1n``. 
		'''
		
		return self * -1
	
	def __add__(self, other: int) -> ANPlusB:
		'''
		``n + b`` is equivalent to ``1n + b``. 
		'''
		
		return ANPlusB(1, other)
	
	def __radd__(self, other: int) -> ANPlusB:
		'''
		``b + n`` is equivalent to ``1n + b``.
		'''
		
		return self + other
	
	def __sub__(self, other: int) -> ANPlusB:
		'''
		``n - b`` is equivalent to ``1n - b``. 
		'''
		
		return self + -other
	
	def __rsub__(self, other: int) -> ANPlusB:
		'''
		``b - n`` is equivalent to ``-1n + b``. 
		'''
		
		return ANPlusB(-1, other)
	
	def __mul__(self, other: int) -> ANPlusB:
		'''
		``n * a`` is equivalent to ``an + 0``.
		'''
		
		return ANPlusB(other, 0)
	
	def __rmul__(self, other: int) -> ANPlusB:
		'''
		``a * n`` is equivalent to ``an + 0``. 
		'''
		
		return self * other


n = _N()
