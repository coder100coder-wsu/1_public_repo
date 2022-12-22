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
    # set of predictors
    X = df_1[['city-mpg', 'highway-mpg']]
    # response or target variable
    y = df_1['price']
    # Split the dataset into train and test
    from sklearn.model_selection import train_test_split
    input_test_size = 0.3
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=input_test_size,
                                                        random_state=2022)
    ###################################################################################
    # setup linear regression
    model_lr_0 = LinearRegression(fit_intercept=True, copy_X=True, n_jobs=-1, positive=False)
    # fit the model
    model_lr_0 = model_lr_0.fit(X=X_train, y=y_train)
    # train, get results of model fitting, coefficient of determination, r_squared
    r_sq_train = model_lr_0.score(X_train, y_train)
    # print(f"train, coefficient of determination, r_squared: {r_sq_train}")
    model_lr_0_intercept_train = model_lr_0.intercept_
    # print(f"train, intercept: {model_lr_0.intercept_}")
    model_lr_0_slope_train = model_lr_0.coef_
    # print(f"train, slope, coefficients: {model_lr_0.coef_}")
    #########################################################################
    # predict using model
    y_pred_test = model_lr_0.predict(X_test)
    # print(f"predicted response for X[0:5]:\n{y_pred_test[0:5]}")
    y_pred_df = pd.DataFrame(pd.Series(y_pred_test), columns=['y_pred_test'])
    # test, get results, coefficient of determination, r_squared
    r_sq_test = model_lr_0.score(X_test, y_test)
    # print(f"test, coefficient of determination, r_squared: {r_sq_test}")
    #########################################################################
    data = {'train_split':f"{(1-input_test_size)*100}%",
            'test_split':f"{(input_test_size)*100}%",
            'r_sq_train':r_sq_train,
            'r_sq_test': r_sq_test,
            'model_lr_0_intercept_train':model_lr_0_intercept_train,
            'model_lr_0_slope_train': model_lr_0_slope_train,
            }
    df_sample = pd.DataFrame(data)
    print('df_sample.iloc[0]=\n', df_sample.iloc[0])
    save_output_predictions(input_df=df_sample, counter=2)
    return 1




    # # create NEW_data
    # # perturbation_in_X = np.random.choice(a=np.arange(10,100,1), size=len(X_test), replace=True, p=None)
    # # perturbation_in_X = np.array(perturbation_in_X)
    # # print(type(perturbation_in_X),"....",perturbation_in_X.shape)
    # X_NEW = X.multiply(perturbation_in_X, axis=0)
    # # print(X == X_NEW)
    # #########################################################################
    # # predict on NEW_data
    # y_pred_new = model_lr_0.predict(X_NEW)
    # # print(f"predicted response for X_NEW[0:5]:\n{y_pred_new[0:5]}")
    # y_pred_new_df = pd.DataFrame(pd.Series(y_pred_new), columns=['y_pred_test'])
    # #########################################################################
    # # save predictors and predictions as pandas df to csv
    # df_inputs = pd.concat([X, X_NEW], axis=0, ignore_index=True)
    # # print("df_inputs=\n", df_inputs.head(2))
    # df_outputs = pd.concat([y_pred_df, y_pred_new_df], axis=0, ignore_index=True)
    # # print("df_outputs=\n", df_outputs.head(2))
    # df_inputs_outputs = df_inputs.copy()
    # df_inputs_outputs['y_pred_test'] = df_outputs[['y_pred_test']]
    # # print("df_inputs_outputs=\n", df_inputs_outputs.head(2))
