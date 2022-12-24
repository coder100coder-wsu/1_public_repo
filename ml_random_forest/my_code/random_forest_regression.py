import numpy as np
import pandas as pd
import statsmodels as stmd
import csv
from get_file_path_for_data import  get_file_path_for_data
from save_output import save_output_predictions
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import tree
from sklearn.metrics import mean_absolute_error, mean_squared_error

random_seed_value = 42

def run_random_forest_regression(
        bool_var=False,
        clean_csv_data_file_name='autos.csv',
        data_in_folder_name='ref_data'):

    data_file_path = get_file_path_for_data(bool_var=True, folder_name=data_in_folder_name,
                                            sub_folder_name='random_forest_regression',
                                            file_name=clean_csv_data_file_name)
    # print("data_file_path=\n", data_file_path)
    # read results_data. use as-is.
    # this is clean results_data, so expected that headers, missing, nan etc. already handled
    df = pd.read_csv(filepath_or_buffer=data_file_path)
    # print(df.head(3))
    # pick numerical values only since regression problem
    # predictors= numerical type; target var= price, also numerical
    # check results_data types, change if need be
    # print(df.info())
    # print(df.columns)
    # keep only a subset of all available columns that are also numericla datatype
    cols_to_keep = [
       ' length', ' width', ' height', ' curb-weight', ' engine-size',
       ' bore', ' stroke', ' compression-ratio', ' horsepower', ' peak-rpm', ' city-mpg',
        ' highway-mpg', ' price']
    df =df[cols_to_keep]
    # print(df.info())
    # print(df.columns)
    # declare target var
    y = df[' price']
    # declare predictors, drop target var from predictors
    X = df.drop([' price'], axis=1)
    # split into train-test datasets
    # test size = 20% = 0.2
    input_test_size = 0.3
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=input_test_size,
                                                        random_state=random_seed_value)
    # instantiate random forest regressor
    rfr = RandomForestRegressor(n_estimators=100,  # 100 trees
                                #max_depth=3,  # 4 levels
                                random_state=random_seed_value)
    # fit the model
    rfr.fit(X_train, y_train)
    # predict values
    y_pred = rfr.predict(X_test)
    # evaluate model performance
    rfr_mae_not_cv = mean_absolute_error(y_test, y_pred)
    rfr_mse_not_cv = mean_squared_error(y_test, y_pred)
    rfr_rmse_not_cv = np.sqrt(mean_squared_error(y_test, y_pred))
    # print('Mean Absolute Error:', rfr_mae_not_cv)
    # print('Mean Squared Error:', rfr_mse_not_cv)
    # print('Root Mean Squared Error:', rfr_rmse_not_cv)
    ##########################################################################################
    # use cross validation with random forest regression, cv
    rfr_cv_scores = cross_val_score(rfr, X, y, cv=10,
                                    scoring="neg_mean_squared_error")
    forest_rmse_scores = np.sqrt(-rfr_cv_scores)
    rfr_rmse_with_cv_mean = forest_rmse_scores.mean()
    rfr_rmse_with_cv_std_dev = forest_rmse_scores.std()
    ##########################################################################################
    # compile results into dict
    results_data = {'train_split': f"{(1 - input_test_size) * 100}%",
                    'test_split': f"{(input_test_size) * 100}%",
                    'rfr_mae_not_cv': round(rfr_mae_not_cv,4),
                    'rfr_mse_not_cv': round(rfr_mse_not_cv,4),
                    'rfr_rmse_not_cv': round(rfr_rmse_not_cv,4),
                    'rfr_rmse_with_cv_mean': round(rfr_rmse_with_cv_mean,4),
                    'rfr_rmse_with_cv_std_dev': round(rfr_rmse_with_cv_std_dev, 4),
                    }
    # make a df from dict
    df_results = pd.DataFrame(results_data, index=[0])
    # print('df_results.iloc[0]=\n', df_results.iloc[0])
    # write df to csv
    save_output_predictions(input_df=df_results,
                            output_dir_name='output_predictions_',
                            output_sub_dir_name='random_forest_regression',
                            counter=1,
                            input_index_label='row_index',
                            file_prefix='results_')
    return 1


# run_random_forest_regression(bool_var=False, clean_csv_data_file_name='clean_1.csv',
#                              data_in_folder_name='clean_etl_data_')