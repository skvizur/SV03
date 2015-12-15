# -*- coding: utf-8 -*-
"""

Transforms: Vincent Data Class for Vega Transform types

"""
from __future__ import (print_function, division)
from core import _assert_is_type, ValidationError, grammar, GrammarClass, LoadError


class Transform(GrammarClass):
    """Container to Transforma metrics

    As detailed in the Vega wiki:

    "A data transform performs operations on a data set prior to visualization.
    Common examples include filtering and grouping (e.g., group data points
    with the same stock ticker for plotting as separate lines).

    All transform definitions must include a "type" parameter,
    which specifies the transform to apply.
    Each transform then has a set of transform-specific parameters."

    """

    @grammar(str)
    def type(value):
        """string: property name in which to store the computed transform value.

        The valid transform types are as follows:
        array, copy, facet, filter, flatten, formula, sort, stats, unique, zip,
        force, geo, geopath, link, pie, stack, treemap, wordcloud

        """

        valid_transforms = ['array', 'copy', 'facet', 'filter', 'flatten',
                            'formula', 'sort', 'stats', 'unique', 'zip',
                            'force', 'geo', 'geopath', 'link', 'pie', 'stack',
                            'treemap', 'wordcloud']

        if value not in valid_transforms:
            raise ValueError('Transform type must be'
                             ' one of {0}'.format(str(valid_transforms)))

    @grammar(list)
    def fields(value):
        """list: Can take data references or object references

        Only used if ``type`` is ``array`` or ``copy``

        """

    @grammar(grammar_type=str, grammar_name='from')
    def from_(value):
        """str: The name of the object to copy values from

        Only used if ``type`` is ``copy``

        """

    @grammar(grammar_type=list, grammar_name='as')
    def as_(value):
        """list: The field names to copy the values to.

        Can be used with the following ``type``:
        ``copy``
        ``unique``
        ``zip``

        """

    @grammar(list)
    def keys(value):
        """list: Each key value corresponds to a single facet in the output.

        Only used if ``type`` is ``facet``
        """

    @grammar(str)
    def sort(value):
        """string: Optional for sorting facet values

        Only used if ``type`` is ``facet``
        """

    @grammar(str)
    def test(value):
        """string: A string containing a javascript filtering expression.

        Ex: d.data.y >= 3

        Only used if ``type`` is ``filter``
        """

    @grammar(str)
    def field(value):
        """string: Property name to store computed formula value.

        Only used if ``type`` is ``formula`` or ``unique``

        See: https://github.com/trifacta/vega/wiki/Data-Transforms#-formula
        """

    @grammar(str)
    def expr(value):
        """string: Javascript expression of a formula, referencing the data as d.

        Only used if ``type`` is formula

        See: https://github.com/trifacta/vega/wiki/Data-Transforms#-formula
        """

    @grammar((str, list))
    def by(value):
        """str, list: a field or list of fields to sort. Can prepend with - to
        sort descending.

        Only used if ``type`` is ``sort``
        """

    @grammar(str)
    def value(value):
        """str: Field for which to compute statistics.

        Only used if ``type`` is ``stats``
        """

    @grammar(bool)
    def median(value):
        """boolean: If true, median statistic will also be computed.

        Only used if ``type`` is stats``
        """

    @grammar(grammar_type=str, grammar_name='with')
    def with_(value):
        """string: Name of dataset to zip to current dataset

        Only used if ``type`` is ``zip``
        """

    @grammar(str)
    def key(value):
        """string: Primary dataset field to match to secondary data

        Only used if ``type`` is ``zip``
        """

    @grammar(grammar_type=str, grammar_name='withKey')
    def with_key(value):
        """string: Field in secondary dataset to match to primary

        Only used if ``type`` is ``zip``
        """

    @grammar(str)
    def links(value):
        """string: Name of link (edge) data set.

        To be used with ``force`` types
        """

    @grammar(list)
    def size(value):
        """list: Dimensions of force layout

        To be used with ``force`` types
        """

    @grammar(int)
    def iterations(value):
        """int: Number of iterations to run force directed layout.

        To be used with ``force`` types
        """

    @grammar((int, str))
    def charge(value):
        """int or string: Strength of the charge each node exerts.

        To be used with ``force`` types
        """

    @grammar(grammar_type=(int, str), grammar_name='linkDistance')
    def link_distance(value):
        """int or string: Determines lenght of the edges, in pixels.

        To be used with ``force`` types
        """

    @grammar(grammar_type=(int, str), grammar_name='linkStrength')
    def link_strength(value):
        """int or string: Determines the tension of the edges.

        To be used with ``force`` types
        """

    @grammar((int, float))
    def friction(value):
        """int or float: Strength of friction force to stabilize layout

        To be used with ``force`` types
        """

    @grammar((int, float))
    def theta(value):
        """int or float: theta parameter for the Barnes-Hut algorithm.

        To be used with ``force`` types
        """

    @grammar((int, float))
    def gravity(value):
        """int or float: Strength of pseudo-gravity force

        To be used with ``force`` types
        """

    @grammar((int, float))
    def alpha(value):
        """int or float: "temperature" parameter to determine node position adjustment

        To be used with ``force`` types
        """

    @grammar(str)
    def point(value):
        """string: Data field determining the points at which to stack. When stacked
        vertically, these are the x-coords.

        To be used with ``stack`` types
        """

    @grammar(str)
    def height(value):
        """string: Data field determining thickness, or height of stacks.

        To be used with ``stack`` types
        """

    @grammar(str)
    def offset(value):
        """string: Baseline offset style. Must be one of the following:

        ``zero``, ``silhouette``, ``wiggle``, ``expand``

         To be used with ``stack`` types
         """
        offsets = ['zero', 'silhouette', 'wiggle', 'expand']
        if value not in offsets:
            raise ValueError('offset must be one of {0}'.format(offsets))

    @grammar(str)
    def order(value):
        """str: The sort order for stack layers. Must be one of the following:

        ``default``, ``reverse``, ``inside-out``

        To be used with ``stack`` types
        """
        orders = ['default', 'reverse', 'inside-out']
        if value not in orders:
            raise ValueError('order must be one of {0}'.format(orders))
