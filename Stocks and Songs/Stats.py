import pandas as pd
from patsy import dmatrices
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

#Followed an Article written by Sachin Date on towardsdatascience.com in order to
#get syntax on how to use Poisson and NB models

#We decided to not funcitonize this code so that both models could be trained and compared on the same
#training and test data
def main():

    with open("FullData.csv", "r") as file:
        df = pd.read_csv(file)

    #Get traning and test data for Poisson model
    mask = np.random.rand(len(df)) <0.8
    df_train = df[mask]
    df_test = df[~mask]
    print('Training data length= '+str(len(df_train)))
    print('Testing data length= '+str(len(df_test)))

    #Define the regression model for patsy
    #
    model = """num_mentions ~ industry + Delta_Price + log_volume + consecutive_weeks"""

    #Set up test and training matricies
    Y_train , X_train = dmatrices(model, df_train, return_type='dataframe')
    Y_test , X_test = dmatrices(model, df_test, return_type='dataframe')

    #Use GLM to train Poisson and NB2 regression model on training data
    poisson = sm.GLM(Y_train, X_train, family=sm.families.Poisson()).fit()
    nb2 = sm.GLM(Y_train, X_train,family=sm.families.NegativeBinomial(alpha=.05)).fit()
    
    #Print summary stats 
    print(poisson.summary())
    print(nb2.summary())

    #Test model accuracy with predictions
    poisson_predict = poisson.get_prediction(X_test)
    pred_vals = poisson_predict.summary_frame() #Returns pandas df
    print(pred_vals)

    #Test NB accuracy with predictions
    nb2_pred = nb2.get_prediction(X_test)
    nb2_pred_vals = nb2_pred.summary_frame()
    print(nb2_pred_vals)

    #Get predicted and actual counts for graphs
    pred_count = pred_vals['mean']
    actual_count = Y_test['num_mentions']

    #Plot predicted vs actual for test data Poisson
    figure = plt.figure()
    figure.suptitle('Predicted vs. Actual # of Mentions Poisson')
    predict, = plt.plot(X_test.index, pred_count, 'go-', label='Predicted counts')
    actual, = plt.plot(X_test.index, actual_count, 'ro-', label='Actual counts')
    plt.legend(handles=[predict, actual])
    plt.show()

    #Change predicted counts for NB graph
    pred_count = nb2_pred_vals['mean']

    ##Plot predicted vs actual for test data NB
    plt.clf()
    fig = plt.figure()
    fig.suptitle('Predicted vs. Actual # of Mentions Negative Binomial')
    predicted, = plt.plot(X_test.index, pred_count, 'go-', label='Predicted counts')
    actual, = plt.plot(X_test.index, actual_count, 'ro-', label='Actual counts')
    plt.legend(handles=[predicted, actual])
    plt.show()


if __name__ == "__main__":
    main()