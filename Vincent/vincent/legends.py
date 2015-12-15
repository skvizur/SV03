# -*- coding: utf-8 -*-
"""

Legend: Classes to define Vega Legends

"""
from __future__ import (print_function, division)
from core import (initialize_notebook, _assert_is_type, ValidationError,
                  KeyedList, grammar, GrammarClass, LoadError)
from values import ValueRef


class LegendProperties(GrammarClass):
    """Sets of Legend Properties.

    These properties enable custom mark properties for the legend
    elements. Each element can use a standard ValueRef for values.

    """

    @grammar(ValueRef)
    def title(value):
        """Legend title properties """

    @grammar(ValueRef)
    def labels(value):
        """Legend label properties"""

    @grammar(ValueRef)
    def symbols(value):
        """Legend symbol properties"""

    @grammar(ValueRef)
    def gradient(value):
        """Continuous color gradient for legend"""

    @grammar(ValueRef)
    def legend(value):
        """Legend styling properties"""


class Legend(GrammarClass):
    """Definition for Vega Legends

    Legends visualize scales, and take one or more scales as their input.
    They can be customized via a LegendProperty object.

    """

    @grammar(str)
    def size(value):
        """The name of the scale that determines an item's size"""

    @grammar(str)
    def shape(value):
        """The name of the scale that determines an item's shape"""

    @grammar(str)
    def fill(value):
        """The name of the scale that determines an item's fill color"""

    @grammar(str)
    def stroke(value):
        """The name of the scale that determine's stroke color"""

    @grammar(str)
    def orient(value):
        """The orientation of the legend.

        Must be one of 'left' or 'right'
        """

        if value not in ('left', 'right'):
            raise ValueError('Value must be one of "left" or "right".')

    @grammar(int)
    def offset(value):
        """Pixel offset from figure"""

    @grammar(str)
    def title(value):
        """The Legend title"""

    @grammar(str)
    def format(value):
        """Optional formatting pattern for legend labels.

        See the D3 formatting pattern:
        https://github.com/mbostock/d3/wiki/Formatting
        """

    @grammar(list)
    def values(value):
        """Explicitly set visible legend values"""

    @grammar(LegendProperties)
    def properties(value):
        """Optional mark property definitions for custom styling"""
