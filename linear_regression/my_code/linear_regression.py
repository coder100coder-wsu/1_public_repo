import numpy as np
import pandas as pd
import statsmodels as stmd
from sklearn.linear_model import LinearRegression
import csv
from get_file_path_for_data import  get_file_path_for_data
from save_output import save_output_predictions


def run_linear_reg(bool_var=False,
                   column_titles='names.txt',
                   csv_data_file_name='autos.csv',
                   data_in_folder_name='ref_data'):
    #########################################################################
    col_header_names = get_file_path_for_data(folder_name='ref_data', file_name=column_titles,
                                            bool_var=True)
    data_file_path = get_file_path_for_data(folder_name='ref_data', file_name=csv_data_file_name,
                                            bool_var=True)
    #########################################################################
    # read list of column titles
    list_col_headers = []
    # opening the CSV file
    with open(col_header_names, mode ='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            for indv_line in lines:
                list_col_headers.append(indv_line.strip().lstrip().rstrip())
    #########################################################################
    # read data
    df = pd.read_csv(filepath_or_buffer=data_file_path,
                     sep=',',
                     header=None,
                     skip_blank_lines=True,
                     index_col=0,
                     skiprows=1)
    # drop first col from df
    df.reset_index(drop=True, inplace=True)
    # drop first col from list, row_id
    df.columns=list_col_headers[1:]
    # replace weird values
    df.replace(to_replace='?', value=np.nan, inplace=True)
    # drop na values, if any column has na, then drop entire row
    df.dropna(how='any', inplace=True)
    #########################################################################
    # subset columns. COPY to avoid the pandas warning of seeting value on view/slice of df.
    df_1 = df[['city-mpg', 'highway-mpg', 'price']].copy()
    # recast column data_type
    df_1['price'] = df_1['price'].astype('int64')
    # print("\n", df_1.info())
    #########################################################################
    # setup linear regression
    model_lr_0 = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
    # set of predictors
    X = df_1[['city-mpg', 'highway-mpg']]
    # response or target variable
    y = df_1['price']
    # fit the model
    model_lr_0 = model_lr_0.fit(X=X, y=y)
    # get results of model fitting
    r_sq = model_lr_0.score(X,y)
    # print(f"coefficient of determination, r_squared: {r_sq}")
    model_lr_0_intercept = model_lr_0.intercept_
    # print(f"intercept: {model_lr_0.intercept_}")
    model_lr_0_slope = model_lr_0.coef_
    # print(f"slope, coefficients: {model_lr_0.coef_}")
    #########################################################################
    # predict using model
    y_pred = model_lr_0.predict(X)
    # print(f"predicted response for X[0:5]:\n{y_pred[0:5]}")
    y_pred_df = pd.DataFrame(pd.Series(y_pred), columns=['y_pred'])
    #########################################################################
    # create NEW_data
    perturbation_in_X = np.random.choice(a=np.arange(-10,10,1), size=len(X), replace=True, p=None)
    perturbation_in_X = np.array(perturbation_in_X)
    # print(type(perturbation_in_X),"....",perturbation_in_X.shape)
    X_NEW = X.multiply(perturbation_in_X, axis=0)
    # print(X == X_NEW)
    #########################################################################
    # predict on NEW_data
    y_pred_new = model_lr_0.predict(X_NEW)
    # print(f"predicted response for X_NEW[0:5]:\n{y_pred_new[0:5]}")
    y_pred_new_df = pd.DataFrame(pd.Series(y_pred_new), columns=['y_pred'])
    #########################################################################
    # save predictors and predictions as pandas df to csv
    df_inputs = pd.concat([X, X_NEW], axis=0, ignore_index=True)
    # print("df_inputs=\n", df_inputs.head(2))
    df_outputs = pd.concat([y_pred_df, y_pred_new_df], axis=0, ignore_index=True)
    # print("df_outputs=\n", df_outputs.head(2))
    df_inputs_outputs = df_inputs.copy()
    df_inputs_outputs['y_pred'] = df_outputs[['y_pred']]
    # print("df_inputs_outputs=\n", df_inputs_outputs.head(2))
    save_output_predictions(input_df=df_inputs_outputs, counter=2)
    return 1
