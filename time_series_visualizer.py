import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=[0]).set_index('date')

# Clean data
df = df[
    (df['value'] >= df.quantile(0.025)['value']) &
    (df['value'] <= df.quantile(0.975)['value'])
]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12, 5))

    # Now add axes to figure. The add_axes() method requires a list object of 4 elements corresponding to left, bottom,
    # width and height of the figure. Each number must be between 0 and 1 −
    ax = fig.add_axes([0, 0, 1, 1])

    # Set labels for x and y axis as well as title
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    ax.plot(df, 'r')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    year_month = df.groupby([df.index.year.values, df.index.month_name().values]).sum()

    year_month = year_month.reset_index(level=[0, 1])
    year_month.columns = ['Years', 'month', 'views']
    year_month = year_month.set_index(['month'])

    cats = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
            'November', 'December']
    year_month.index = pd.CategoricalIndex(year_month.index, categories=cats, ordered=True)
    year_month = year_month.sort_index()

    year_month = year_month.reset_index().set_index(['Years', 'month'])['views']

    fig = plt.figure(figsize=[11, 6])
    ax = fig.add_subplot(111)
    year_month.unstack().plot(kind='bar', figsize=(10, 10), ax=ax)
    plt.ylabel('Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_cln = df.copy()

    df_cln['Year'] = df_cln.index.year.values
    df_cln['Month'] = df_cln.index.month_name().values

    df_cln.columns = ['Page Views', 'Year', 'Month']

    df_cln['Month'] = df_cln['Month'].str[:3]
    cats = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_cln['Month'] = pd.CategoricalIndex(df_cln['Month'], categories=cats, ordered=True)

    fig, ax = plt.subplots(1, 2)
    fig.set_figheight(6)
    fig.set_figwidth(15)

    sns.boxplot(x="Year", y="Page Views", data=df_cln, palette='rainbow', ax=ax[0]).set(
        title='Year-wise Box Plot (Trend)')

    sns.boxplot(x="Month", y="Page Views", data=df_cln, palette='rainbow', ax=ax[1]).set(
        title='Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
