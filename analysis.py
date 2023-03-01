import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gender_guesser.detector import Detector

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/avramenriquez/Documents/GitHub/Restaurant-Data-Analysis/pointbrugge.csv')

# Add a new column to the DataFrame to store the guessed gender
df['Gender'] = ''
# Create a new instance of the gender detector
d = Detector()
for index, row in df.iterrows():
    # Extract the author's first name
    first_name = row['Author'].split()[0]
    # Use the gender_guesser package to guess the gender based on the first name
    gender = d.get_gender(first_name)
    # Map the gender_guesser output to a simpler format (i.e. 'male' or 'female')
    if gender == 'male' or gender == 'mostly_male':
        df.at[index, 'Gender'] = 'male'
    elif gender == 'female' or gender == 'mostly_female':
        df.at[index, 'Gender'] = 'female'
    else:
        df.at[index, 'Gender'] = 'unknown'

# Change Date column to datetime format
df["Date"] = pd.to_datetime(df["Date"])
# Create a new column with the season
df["Season"] = np.where(df["Date"].dt.month.isin([12, 1, 2]), "Winter",
                np.where(df["Date"].dt.month.isin([3, 4, 5]), "Spring",
                np.where(df["Date"].dt.month.isin([6, 7, 8]), "Summer",
                np.where(df["Date"].dt.month.isin([9, 10, 11]), "Fall", ""))))
# Remove rows with 'Owner Response' value in the 'Author' column
df = df[df['Author'] != 'Owner Response']

# Save the new DataFrame to a new CSV file
df.to_csv('/Users/avramenriquez/Documents/GitHub/Restaurant-Data-Analysis/reviews_with_gender_season_no_owner_response.csv', index=False)

import matplotlib.pyplot as plt

def mean_by_season():
  mean_rating_by_season = df.groupby("Season")["Rating"].mean()
  # Create a bar plot of the mean rating by season
  ax = mean_rating_by_season.plot(kind="bar", color="C0")

  # Set the plot title and axis labels
  ax.set_title("Mean Rating by Season")
  ax.set_xlabel("Season")
  ax.set_ylabel("Mean Rating")

  # Set the y-axis limits to make the differences more obvious
  ax.set_ylim([4.5, 5.0])

  # Add text labels to the bars
  for i, mean_rating in enumerate(mean_rating_by_season):
      ax.annotate(str(round(mean_rating, 2)), xy=(i, mean_rating+0.01), ha='center')

  # Display the plot
  plt.show()

def mean_by_gender():
  mean_rating_by_gender = df.groupby("Gender")["Rating"].mean()
  # Create a bar plot of the mean rating by season
  ax = mean_rating_by_gender.plot(kind="bar", color="C0")

  # Set the plot title and axis labels
  ax.set_title("Mean Rating by Gender")
  ax.set_xlabel("Gender")
  ax.set_ylabel("Mean Rating")

  # Set the y-axis limits to make the differences more obvious
  ax.set_ylim([1.0, 5.0])

  # Add text labels to the bars
  for i, mean_rating in enumerate(mean_rating_by_gender):
      ax.annotate(str(round(mean_rating, 2)), xy=(i, mean_rating+0.01), ha='center')

  # Display the plot
  plt.show()

mean_by_season()
mean_by_gender()