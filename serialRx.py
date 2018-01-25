"""
Serial port data Rx
Author: Oskar Staniszewski
Wroclaw 2018
"""
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.dates import DateFormatter
import datetime
import serial


serial_port = serial.Serial('COM3', '9600', timeout=None)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(15,7))
fig.autofmt_xdate()
xaxis_data = []
xmin = datetime.datetime.now()
xmax = xmin + datetime.timedelta(minutes=30)


# Temperature subplot settings
temp_subplot = plt.subplot(3, 1, 1)
temp_subplot.grid()
temp_subplot.set_title('Temperature')
temp_subplot.set_ylabel('Celsius degrees [C]')
# Set the OY axis
temp_yaxis_data = []
temp_subplot.set_ylim(10, 50)
# Set the OX axis
temp_subplot.xaxis_date()
#temp_subplot.xaxis.set_major_formatter(DateFormatter('%a %d\n%H:%M:%S'))
temp_subplot.get_xaxis().set_ticklabels([])
temp_subplot.set_xlim(xmin, xmax)
# Temperature data setter
temp_plot_data, = temp_subplot.plot([], [], '-')


# Humidity subplot settings
hum_subplot = plt.subplot(3, 1, 2)
hum_subplot.grid()
hum_subplot.set_title('Humidity')
hum_subplot.set_ylabel('Humidity [%]')
# Set the OY axis
hum_yaxis_data = []
hum_subplot.set_ylim(10, 80)
# Set the OX axis
hum_subplot.xaxis_date()
#hum_subplot.xaxis.set_major_formatter(DateFormatter('%a %d\n%H:%M:%S'))
hum_subplot.get_xaxis().set_ticklabels([])
hum_subplot.set_xlim(xmin, xmax)
# Humidity data setter
hum_plot_data, = hum_subplot.plot([], [], '-')


# Pressure subplot settings
pres_subplot = plt.subplot(3, 1, 3)
pres_subplot.grid()
pres_subplot.set_title('Pressure')
pres_subplot.set_ylabel('Pressure [hPa]')
# Set the OY axis
pres_yaxis_data = []
pres_subplot.set_ylim(950, 1400)
# Set the OX axis
pres_subplot.xaxis_date()
pres_subplot.xaxis.set_major_formatter(DateFormatter('%a %d\n%H:%M:%S'))
pres_subplot.set_xlim(xmin, xmax)
# Pressure data setter
pres_plot_data, = pres_subplot.plot([], [], '-')



def animate(i):

    serial_data = str(serial_port.readline())
    if (serial_data != 0):
        # If recieved -> put data to plot
        temperature = float(serial_data.strip()[serial_data.find('E') + 1:serial_data.find('H')])
        humidity = float(serial_data.strip()[serial_data.find('H') + 1:serial_data.find('P')])
        pressure = float(serial_data.strip()[serial_data.find('P') + 1:serial_data.find('L')])
        pressure = pressure / 100.0
        timer = datetime.datetime.now()
        xaxis_data.append(timer)
        temp_yaxis_data.append(temperature)
        hum_yaxis_data.append(humidity)
        pres_yaxis_data.append(pressure)       
             
        if timer >= xmax:
            new_xmax = timer + datetime.timedelta(minutes=30)
            temp_subplot.set_xlim(xmin, new_xmax)
            hum_subplot.set_xlim(xmin, new_xmax)
            pres_subplot.set_xlim(xmin, new_xmax)
            temp_subplot.figure.canvas.draw()
            hum_subplot.figure.canvas.draw()
            pres_subplot.figure.canvas.draw()


        temp_plot_data.set_data(xaxis_data, temp_yaxis_data)
        hum_plot_data.set_data(xaxis_data, hum_yaxis_data)
        pres_plot_data.set_data(xaxis_data, pres_yaxis_data)

    return temp_plot_data, hum_plot_data, pres_plot_data,


anim = animation.FuncAnimation(fig, animate,
                               frames=200, interval=20, blit=True)


plt.show()
