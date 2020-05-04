
import cx_Oracle
import chart_studio.plotly as py
import plotly.graph_objs as go
import re
import chart_studio.dashboard_objs as dashboard

username = 'crispyyv'
password = '19680401'
database = 'localhost/xe'


def fileId_from_url(url):
    """Return fileId from a url."""
    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1:]
    return raw_fileId.replace('/', ':')


conn = cx_Oracle.connect(username, password, database)
cursor = conn.cursor()

firstQuery = """select
    count(fire_id) as "count_of_fire",
    round(latitude, 1) || ' ' || round(longitude, 1) as "coordinate"
    from fire_params_locations
    WHERE
    round(fire_params_locations.latitude, 1) >= - 15.1 and round(fire_params_locations.latitude, 1) <= -14.5
    AND round(fire_params_locations.longitude, 1) >= 135.2 and round(fire_params_locations.longitude, 1) <= 140.1 group by round(latitude, 1) || ' ' || round(longitude, 1)


"""

secondQuery = """
    SELECT
    fire_params_locations.brightness,
    COUNT(fire_params_locations.params_id) AS "count of brightness"
FROM
    fire_params_locations
GROUP BY
    fire_params_locations.brightness
"""

thirdQuery = """
 SELECT
    fire_id,
    confidence
FROM
    fire_params_locations
"""

cursor.execute(firstQuery)

coords = []
fire_count = []

for row in cursor:
    print(row)
    fire_count += [row[0]]
    coords +=[row[1]]
data = [go.Bar(
    x=coords,
    y=fire_count
)]

layout = go.Layout(
    title='Загальна кількість пожарів, за заданими координатами',
    xaxis=dict(
        title='Fire info',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Count of fires',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig = go.Figure(data=data, layout=layout)

fires_count = py.plot(fig, filename='fires-count')

cursor.execute(secondQuery)

brightness = []
count_of_brightness = []

for row in cursor:
    brightness += [row[0]]
    count_of_brightness += [row[1]]

pie = go.Pie(labels=brightness, values=count_of_brightness)
fire_brightness = py.plot([pie], filename ='fire-brightness')

cursor.execute(thirdQuery)

fire_id = []
cofidence = []

for row in cursor:
    fire_id += [row[0]]
    cofidence += [row[1]]


car_prices = go.Scatter(
    x=cofidence,
    y=fire_id,
    mode='lines+markers'
)

data = [car_prices]
fire_confidence = py.plot(data, filename='fire-confidence')

my_dboard = dashboard.Dashboard()

fires_count = fileId_from_url(fires_count)
fire_brightness = fileId_from_url(fire_brightness)
fire_confidence = fileId_from_url(fire_confidence)

box_1 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fires_count,
    'title': 'Кількість в заданих координатах'
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fire_brightness,
    'title': 'Яркость та пожар'
}

box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': fire_confidence,
    'title': 'Пожар та впевненість'
}

my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)
my_dboard.insert(box_3, 'left', 2)

py.dashboard_ops.upload(my_dboard, 'Fire in Australia')
