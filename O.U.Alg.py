#Roadmap for OU Model Design
#Step1: Figure out innerworkings of Ornstein Uhlenbeck Algorithm
#Step2: Figure out what variables you want in it. think price open or close, volume, minute data, etc
#Step3: Modifications?
#Step4: Pick a pairs trading set i.e HO&CL
#Step5: Figure out how to iterate through a csv file of historical data, one by one
#Step6: As you go, generate a trading signal into a new csv about when to get in a trade, and when to get out. 
#Step7: Calculate PNL of each trade
#Step8: Calculate total balance, percent of capital risked, establish a risk model that shows 2 stdev VAR

# theta: Speed of mean reversion
# mu: Long-term mean
# sigma: Volatility (how much prices deviate from the mean)
# X0: Initial value
# T: Total time
# dt: Time step interval, i.e 1 day, 1 minute, etc


# Begin Libraries 

import pandas as pd 
# Used to handle tabular data like CSV files, making it easy to load, manipulate, and process data.

import numpy as np 
# Provides numerical operations, especially for arrays and mathematical functions.
# List is used to collect items that usually consist of elements of multiple data types. 
# An array is also a vital component that collects several items of the same data type. 
# List cannot manage arithmetic operations. Array can manage arithmetic operations.

import time 
# Used to introduce delays (time.sleep()), simulating real-time data processing.



#Begin Model

# Function to simulate real-time processing
def process_data_realtime(csv_file, dt, initial_theta=0.5, initial_mu=0.0, initial_sigma=0.1):
    # Load data
    data = pd.read_csv(csv_file) # Defines the data variable and tells it where to read using pandas
    prices = data['Spread'].values # Defines our prices variable which is equal to being within 'data' and under the name 'spread'
    dates = data['Day'].values  # Defines our dates variable which is equal to being within 'data' and under the name 'day'

    # Initialize OU parameters
    theta, mu, sigma = initial_theta, initial_mu, initial_sigma #set our variables to starting at the first values
    X_t = prices[0]  # The starting value of the OU process is set to the first price in the dataset, i.e price number 0

    # Simulate real-time processing, does so by processing each variable once at a time. does it from to to the length (amount) of prices
    for t in range(1, len(prices)):
        X_t_next = prices[t]
        
        # Update parameters (example: exponential smoothing for simplicity)
        # Updates parameters by blending the previous value (weighted by 0.9) with the new information (weighted by 0.1). 
        # Can adjust weightings depending on strength of new data, maybe define an algorithm that defines the strength?
        theta = 0.9 * theta + 0.1 * (mu - X_t) / dt
        mu = 0.9 * mu + 0.1 * X_t
        sigma = 0.9 * sigma + 0.1 * abs(X_t_next - X_t) / np.sqrt(dt)

        # Predict the next state
        prediction = X_t + theta * (mu - X_t) * dt
        # O.U Algorithm prediction formula: X_{t+1} this to the left is the variable we are guessing = X_t (the past one) + theta (speed of mean reversion) times (mu (the long term mean) - X_t) * dt (the time interval)]
        # predicts where the price should move based on the current state, mean reversion speed sigma, and long term mean 𝜇
        
        # Output results
        print(f"Date: {dates[t]}, Price: {X_t_next:.2f}, Predicted: {prediction:.2f}, "
              f"Theta: {theta:.3f}, Mu: {mu:.3f}, Sigma: {sigma:.3f}")
        
        # Above: Outputs the current date, observed price, predicted price, and updated parameters.

        # Update current state. Updates Xt to the new observed price for the next iteration.
        X_t = X_t_next

        # Pause to simulate real-time (optional)
        # time.sleep(0.1)  # Adjust to control speed of simulation. Introduces a short delay (0.1 seconds) to simulate real-time processing.
        # In practice, this would match the frequency of live data arrival (e.g., 1 second, 1 minute).

# Example Usage
# Ensure you have a CSV file with columns 'Day' and 'Spread'
csv_file_path = 'HO_CL_PRICESpread.csv'  # Replace with your file path
dt = 1  # Time step in days (adjust based on your data granularity)

process_data_realtime(csv_file_path, dt) #calls the function to make it work, now that we've defined it.

# Code to save to CSV file