#Stock price prediction

To build everything run this in the Terminal:
'''
make docker-all
'''

Then try the different endpoints as per the yaml file on the url:
'''
localhost:8000
'''

##Endpoints

###/read_file/<filename>
Add the name of the file in this endpoint to load the file. All the following end points will be according to this file that is loaded.
If the file name is AAPL.csv, use the endpoint /read_file/AAPL

###/plot
It will plot the data you just uploaded

###/split
Split the data in train and test

###/train
Train the model
###Training the model takes really long time, but a model is saved, so you can skip the /train endpoint

###/predict
Make the predictions on the test set

###/plot_pred
Plot the predictions to get a visual of how well your model did
