import pandas as pd
from io import StringIO

def analyze_demographic_data(data_path="adult.data.csv", custom_data=None):
    # Define column names manually since the data has no header
    columns = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
    ]
    

    df = pd.read_csv(data_path, header=None, names=columns)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Handle missing values by dropping rows with NaN values
    df_clean = df.dropna()  # Drop rows containing NaN values
    
    # Print cleaned DataFrame without NaN values
    print("\nCleaned DataFrame (No NaN values):")
    print(df_clean)

    # How many people of each race are represented in this dataset?
    race_count = df_clean['race'].value_counts()
    
    # What is the average age of men?
    men_data = df_clean[df_clean['sex'] == 'Male']
    average_age_men = round(men_data['age'].mean(), 1) if not men_data.empty else "No data available"
    
    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df_clean['education'] == 'Bachelors').mean() * 100, 1)
    
    # What percentage of people with advanced education make more than 50K?
    advanced_education = df_clean['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_data = df_clean[advanced_education & (df_clean['salary'] == '>50K')]
    higher_education_rich = round((higher_education_data.shape[0] / df_clean[advanced_education].shape[0]) * 100, 1) if df_clean[advanced_education].shape[0] > 0 else "No data available"
    
    # What percentage of people without advanced education make more than 50K?
    lower_education_data = df_clean[~advanced_education & (df_clean['salary'] == '>50K')]
    lower_education_rich = round((lower_education_data.shape[0] / df_clean[~advanced_education].shape[0]) * 100, 1) if df_clean[~advanced_education].shape[0] > 0 else "No data available"
    
    # What is the minimum number of hours a person works per week?
    min_work_hours = df_clean['hours-per-week'].min()
    
    # What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?
    min_workers = df_clean['hours-per-week'] == min_work_hours
    rich_percentage = round((df_clean[min_workers]['salary'] == '>50K').mean() * 100, 1) if df_clean[min_workers].shape[0] > 0 else "No data available"
    
    # What country has the highest percentage of people that earn >50K and what is that percentage?
    country_salary = df_clean[df_clean['salary'] == '>50K']['native-country'].value_counts() / df_clean['native-country'].value_counts()
    country_salary = country_salary.dropna()  # Remove NA values
    highest_earning_country = country_salary.idxmax() if not country_salary.empty else "No data available"
    highest_earning_country_percentage = round(country_salary.max() * 100, 1) if not country_salary.empty else "No data available"
    
    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df_clean[(df_clean['native-country'] == 'India') & (df_clean['salary'] == '>50K')]['occupation'].mode()
    top_IN_occupation = top_IN_occupation[0] if not top_IN_occupation.empty else "No data available"
    
    # Return results as a dictionary
    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

if __name__ == "__main__":
    results = analyze_demographic_data()
    for key, value in results.items():
        print(f"{key}: {value}")
