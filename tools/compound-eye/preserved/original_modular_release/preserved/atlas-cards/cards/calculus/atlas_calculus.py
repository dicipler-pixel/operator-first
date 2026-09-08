"""Exact finite determinant diagrams. Python >=3.10; requires SymPy.

Domain: finite real symmetric quadratic contributions with labeled ports and a
positive scalar determinant weight. The assembled system being reduced is
positive definite; an attached load may be positive semidefinite, including zero.
The caller supplies the domain certificate; it is not guessed by this module.
This is a determinant calculus, not a general Gaussian integration package.
"""
from dataclasses import dataclass
from typing import Tuple
import sympy as sp


@dataclass(frozen=True)
class Diagram:
    ports: Tuple[str, ...]
    matrix: sp.ImmutableMatrix
    weight: sp.Expr = sp.S.One
    retired: frozenset = frozenset()

    def __post_init__(self):
        ports = tuple(self.ports)
        matrix = sp.ImmutableMatrix(self.matrix)
        if len(set(ports)) != len(ports):
            raise ValueError('Port labels must be unique.')
        if matrix.shape != (len(ports), len(ports)) or matrix != matrix.T:
            raise ValueError('The matrix must be symmetric and match the ports.')
        object.__setattr__(self, 'ports', ports)
        object.__setattr__(self, 'matrix', matrix)
        object.__setattr__(self, 'weight', sp.sympify(self.weight))
        object.__setattr__(self, 'retired', frozenset(self.retired))
        if set(ports) & self.retired:
            raise ValueError('An eliminated coordinate cannot also be exposed.')

    def eliminate(self, internal):
        """Remove specified ports; preserve the Schur response and determinant.

        Positive definiteness ensures an invertible pivot. The algebraic rule
        also works outside that domain whenever the selected pivot is invertible.
        """
        internal = tuple(internal)
        if len(set(internal)) != len(internal) or not set(internal) <= set(self.ports):
            raise ValueError('Elimination needs distinct existing port labels.')
        if not internal:
            return self
        ii = [self.ports.index(p) for p in internal]
        remaining = tuple(p for p in self.ports if p not in internal)
        bb = [self.ports.index(p) for p in remaining]
        D = self.matrix.extract(ii, ii)
        B = self.matrix.extract(ii, bb)
        A = self.matrix.extract(bb, bb)
        if D.det() == 0:
            raise ValueError('Singular pivot: this rewrite is not admissible.')
        response = (A - B.T * D.inv() * B).applyfunc(sp.simplify)
        return Diagram(remaining, response, sp.factor(self.weight * D.det()), self.retired | set(internal))

    def attach(self, other):
        """Glue equal port names by adding their quadratic contributions.

        New port labels are appended in the other diagram's order. All external
        attachments must use exposed ports: eliminated labels are no longer ports.
        """
        if set(other.ports) & self.retired or set(self.ports) & other.retired:
            raise ValueError('An attachment cannot reconnect an eliminated coordinate; use a fresh label for a new coordinate.')
        ports = self.ports + tuple(p for p in other.ports if p not in self.ports)
        matrix = sp.zeros(len(ports))
        for diagram in (self, other):
            for i, a in enumerate(diagram.ports):
                for j, b in enumerate(diagram.ports):
                    matrix[ports.index(a), ports.index(b)] += diagram.matrix[i, j]
        return Diagram(ports, matrix, sp.factor(self.weight * other.weight), self.retired | other.retired)

    def read(self):
        """Close remaining ports with the determinant readout (det empty = 1)."""
        return sp.factor(self.weight * self.matrix.det())


if __name__ == '__main__':
    chain = Diagram(('left', 'inside', 'right'), sp.Matrix([[4,-1,0],[-1,5,-2],[0,-2,3]]))
    reduced = chain.eliminate(('inside',))
    lam = sp.Symbol('lambda', nonnegative=True)
    load = Diagram(('right',), sp.Matrix([[lam]]))
    print('Reduced ports:', reduced.ports)
    print('Boundary response:', reduced.matrix)
    print('Retained determinant weight:', reduced.weight)
    print('Full readout after attachment:', chain.attach(load).read())
    print('Reduced readout after attachment:', reduced.attach(load).read())
