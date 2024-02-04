import re
from typing import TypeVar


T = TypeVar('T')


class Regex:
	'''
	Proxy class for ergonomic syntax.
	'''
	
	__slots__ = ('_raw_pattern', '_compiled')
	
	_raw_pattern: str
	_compiled: re.Pattern[str]
	
	def __init__(self, pattern: str, /) -> None:
		self._raw_pattern = pattern
		self._compiled = re.compile(pattern)
	
	def __str__(self) -> str:
		return self._raw_pattern
	
	def fullmatch(self, text: str, /) -> re.Match[str] | None:
		return self._compiled.fullmatch(text)
	
	def sub(self, replacement: str, text: str, /) -> str:
		return self._compiled.sub(replacement, text)


whitespace = Regex(r'[\t\n\f\r\x20]')
integer = Regex(r'[+-]?\d+')

_blank = _ = Regex(fr'{whitespace}*')

a_n_plus_b = Regex(fr'''(?x)
(?:
	(?P<a>    [+-]?    \d*) [Nn]
	(?P<b>{_} [+-] {_} \d+)?
)
''')
