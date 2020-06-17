# Loads Apple's and Google's financial for the last 30 days
# Creates, stores and displays a candlestick plot for these data

from pandas_datareader import data
from datetime import datetime, timedelta
from bokeh.plotting import figure, show, output_file


def rect_graph(df, name):
    """takes pandas dataframe and plots rect graph"""

    def hour_to_ms(h):
        """coverts hours to milliseconds"""
        return h * 60 * 60 * 1000


    def incr_decr(opening, closing):
        """takes opening closing prices and returns the price status (increase/decrease/equal)"""
        if opening < closing:
            status = 'increase'
        elif opening > closing:
            status = 'decrease'
        else:
            status = 'equal'
        return status


    # prepare dataframe
    df.name = name
    df['Status'] = [incr_decr(o, c) for o, c in zip(df.Open, df.Close)]
    df['Median'] = (df.Open + df.Close) / 2
    df['Height'] = abs(df.Open - df.Close)

    # main plot
    plot = figure(x_axis_type='datetime',
                    width=1000,
                    height=500,
                    title='candlestick chart',
                    x_axis_label='date',
                    y_axis_label='price',
                    sizing_mode='scale_width')

    plot.grid.grid_line_alpha = 0.3
    plot.ygrid.minor_grid_line_color = '#0000ff'
    plot.ygrid.minor_grid_line_alpha = 0.1

    # glyph line segment showing whole price range
    plot.segment(x0=df.index, y0=df.High, x1=df.index, y1=df.Low, line_color='black')

    # glyphs showing range from opening to closing price, where prices go up
    plot.rect(x=df.index[df.Status == 'increase'],
                y=df.Median[df.Status == 'increase'],
                width=hour_to_ms(12),
                height=df.Height[df.Status == 'increase'],
                fill_color='#00ff00',
                line_color='#000000')

    # glyphs showing range from opening to closing price, where prices go down
    plot.rect(x=df.index[df.Status == 'decrease'],
                y=df.Median[df.Status == 'decrease'],
                width=hour_to_ms(12),
                height=df.Height[df.Status == 'decrease'],
                fill_color='#ff0000',
                line_color='#000000')

    # glyphs where prices stay same
    plot.rect(x=df.index[df.Status == 'equal'],
                y=df.Median[df.Status == 'equal'],
                width=hour_to_ms(12),
                height=df.Height[df.Status == 'equal'],
                fill_color='#666666',
                line_color='#000000')

    # store and show result
    output_file(f'graph-{df.name}.html')
    show(plot)



if __name__ == '__main__':

    # set timeframe
    time_start = datetime.today() - timedelta(days=30)
    time_end = datetime.today()

    # load Apple's financial data from Yahoo
    df_apple = data.DataReader(name='AAPL',
                                data_source='yahoo',
                                start=time_start,
                                end=time_end)

    # load Google's financial data from Yahoo
    df_google = data.DataReader(name='GOOGL',
                                data_source='yahoo',
                                start=time_start,
                                end=time_end)

    # create, store and display graph plots
    rect_graph(df_apple, 'apple')
    rect_graph(df_google, 'google')
