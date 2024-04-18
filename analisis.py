import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

data = pd.read_csv('datos.csv')

# Convert 'fecha' to datetime
data['fecha'] = pd.to_datetime(data['fecha'])

# Plotting the longitude and latitude over time
plt.figure(figsize=(14, 7))
plt.subplot(2, 1, 1)
plt.plot(data['fecha'], data['latitude'], label='Latitude', color='blue')
plt.title('Latitude Changes Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Latitude')
plt.grid(True)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Hourly ticks
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formatting the date

plt.subplot(2, 1, 2)
plt.plot(data['fecha'], data['longitude'], label='Longitude', color='green')
plt.title('Longitude Changes Over Time')
plt.xlabel('Date and Time')
plt.ylabel('Longitude')
plt.grid(True)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Hourly ticks
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Formatting the date

plt.tight_layout()
plt.show()
exit(0)
# Create a figure to hold all the subplots

# from sklearn.cluster import KMeans

# # Preparing data for clustering
# clustering_data = data[['latitude', 'longitude']]

# # Using KMeans to find clusters
# kmeans = KMeans(n_clusters=5, random_state=0).fit(clustering_data)

# # Assigning cluster labels back to the original data
# data['cluster'] = kmeans.labels_

# # Plotting the clusters
# plt.figure(figsize=(10, 6))
# plt.scatter(data['longitude'], data['latitude'], c=data['cluster'], cmap='viridis', marker='o', alpha=0.5)
# plt.title('Geographical Distribution of Data Points by Cluster')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.colorbar(label='Cluster')
# plt.grid(True)
# plt.show()



# fig, axes = plt.subplots(nrows=len(data['Numero_pendiente'].unique()), ncols=2, figsize=(14, 30))

# # Adjusting the layout
# fig.tight_layout(pad=5.0)

# # Plotting each unique 'Numero_pendiente'
# for index, (name, group) in enumerate(data.groupby('Numero_pendiente')):
#     # Plot latitude over time
#     axes[index, 0].plot(group['fecha'], group['latitude'], marker='o', linestyle='-', markersize=2)
#     axes[index, 0].set_title(f'Latitude Changes Over Time for Numero_pendiente {name}')
#     axes[index, 0].set_xlabel('Date and Time')
#     axes[index, 0].set_ylabel('Latitude')
#     axes[index, 0].grid(True)
#     axes[index, 0].xaxis.set_major_locator(mdates.HourLocator(interval=1))
#     axes[index, 0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

#     # Plot longitude over time
#     axes[index, 1].plot(group['fecha'], group['longitude'], marker='o', linestyle='-', markersize=2)
#     axes[index, 1].set_title(f'Longitude Changes Over Time for Numero_pendiente {name}')
#     axes[index, 1].set_xlabel('Date and Time')
#     axes[index, 1].set_ylabel('Longitude')
#     axes[index, 1].grid(True)
#     axes[index, 1].xaxis.set_major_locator(mdates.HourLocator(interval=1))
#     axes[index, 1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

# plt.show()