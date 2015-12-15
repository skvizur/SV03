# -*- coding: utf-8 -*-
"""

Charts: Constructors for different chart types in Vega grammar.

"""
import copy
from core import KeyedList
from visualization import Visualization
from data import Data
from transforms import Transform
from values import ValueRef
from properties import PropertySet
from scales import DataRef, Scale
from marks import ValueRef, MarkProperties, MarkRef, Mark
from axes import AxisProperties, Axis

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None


def data_type(data, grouped=False, columns=None, key_on='idx', iter_idx=None):
    '''Data type check for automatic import'''
    if iter_idx:
        return Data.from_mult_iters(idx=iter_idx, **data)
    if pd:
        if isinstance(data, (pd.Series, pd.DataFrame)):
            return Data.from_pandas(data, grouped=grouped, columns=columns,
                                    key_on=key_on)
    if isinstance(data, (list, tuple, dict)):
            return Data.from_iter(data)
    else:
        raise ValueError('This data type is not supported by Vincent.')


class Chart(Visualization):
    """Abstract Base Class for all Chart types"""

    def __init__(self, data=None, columns=None, key_on='idx', iter_idx=None,
                 grouped=False, width=500, height=300, *args, **kwargs):
        """Create a Vega Chart

        Parameters:
        -----------
        data: Tuples, List, Dict, Pandas Series, or Pandas DataFrame
            Input data. Tuple of paired tuples, List of single values,
            dict of key/value pairs, Pandas Series/DataFrame, Numpy ndarray
        columns: list, default None
            Pandas DataFrame columns to plot.
        key_on: string, default 'idx'
            Pandas DataFrame column to key on, if not index
        iter_index: string, default None
            Pass an index key if data is a dict of multiple iterables. Ex:
            {'x': [0, 1, 2, 3, 4, 5], 'y': [6, 7, 8, 9, 10]}
        width: int, default 960
            Chart width
        height: int, default 500
            Chart height
        grouped: boolean, default False
            Pass true for grouped charts. Currently only enabled for Pandas
            DataFrames

        Output:
        -------
        Vega Chart

        Example:
        -------
        >>>vis = vincent.Chart([10, 20, 30, 40, 50], width=200, height=100)

        """

        super(Chart, self).__init__(*args, **kwargs)

        self.width, self.height = width, height
        self.padding = {'top': 10, 'left': 50, 'bottom': 50, 'right': 100}
        self.columns = columns
        self._is_datetime = False

        #Data
        if data is None:
            raise ValueError('Please initialize the chart with data.')

        if isinstance(data, (list, tuple, dict)):
            if not data:
                raise ValueError('The data structure is empty.')
        if isinstance(data, (pd.Series, pd.DataFrame)):
            if isinstance(data.index, pd.DatetimeIndex):
                self._is_datetime = True

        #Using a vincent KeyedList here
        self.data['table'] = (data_type(data, grouped=grouped, columns=columns,
                              key_on=key_on, iter_idx=iter_idx))


class Bar(Chart):
    """Vega Bar chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Bar Chart"""

        super(Bar, self).__init__(*args, **kwargs)

        #Scales
        self.scales['x'] = Scale(name='x', type='ordinal', range='width',
                                 domain=DataRef(data='table', field="data.idx"))
        self.scales['y'] = Scale(name='y', range='height', nice=True,
                                 domain=DataRef(data='table', field="data.val"))
        self.axes.extend([Axis(type='x', scale='x'),
                          Axis(type='y', scale='y')])

        #Marks
        enter_props = PropertySet(x=ValueRef(scale='x', field="data.idx"),
                                  y=ValueRef(scale='y', field="data.val"),
                                  width=ValueRef(scale='x', band=True,
                                                 offset=-1),
                                  y2=ValueRef(scale='y', value=0))

        update_props = PropertySet(fill=ValueRef(value='steelblue'))

        mark = Mark(type='rect', from_=MarkRef(data='table'),
                    properties=MarkProperties(enter=enter_props,
                                              update=update_props))

        self.marks.append(mark)


