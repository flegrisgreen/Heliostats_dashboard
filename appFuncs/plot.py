import base64
import pandas as pd
from matplotlib.figure import Figure
from matplotlib import dates as mpl_dates
from appFuncs import sql, con, dictionary_convertion
from io import BytesIO

def plot(helio_id):
    # Connect to and read from the tables in the database
    helio = helio_id.split(".", 1)
    helio = ''.join(helio)
    cols = ['battery', 'motor1', 'motor2', 'date']
    data = sql.selectall(con=con, tname=f'helio{helio}', cols=cols)

    # Sort the data that has been read from the database
    battery_vals = []
    motor1_vals = []
    motor2_vals = []
    dates = []
    for val in data:
        val = val.split(':', 1)
        if val[0] == 'battery':
            battery_vals.append(val[1][0:4])
        elif val[0] == 'motor1':
            motor1_vals.append(val[1])
        elif val[0] == 'motor2':
            motor2_vals.append(val[1])
        else:
            dates.append(val[1][0:19])

    # Convert data to correct data types
    df = pd.DataFrame()
    df['battery_vals'] = pd.to_numeric(battery_vals)
    df['motor1_vals'] = pd.to_numeric(motor1_vals)
    df['motor2_vals'] = pd.to_numeric(motor2_vals)
    df['dates'] = pd.to_datetime(dates)
    df.sort_values(by='dates', inplace=True)

    # Configure the battery plot
    graph = Figure()
    graph.gca(title=f'Battery data for heliostat {helio_id}', xlabel='Date', ylabel='Battery Level [V]')
    graph.gca().plot(df.loc[:, 'dates'], df.loc[:, 'battery_vals'], linestyle='solid')
    graph.autofmt_xdate()
    fig = BytesIO()
    graph.savefig(fig, format='png')
    figure = base64.b64encode(fig.getbuffer()).decode('ascii')

    m1graph = Figure()
    m1graph.gca(title=f'Motor 1 data for heliostat {helio_id}', xlabel='Date', ylabel='Motor count [steps]')
    m1graph.gca().plot(df.loc[:, 'dates'], df.loc[:, 'motor1_vals'], linestyle='solid')
    m1graph.autofmt_xdate()
    fig2 = BytesIO()
    m1graph.savefig(fig2, format='png')
    figure2 = base64.b64encode(fig2.getbuffer()).decode('ascii')

    m2graph = Figure()
    m2graph.gca(title=f'Motor 2 data for heliostat {helio_id}', xlabel='Date', ylabel='Motor count [steps]')
    m2graph.gca().plot(df.loc[:, 'dates'], df.loc[:, 'motor2_vals'], linestyle='solid')
    m2graph.autofmt_xdate()
    fig3 = BytesIO()
    m2graph.savefig(fig3, format='png')
    figure3 = base64.b64encode(fig3.getbuffer()).decode('ascii')
    return f'<img src="data:image/png;base64,{figure}"/>', f'<img src="data:image/png;base64,{figure2}"/>', \
           f'<img src="data:image/png;base64,{figure3}"/>'

