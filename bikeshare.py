import datetime as dt
import numpy as np
import pandas as pd
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nWould you like to see data for Chicago, New York City, or Washington?\n").lower()
    while city not in CITY_DATA:
        city = input("Invalid Input. Please choose between \"Chicago\", \"New York City\", or \"Washington\".\n").lower()

    #convert "new york city" to "new_york_city" for easier use
    if city == "new york city":
        city = "new_york_city"

    # get user input for filter (month, day, both, not at all)
    filter = input("\nWould you like to filter the data by month, day, both, or not at all?\n").lower()
    while filter not in ["month", "day", "both", "not at all"]:
        filter = input("Invalid input. Please choose between \"month\", \"day\", \"both\", or \"not at all\".\n").lower()

    # get user input for month (all, january, february, ... , june)
    if filter in ["month", "both"]:
        month = input("\nWhich month - January, February, March, April, May or June?\n").lower()
        while month not in ["january", "february", "march", "april", "may", "june"]:
            month = input("Invalid input. Please choose between \"January\", \"February\", \"March\", \"April\", \"May\", or \"June\".\n").lower()
    else:
        month = "none"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter in ["day", "both"]:
        day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
        while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            day = input("Invalid input. Please choose between \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\", or \"Sunday\".\n").lower()
    else:
        day = "none"

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read in city specific raw data
    raw_data = pd.read_csv("{}.csv".format(city))

    # convert "Start Time" and "End Time" into timestamp-format
    raw_data["Start Time"], raw_data["End Time"] = pd.to_datetime(raw_data["Start Time"]), pd.to_datetime(raw_data["End Time"])

    # add columns "Month" and "Day" to raw data set (for filtering)
    raw_data['Month'] = raw_data['Start Time'].dt.month_name()
    raw_data["Day"] =  raw_data['Start Time'].dt.day_name()

    # add column "Hour" to raw data set (for most common start hour)
    raw_data["Hour"] = raw_data["Start Time"].dt.hour

    # transfer raw_data to df
    df = raw_data

    # filter our dataset by given month, day both or none
    if month == "none" and day == "none":
        return df
    elif month != "none" and day == "none":
        return df[(df["Month"] == month.title())]
    elif month == "none" and day != "none":
        return df[(df["Day"] == day.title())]
    elif month != "none" and day != "none":
        return df[(df["Month"] == month.title()) & (df["Day"] == day.title())]
    else:
        print("IF ELSE - ERROR")
        exit()



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: ", df['Month'].value_counts().idxmax())

    # display the most common day of week
    print("Most common day: ", df['Day'].value_counts().idxmax())

    # display the most common start hour
    print("Most common start hour: {} o'clock".format(df['Hour'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station: ", df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("Most common end station: ", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    station_groupby = df.groupby(['Start Station', 'End Station'])
    most_frequent_combination = station_groupby.size().nlargest(1)
    print("\nMost frequent combination of start station and end station: ")
    print(most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    travel_time_total = df['Trip Duration'].sum() / (60*60*24)
    print("Total travel time: {} days".format(round(travel_time_total, 2)))

    # display mean travel time
    travel_time_mean = df['Trip Duration'].mean() / (60)
    print("Mean travel time: {} minutes".format(round(travel_time_mean, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df["User Type"].value_counts()
    print("Count of user types: \n", user_type_counts)

    # Display counts of gender
    if city in ["chicago", "new_york_city"]:
        user_gender_count = df['Gender'].value_counts()
        print("\nCount of user gender:\n", user_gender_count)

        # Display earliest, most recent, and most common year of birth
        if city in ["chicago", "new_york_city"]:
            birth_earliest = (df['Birth Year'].min())
            print("\nEarliest year of birth: ", int(birth_earliest))
            birth_recent = (df['Birth Year'].max())
            print("Most recent year of birth: ", int(birth_recent))
            birth_common = (df['Birth Year'].value_counts().idxmax())
            print("Most common year of birth: ", int(birth_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def raw_data(df):
    """prints 5 rows of the data at a time,
    then asks the user if they wold like to see 5 more rows
    until the user chooses "no"."""

    # display first 5 rows of data set
    print_raw_data = input("\nWould you like to see some raw data? Enter yes or no.\n").lower()
    while print_raw_data not in ["yes", "no"]:
        print_raw_data = input("Invalid input. Please choose between \"yes\" or \"no\".\n").lower()
    if print_raw_data == "yes":
        df_raw = df.drop(["Month", "Day", "Hour"], axis = 1)
        print(df_raw.head())

    # display 5 more rows of the data set as long as input = "yes"
    x = 0
    while print_raw_data == "yes":
        print_raw_data = input("\nWould you like to see some more? Enter yes or no.\n").lower()
        while print_raw_data not in ["yes", "no"]:
            print_raw_data = input("Invalid input. Please choose between \"yes\" or \"no\".\n").lower()
        if print_raw_data == "yes":
            x += 5
            print(df_raw[x:(x+5)])



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in ["yes", "no"]:
            restart = input("Invalid input. Please choose between \"yes\" or \"no\".\n").lower()
        if restart.lower() != 'yes':
            print("\nHave a nice day! :)\n")
            break



if __name__ == "__main__":
	main()