class Line(Bar):
    """Vega Line chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Line Chart"""

        super(Line, self).__init__(*args, **kwargs)

        #Line Updates
        self.scales['x'].type = 'linear'
        self.scales['y'].type = 'linear'
        if self._is_datetime:
            self.scales['x'].type = 'time'

        self.scales['color'] = Scale(name='color', type='ordinal',
                                     domain=DataRef(data='table', field='data.col'),
                                     range='category20')

        del self.marks[0]
        transform = MarkRef(data='table',
                            transform=[Transform(type='facet', keys=['data.col'])])
        enter_props = PropertySet(x=ValueRef(scale='x', field="data.idx"),
                                  y=ValueRef(scale='y', field="data.val"),
                                  stroke=ValueRef(scale="color", field='data.col'),
                                  stroke_width=ValueRef(value=2))
        new_mark = Mark(type='group', from_=transform,
                        marks=[Mark(type='line',
                                    properties=MarkProperties(enter=enter_props))])
        self.marks.append(new_mark)


class Scatter(Line):
    """Vega Scatter chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Scatter Chart"""

        super(Scatter, self).__init__(*args, **kwargs)

        #Scatter updates

        self.marks[0].marks[0].type = 'symbol'
        del self.marks[0].marks[0].properties.enter.stroke
        del self.marks[0].marks[0].properties.enter.stroke_width
        self.marks[0].marks[0].properties.enter.fill = ValueRef(scale='color',
                                                                field='data.col')
        self.marks[0].marks[0].properties.enter.size = ValueRef(value=100)


class Area(Line):
    """Vega Area Chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Area Chart"""

        super(Area, self).__init__(*args, **kwargs)

        del self.marks[0].marks[0].properties.enter.stroke
        del self.marks[0].marks[0].properties.enter.stroke_width

        self.marks[0].marks[0].type = "area"
        self.marks[0].marks[0].properties.enter.interpolate = ValueRef(value="monotone")
        self.marks[0].marks[0].properties.enter.y2 = ValueRef(value=0, scale="y")
        self.marks[0].marks[0].properties.enter.fill = ValueRef(scale='color',
                                                                field='data.col')


class StackedArea(Area):
    """Vega Stacked Area Chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Stacked Area Chart"""

        super(StackedArea, self).__init__(*args, **kwargs)

        facets = Transform(type='facet', keys=['data.idx'])
        stats = Transform(type='stats', value='data.val')
        stat_dat = Data(name='stats', source='table', transform=[facets, stats])
        self.data['stats'] = stat_dat

        self.scales['x'].zero = False
        self.scales['y'].domain = DataRef(field='sum', data='stats')

        stackit = Transform(type='stack', point='data.idx', height='data.val')
        self.marks[0].from_.transform.append(stackit)
        self.marks[0].marks[0].properties.enter.y.scale = 'y'
        self.marks[0].marks[0].properties.enter.y.field = 'y'
        del self.marks[0].marks[0].properties.enter.y2.value
        self.marks[0].marks[0].properties.enter.y2.field = 'y2'


class StackedBar(StackedArea):
    """Vega Stacked Bar Chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Stacked Bar Chart"""

        super(StackedBar, self).__init__(*args, **kwargs)

        self.scales['x'].type = 'ordinal'
        del self.scales['x'].zero

        del self.marks[0].marks[0].properties.enter.interpolate
        values = ValueRef(scale='x', band=True, offset=-1)
        self.marks[0].marks[0].properties.enter.width = values
        self.marks[0].marks[0].type = 'rect'


class GroupedBar(StackedBar):
    """Vega Grouped Bar Chart"""

    def __init__(self, *args, **kwargs):
        """Create a Vega Grouped Bar Chart"""

        if 'grouped' not in kwargs:
            kwargs['grouped'] = True

        super(GroupedBar, self).__init__(*args, **kwargs)

        del self.data['stats']

        del self.scales['y'].type
        self.scales['y'].domain.field = 'data.val'
        self.scales['y'].domain.data = 'table'
        self.scales['x'].padding = 0.2

        del self.marks[0].from_.transform[1]
        self.marks[0].from_.transform[0].keys[0] = 'data.idx'
        enter_props = PropertySet(x=ValueRef(scale='x', field="key"),
                                  width=ValueRef(scale='x', band=True))
        self.marks[0].properties = MarkProperties(enter=enter_props)
        self.marks[0].scales = KeyedList()
        self.marks[0].scales['pos'] = Scale(name='pos', type='ordinal',
                                            range='width',
                                            domain=DataRef(field='data.group'))

        self.marks[0].marks[0].properties.enter.width.scale = 'pos'
        self.marks[0].marks[0].properties.enter.y.field = 'data.val'
        self.marks[0].marks[0].properties.enter.x.field = 'data.group'
        self.marks[0].marks[0].properties.enter.x.scale = 'pos'

        del self.marks[0].marks[0].properties.enter.y2.field
        self.marks[0].marks[0].properties.enter.y2.value = 0
