import pandas as pd
from geopy.distance import geodesic
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import numpy as np


class Create_price():
    def __init__():
        data = pd.read_excel('Data_Train.xlsx')
        data.loc[data['Total_Stops'] == '4 stops', 'Total_Stops'] = 4
        data.loc[data['Total_Stops'] == '3 stops', 'Total_Stops'] = 3
        data.loc[data['Total_Stops'] == '2 stops', 'Total_Stops'] = 2
        data.loc[data['Total_Stops'] == '1 stop', 'Total_Stops'] = 1
        data.loc[data['Total_Stops'] == 'non-stop', 'Total_Stops'] = 0
        data = data.dropna()

        source_coordinates = {
            "Bangalore": (12.9716, 77.5946),
            "Kolkata": (22.5726, 88.3639),
            "Delhi": (28.7041, 77.1025),
            "Chennai": (13.0827, 80.2707), }

        destination_coordinates = {
            "New Delhi": (28.6139, 77.2090),
            "Bangalore": (12.9716, 77.5946),
            "Cochin": (9.9312, 76.2673),
            "Kolkata": (22.5726, 88.3639),
            "Delhi": (28.7041, 77.1025),
            "Hyderabad": (17.3850, 78.4867)
        }

        def calculate_distance(row):
            source_coords = source_coordinates.get(row['Source'])
            dest_coords = destination_coordinates.get(row['Destination'])
            return geodesic(source_coords, dest_coords).kilometers

        def time_to_minutes(time_str):
            parts = time_str.split()
            hours = 0
            minutes = 0
            for part in parts:
                if 'h' in part:
                    # Убираем 'h' и переводим в число
                    hours = int(part.replace('h', ''))
                elif 'm' in part:
                    # Убираем 'm' и переводим в число
                    minutes = int(part.replace('m', ''))
            return hours * 60 + minutes

        data['Track'] = data.apply(calculate_distance, axis=1)
        del data['Route']
        data['Duration'] = data['Duration'].apply(time_to_minutes)
        data = data.sort_values('Price')
        print(data['Price'].min(), data['Price'].max())

        X_1 = data['Duration'].to_numpy()
        X_2 = data['Total_Stops'].to_numpy()
        X_3 = data['Track'].to_numpy()
        # X_1 = (X_1 - X_1.min()) / (X_1.max() - X_1.min())
        # X_2 = (X_2 - X_2.min()) / (X_2.max() - X_2.min())
        # X_3 = (X_3 - X_3.min()) / (X_3.max() - X_3.min())
        y = data['Price'].to_numpy()
        y_max = max(y)
        y_min = min(y)
        # y = (y - y.min()) / (y.max() - y.min())
        def normalization(elem): return (elem - y_min) / (y_max - y_min)
        def restored(array): return array * (y_max - y_min) + y_min

        X = np.concatenate((X_1, X_2, X_3)).reshape(10682, -1)
        # X = X_1.reshape(10682, -1)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        model = DecisionTreeRegressor()

        n_epochs = 1
        train_errors, test_errors = [], []

        for epoch in range(n_epochs):
            model.fit(X_train, y_train)

        return model


price = Create_price.__init__()
pred = np.array([40, 0, 10000]).reshape(1, -1)
print(price.predict(pred))
