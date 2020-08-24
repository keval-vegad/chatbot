# Multiple Linear Regression

# Importing the libraries


# find the closest value from column
def get_station_and_deley(stationname,total_minutes, deley_time):
    import numpy as np
    import pandas as pd
    import datetime as dt

    # Importing the dataset
    dataset = pd.read_excel('schedule_for_delay_prediction.xlsx')
    # mark zero values as missing or NaN
    dataset[:] = dataset[:].replace(0, np.NaN)
    # drop rows with missing values
    dataset.dropna(inplace=True)
    print(dataset)
    X = dataset.iloc[:, 1:31].values
    y = dataset.iloc[:, 31].values

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Fitting Multiple Linear Regression to the Training set
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = regressor.predict(X_test)
    dataset1 = pd.DataFrame(
        {'NORWICH': X_test[:, 0], 'NRCHTPJ': X_test[:, 1], 'TRWSSBJ': X_test[:, 2], 'TROWSEJ': X_test[:, 3],
         'DISS': X_test[:, 4], 'HAUGHLEY': X_test[:, 5],
         'STOWMARKET': X_test[:, 6], 'IPSWESJ': X_test[:, 7], 'IPSWICH': X_test[:, 8], 'IPSWHJN': X_test[:, 9],
         'MANNINGTREE': X_test[:, 10], 'COLCHESTER': X_test[:, 11],
         'MARKS TEY': X_test[:, 12], 'WITHAM': X_test[:, 13], 'CHELMSFORD': X_test[:, 14], 'SHENFIELD': X_test[:, 15],
         'BRENTWOOD': X_test[:, 16], 'HAROLD WOOD': X_test[:, 17],
         'GIDEA PARK': X_test[:, 18], 'ROMFORD': X_test[:, 19], 'CHADWELL HEATH': X_test[:, 20],
         'GOODMAYES': X_test[:, 21], 'SEVEN KINGS': X_test[:, 22], 'SOUTH MILFORD': X_test[:, 23],
         'FRSTGTJ': X_test[:, 24], 'MANOR PARK': X_test[:, 25], 'FOREST GATE': X_test[:, 26],
         'STRATFORD': X_test[:, 27], 'BOWJ': X_test[:, 28], 'BETHNAL GREEN': X_test[:, 29]
         })
    print(dataset1)
    dataset1 = dataset1.astype('float64')
    value = total_minutes + deley_time
    index = abs(dataset1[stationname] - value).idxmin() #find the closest value from column
    print("index is: ",index)
    print(dataset1.iloc[[index]])

    y_pred2 = regressor.predict(dataset1.iloc[[index]])
    arrival_time_hours = y_pred2 // 60
    arrival_time_mins = y_pred2 % 60
    print("--->>",arrival_time_hours)
    final_delay = str(int(arrival_time_hours)) + ":" + str(int(arrival_time_mins))
    return final_delay

def get_current_time_at_station(time):
    input_time = time
    t = input_time.split(':')
    total_minutes = int(t[0]) * 60 + int(t[1])
    return total_minutes
def get_delay_time_at_current_station(time):
    current_delay_time = int(time)
    return current_delay_time

if __name__ == '__main__':
    # get_station_and_deley('DISS',get_current_time_at_station('18:00'),10)
    # print(get_station_and_deley('DISS', get_current_time_at_station('18:00'),
    #                             get_delay_time_at_current_station('10')))
    print(get_current_time_at_station('17:00'))
    # print("-----------------data set is printing here-----------------------")
    # print(dataset)
    # print("-----------------X is printing here-----------------------")
    # print(X)
    # print("-----------------Y is printing here-----------------------")
    # print(y)
    # print("-----------------X_train is printing here-----------------------")
    # print(X_train)
    # print("-----------------X test is printing here-----------------------")
    # print(X_test)
    # print("-----------------y_train is printing here-----------------------")
    # print(y_train)
    # print("-----------------y_test is printing here-----------------------")
    # print(y_test)
    # print(y_pred)