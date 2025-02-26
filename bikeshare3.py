import time
import datetime
import calendar
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': './chicago.csv',
              'new york': './new_york_city.csv',
              'washington': './washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('-'*40)
    print('\n')
    
    # Get user input for city. Includes validation for case and correct city options.
    city_options = ["chicago", "washington", "new york"]
    while True:
        city = str(input("Which city would you like to analyze? Chicago, Washington, or New York?")).lower()
        if city in city_options:
                break
        else:
            print("Invalid input. Please choose Chicago, Washington, or New York.")

    print("You chose:", city.title())

    # Get user input for month. Includes validation for case and correct month options (with "all").
    month_options = ["january", "february", "march", "april", "may", "june", "all"]
    while True:
        month = str(input("Which month would you like to analyze? ")).lower()
        if month.lower() in month_options:
                break
        else:
            print("Invalid input. Please choose from:", month_options)

    print("You chose:", month.title())

    # Get user input for day of the week. Includes validation for case and correct day options (with "all").
    day_options = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    while True:
        day = str(input("Which day of the week would you like to analyze? ")).lower()
        if day.lower() in day_options:
                break
        else:
            print("Invalid input. Please choose from:", day_options)

    print("You chose:", day.title())

    print('-'*40)

    #Provides the user confirmation of all three choices in title format, regardless of input case.
    print('You chose city: {}, month: {}, day: {}.'.format(city.title(), month.title(), day.title()))

    print('-'*40)

    #print(city, month, day)
    
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
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    #Displays statistics on rental times
    print('\nWhen are the most common times for bike rentals?\n')
    start_time = time.time()
    
    print('Based on your choices:\n')
    
    common_month = df['month'].mode()[0]
    print('The most popular month for users to rent bikes is {}.'.format(calendar.month_name[common_month]))
    
    common_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week to rent bikes is {}.'.format(common_day))
    
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most popular time of the day is {}:00.'.format(common_hour))
   
    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)

def station_stats(df):
    #Displays statistics on the most popular stations and trip.

    print('\nWhat are the most popular stations and trips?\n')
    start_time = time.time()  
    
    print('Based on your choices:\n')
    
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(common_start_station))
    
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(common_end_station))
    
    df['combination'] = df['Start Station'] + ' - ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print('The most common combination of start station and end station trip is {}.'.format(common_combination))
    
    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)

def trip_duration_stats(df):

    print('\nHow long are users renting the bikes?\n')
    start_time = time.time()
    
    print('Based on your choices:\n')
    
    #Displays the total travel time for the selected criteria, displayed as hours and minutes
    total_travel_time = df['Trip Duration'].sum()
    ht, mt, st = map(lambda x: int(x), [total_travel_time/3600, total_travel_time%3600/60, total_travel_time%60])
    print('The total travel time for all trips is {} hour(s) and {} minute(s).'.format(ht,mt))

    #Displays the mean trip time for the selected criteria, displayed as hours and minutes
    mean_travel_time = df['Trip Duration'].mean()
    hm, mm, sm = map(lambda x: int(x), [mean_travel_time/3600, mean_travel_time%3600/60, mean_travel_time%60])
    print('The mean trip time is {} hour(s) and {} minute(s).'.format(hm,mm))
    
    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    
    print('-'*40)

def user_stats(df):
    #Displays information on users within the selected criteria, based on data availability. Age and gender data are only available for Chicago and New York.
    
    print('\nWho\'s using the bikes?\n')
    start_time = time.time()
    
    print('Based on your choices:\n')
    
    #Provides counts of all users, and how many are subscribers
    type_count = df['User Type'].value_counts()
    total_users = type_count.sum()
    subscriber_count = type_count['Subscriber']
    customer_count = type_count['Customer']
    sub_pct = round(((subscriber_count / total_users)*100),1)
    print('There were {} total users, and {} ({}%) of those users were subscribers.'.format(total_users,subscriber_count,sub_pct))   
    
    #When gender data are available, displays select statistics related to user gender
    print('\nStatistics on user gender:')
    try:
        gender_counts = df['Gender'].value_counts(dropna=True)
        male_count = gender_counts['Male']
        female_count = gender_counts['Female']
        male_pct = round(((male_count / total_users)*100),1)
        female_pct = round(((female_count / total_users)*100),1)
        print('Of the total users, {} ({}%) were male and {} ({}%) were female. The gender of remaining users is unknown.'.format(male_count,male_pct,female_count,female_pct))
    except KeyError:
        print('\nSorry. Gender statistics are not available for Washington.')
    
    #When age/birth year data are available, displays select statistics related to user age/birth year
    print('\nStatistics on user age:')
    try:
        user_age = (2017 - df['Birth Year'])
        mode_year = int(df['Birth Year'].mode())
        max_year = int(df['Birth Year'].max()) 
        min_year = int(df['Birth Year'].min())
        young_age = int(user_age.min())
        old_age = int(user_age.max())
        print('The average user age was {} years old.'.format(round(user_age.mean()),1))
        print('The most common user age was {} years old, and the most common birth year is {}.'.format(user_age.mode()[0], mode_year))
        print('The youngest user was {} years old, and was born in {}.'.format(young_age,max_year))
        print('The oldest user was {} years old, and was born in {}.'.format(old_age,min_year))
    except KeyError:
        print('\nSorry. Age and birth year statistics are not available for Washington.')
      
    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)
    
#def display_data(df):
    #Displays raw data five rows at a time based on previously selected criteria; user can choose to see more rows or exit the function
    #Validation is included to limit answers to 'yes' or 'no'
 #   data_location = 0
 #   retrieve_data = str(input("Would you like to see the first five rows of raw data for your request? Yes or No")).lower()
 #   while True:
 #       if retrieve_data == 'yes':
 #           print(df.iloc[data_location : data_location + 5])
 #           data_location += 5
 #           retrieve_data = str(input("Would you like to see the next five rows? Yes or No")).lower()
 #       if retrieve_data == 'no':
 #           break
 #       else:
 #           print("Invalid input. Please enter Yes or No.")
 #           retrieve_data = str(input("Would you like to see the next five rows? Yes or No")).lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
 #       display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nThanks for exploring with us!')
            break


if __name__ == "__main__":
	main()
