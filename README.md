# SE-Europe-Data_Challenge_Template
Template repository to work with for the NUWE - Schneider Electric European Data Science Challenge in November 2023.

1. Set up environment (Discord, VSC, etc)
2. Cloned the skeleton repository

**[DATA PROCESSING]**

3. Prepare the l_your_train.csv with historical data

    3.1. Get the data from the API

    3.2. Explore the dataset

    3.3. Data processing: reformat the dataset to our needs
    
    - Give AreaID column country name
    - Replace nulls with the mean between the preceding and following values. 
    - Identify what energy types each column represent, and discard the ones that are not green energy source. 
    - Normalise all energy values are in the same units (MAW)
    - Calculate surplus column
    - Adapt the structure of the dataset to the following schema: one column for each energy type and load (consumption) for each country + an additional column for the label: the ID of the country with the bigger surplus of green energy for the next hour. The final dataset should have 2210 rows. 
    - Split the data into training (save it in train.csv) and test (save it in test.csv). For the latter we delete the label column. The test set should have 442 rows. 

**[MODEL CREATION]**

4. Choose the optimal model to train.
5. Build the model.
6. Train the model with the train.csv
7. Make predictions with the test.csv and save it in predictions.json following the same format we can find in example_predictions.json.
8. Evaluate the model performance on F1-score macro.

**[SUBMISSION]**

9. Save our repository in Github and make it public.
10. Include a document with explanations of the process.
11. Submit the link to the organization through Nuwe portal. (Team lead)

**[EVALUATION]**

12. Save our repository in Github and make it public.
