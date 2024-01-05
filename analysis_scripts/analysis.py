#!/usr/bin/env python3

import rosbag
from matplotlib import pyplot as plt

# Open the ROS bags for stationary and walking data
stationary_data_bag = rosbag.Bag('stationary_data.bag')
walking_data_bag = rosbag.Bag('walking_data.bag')

# Initialize lists to store GPS data
stationary_easting = []
stationary_northing = []
stationary_timestamps = []

walking_easting = []
walking_northing = []
walking_timestamps = []

# Extract GPS data from the stationary ROS bag
for topic, msg, t in stationary_data_bag.read_messages(topics=['/GPS']):
    stationary_easting.append(msg.UTM_easting)
    stationary_northing.append(msg.UTM_northing)
    stationary_timestamps.append(msg.header.stamp.secs)

# Extract GPS data from the walking ROS bag
for topic, msg, t in walking_data_bag.read_messages(topics=['/GPS']):
    walking_easting.append(msg.UTM_easting)
    walking_northing.append(msg.UTM_northing)
    walking_timestamps.append(msg.header.stamp.secs)

# Calculate relative values for GPS data
Easting_stationary = [e - min(stationary_easting) for e in stationary_easting]
Northing_stationary = [n - min(stationary_northing) for n in stationary_northing]
Easting_walking = [e - min(walking_easting) for e in walking_easting]
Northing_walking = [n - min(walking_northing) for n in walking_northing]

# Create subplots to visualize the data
plt.figure(figsize=(12, 8))

# Subplot 1: Stationary Data - UTM Easting and Northing vs. Time
plt.subplot(2, 2, 1)
plt.plot(stationary_timestamps, Easting_stationary, 'r', label='UTM-Easting')
plt.plot(stationary_timestamps, Northing_stationary, 'b', label='UTM-Northing')
plt.ylim(-0.01, 0.07)
plt.title("Stationary GPS Data")
plt.ylabel("UTM Easting,Northing")
plt.xlabel("Time")

# Subplot 2: Stationary Data - UTM Northing vs. UTM Easting
plt.subplot(2, 2, 2)
plt.plot(stationary_easting, stationary_northing, 'r')
plt.title("Stationary GPS Data")
plt.ylabel("UTM-Northing")
plt.xlabel("UTM-Easting")

# Subplot 3: Walking Data - UTM Easting and Northing vs. Time
plt.subplot(2, 2, 3)
plt.plot(walking_timestamps, Easting_walking, 'r', label='UTM-Easting')
plt.plot(walking_timestamps, Northing_walking, 'b', label='UTM-Northing')
plt.title("Walking GPS Data")
plt.ylabel("UTM-Easting, Northing")
plt.xlabel("Time")

# Subplot 4: Walking Data - UTM Northing vs. UTM Easting
plt.subplot(2, 2, 4)
plt.plot(walking_easting, walking_northing, 'r')
plt.title("Walking GPS Data")
plt.xlabel("UTM-Easting")
plt.ylabel("UTM-Northing")

plt.tight_layout()
plt.show()

# Close the ROS bags
stationary_data_bag.close()
walking_data_bag.close()
