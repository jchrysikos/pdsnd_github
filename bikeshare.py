import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # Request user input for city (chicago, new york city, washington). Insert while loop to handle invalid inputs
    city = input('Please choose a city name (chicago, new york city, washington)').lower()
    while city not in CITY_DATA.keys():
        print('Please enter a valid city name')
        city = input('Please choose a city name (chicago, new york city, washington)').lower()


    # Request user input for month (all, january, february, ... , june). Insert while loop to handle invalid inputs
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all months']
    while True:
        month = input('Please choose month (january, february, march, april, may, june, all months) ').lower()
        if month in months :
         break
        else:
            print('Please enter a valid month name')


    # Request user input for day of week (all, monday, tuesday, ... sunday). Inswert while loop to handle invalid inputs
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all days']
    while True:
        day = input('Please choose a day of the week: (sunday, monday, tuesday, wednesday, thursday, friday, saturday, all days) ').lower()
        if day in days :
            break
        else:
            print('Please enter a valid day of the week')

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

   #convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month, day of week and start hour from start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all months':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of the week
    if day != 'all days':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month by using mode function against months, which will show the month that appears the most often for the specified city.
    print('The most common month is : {}'.format(df['month'].mode()[0]))

    # Display the most common day of week by using mode function against week days, which will show the day of the week that appears the most often for the specified city.
    print('The most common day is : {}'.format(df['day_of_week'].mode()[0]))

    # Display the most common start hour by using mode function against the start hour, which will show the start hour that appears the most often for the specified city.
    print('The most common start hour is : {}'.format(df['start hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station by using mode function against the start station, which will show the start station that appears the most often for the specified city.
    print('The most common start station is : {}'.format(df['Start Station'].mode()[0]))

    # Display most commonly used end station by using mode function against the end station, which will show the end station that appears the most often for the specified city.
    print('The most common end station is : {}'.format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip by using mode function against the calculated route, which will show the route that appears the most often for the specified city. The calculated route finds all the combinations of start and       end stations.
    df['route']=df['Start Station']+","+df['End Station']
    print('The most common route is : {}'.format(df['route'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time : ', total_time/(3600*24), ' days')

    # Display mean travel time
    avg_time = df['Trip Duration'].mean()
    print('Average travel time : ', avg_time/(3600*24), ' days')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types. Count unique users then convert values to dataframe.
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender. Count unique values then convert values to dataframe.
    if city != 'washington' :
        print(df['Gender'].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth
        print('The most common year of birth is : ',int(df['Birth Year'].mode()[0])) # return integer for birth year then use mode to calculate the year that appears the most for the specified city
        print('The most recent year of birth is : ',int(df['Birth Year'].max())) # return integer for birth year and find the highest value to indicate the most recent year
        print('The earliest year of birth is : ',int(df['Birth Year'].min())) # return integer for birth year and find lowest value to indicate the earlierst year
    else:
        print('there is no data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    #to ask the user if he/she would like to see the raw data of the selected city as chunks of 5 rows based on user input
    print('\nRaw data is available to check...\n')

    i=0
    user_input=input('would you like to display 5 rows of raw data? Please type yes or no ').lower()
    if user_input not in ['yes','no']:
        print('Invalid input. Please type yes or no') # handles invalid input
        user_input=input('would you like to display 5 rows of raw data? Please type yes or no ').lower()
    elif user_input != 'yes':
        print('Thank you')

    else:
        while i+5 < df.shape[0]:
            print(df.iloc[i:i+5]) #subsets dataframe to display next 5 rows
            i += 5
            user_input = input('would you like to display 5 more rows of raw data? Please type yes or no ').lower()
            if user_input != 'yes':
                print('Thank you')
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thanks for exploring!')
            break


if __name__ == "__main__":
	main()
