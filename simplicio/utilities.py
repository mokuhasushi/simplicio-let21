# Invece di Stack di liblet, uso deque per implementare lo stack. Rispetto a una
# rappresentazione tramite lista, l'accesso all'ultimo elemento accade in O(n)
from collections import deque


class Stack():
    def __init__(self, iterable=None):
        self._stack = deque()
        if iterable is not None:
            for x in iterable:
                self._stack.append(x)
    def peek(self):
        return self._stack[-1]
    def pop(self):
        return self._stack.pop()
    def push(self, element):
        self._stack.append(element)
    def clear(self):
        self._stack.clear()