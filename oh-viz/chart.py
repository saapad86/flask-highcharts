import pandas as pd
import numpy as np
import json
import re
from datetime import datetime
from helpers import *

def convert_type(obj): # if object is not JSON serializable, try this with json.dumps
    d = {'__class__': obj.__class__.__name__,
         '__module__':obj.__module__}
    d.update(obj.__dict__)
    return d

class Chart():
    '''
     A line/area chart class. A chart object is instantiated with :
        title (STRING)
        xlabel (STRING, default is None)
        ylabel (STRING, default is "Number")

    Chart objects contain the necessary information to build a Highcharts Chart.
    '''
    def __init__(self, title="My Chart Title", xlabel=None, ylabel="Number"):
        self.title=title
        self.xlabel=xlabel
        self.ylabel=ylabel
        self.series = []
        self._id = "_".join(re.split('\W+', title))
        self.notes="" #initialize empty

    def __repr__(self):
        return pd.io.json.dumps(self.__dict__)


    def add_series(self, name, data, visible=True, showInLegend=True, chart_type="line", decimals=0, percent=False):
        '''
        INPUT:  series name (STRING)
                data (LIST)
                visible (BOOL)
                showInLegend (BOOL)
                chart_type (STRING, ['line', 'area'], default is 'line')
                decimals (INT) - places after the decimal to appear in tooltip; default is 0 (integer)
                percent (BOOL) - percent sign (%) in tooltip, default False

        OUTPUT: None

        '''
        series = {'name': name,
                  'data' : data,
                  'type' : chart_type,
                  'visible' : visible,
                  'showInLegend' : showInLegend
                 }
        if percent:
            # double {{}} to escape bracket character in python string formatting
            series['pointFormat'] = '{{series.name}}: <b>{{point.y:.{}f}}%</b><br/>'.format(decimals)
        else:
            series['pointFormat'] = '{{series.name}}: <b>{{point.y:,.{}f}}</b><br/>'.format(decimals)

        self.series.append(series)


    def add_notes(self, notes):
        '''
        INPUT: notes (STRING)
        OUTPUT: None

        Fills in Notes field for chart notes that will apear below chart on page.
        '''
        self.notes = notes
