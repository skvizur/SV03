# -*- coding: utf-8 -*-
"""

ValueRef: Generally used in a PropertySet class to define a set of values within a property

"""
from core import grammar, GrammarClass


class ValueRef(GrammarClass):
    """Container for the value-referencing properties of marks

    It is often useful for marks to share properties to maintain consistency
    when parts of the visualization are changed. Additionally, the marks
    themselves may have properties somehow mapped from the data (i.e. mark
    size proportional to some data field). The ``ValueRef`` class can be
    used to either define values locally or reference other fields.

    ValueRefs can reference numbers, strings, or arbitrary objects,
    depending on their use.
    """
    @grammar((str, int, float))
    def value(value):
        """int, float, or string : used for constant values

        This is ignored if the ``field`` property is defined.
        """

    @grammar(str)
    def field(value):
        """string : reference to a field of the data in dot-notation

        The data is taken from the Mark's ``from_`` property. For instance, if
        the data has a definition
        ``[{'x': 2}, {'x': 3}, {'x': 1}]``
        then the data should be referenced as ``data.x``. Note that the first
        element is always `data` regardless of the name of the data.
        """

    @grammar(str)
    def scale(value):
        """string : reference to the name of a ``Scale``

        The scale is applied to the ``value`` and ``field`` attributes.
        """

    @grammar((int, float))
    def mult(value):
        """int or float : multiplier applied to the data after any scaling
        """

    @grammar((int, float))
    def offset(value):
        """int or float : additive offset applied to the data after any
        scaling and multipliers
        """

    @grammar(bool)
    def band(value):
        """boolean : use the range of the scale if applicable

        If this is True and ``scale`` is defined, then the value referenced
        is the range band referenced scale. See the d3 documentation on
        ``ordinal.rangeBand`` for more info.
        """
