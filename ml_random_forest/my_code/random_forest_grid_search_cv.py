import numpy as np
import pandas as pd
import statsmodels as stmd
import csv
import joblib
from get_file_path_for_data import  get_file_path_for_data
from save_output import save_output_predictions
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
# from sklearn.model_selection import StratifiedShuffleSplit
from sklearn import tree
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
# from sklearn.impute import SimpleImputer
from scipy import stats



input_test_size = 0.3 # 30% test set
random_seed_value = 42

def run_grid_search_cv_random_forest_regression(
        bool_var=False,
        clean_csv_data_file_name='autos.csv',
        data_in_folder_name='ref_data'):

    data_file_path = get_file_path_for_data(bool_var=True,
                                            folder_name=data_in_folder_name,
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
    ##########################################################################################
    # declare target var
    y = df[' price']
    # declare predictors, drop target var from predictors
    X = df.drop([' price'], axis=1)
    ##########################################################################################
    # Stratified Sampling, proportional random sampling instead of purely random sampling
    # train_test_split is used for purely random sampling as in NOT-STRATIFIED
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size = input_test_size,
                                                        random_state = random_seed_value)
    ##########################################################################################
    # form pipeline for numerical columns only
    num_pipeline = Pipeline([
        # ('imputer', SimpleImputer(strategy="median")),
        ('std_scaler', StandardScaler()),
    ])
    num_attribs = list(X_train) # numerical cols
    ##########################################################################################
    # apply different pipelines
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, num_attribs),
    ])
    ##########################################################################################
    # apply pipeline to data.
    # we can use X directly, because we already know X is numerical only.
    # call fit_transform directly. OR OR we can "fit->then->transform" as typical.
    X_train_after_pipeline = full_pipeline.fit_transform(X_train)
    # print(X_train_after_pipeline)
    ##########################################################################################
    n_estimators_1 = [100, 158]
    n_estimators_2 = [59, 159]
    max_features_1 = [4, 8]
    max_features_2 = [13]
    # n_estimators_1 = [50, 100, 158]
    # n_estimators_2 = [49, 99, 159]
    # max_features_1 = [2, 4, 6, 8, 10, 12]
    # max_features_2 = [3, 5, 7, 9, 11, 13]
    # construct parameter grid
    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {'n_estimators': n_estimators_1, 'max_features': max_features_1},
        # then try 6 (2×3) combinations with bootstrap set as False
        {'bootstrap': [False], 'n_estimators': n_estimators_2, 'max_features': max_features_2},
    ]
    ##########################################################################################
    # instantiate RandomForestRegressor
    forest_reg = RandomForestRegressor(random_state=random_seed_value)
    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(forest_reg,
                               param_grid,
                               cv=5,
                               scoring='neg_mean_squared_error',
                               return_train_score=True)
    # fit the model
    grid_search.fit(X_train_after_pipeline, y_train)
    # print results
    # print("\n grid_search.best_params_ \n")
    # print(grid_search.best_params_)

    # print("\n grid_search.best_estimator_ \n")
    # print(grid_search.best_estimator_)

    # print("\n all grid search cv results: \n")
    cvres = grid_search.cv_results_
    # print("type(cvres)=\n", type(cvres))
    # print("cvres=\n", cvres)
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print("rmse= ", np.sqrt(-mean_score), "; params= ", params)
    df_grid_cv_results = pd.DataFrame(grid_search.cv_results_)
    # df_grid_cv_results.head(2)
    save_output_predictions(input_df=df_grid_cv_results,
                            output_dir_name='output_predictions_',
                            output_sub_dir_name='random_forest_regression',
                            counter=1,
                            input_index_label='row_index',
                            file_prefix='models_grid_srch_cv_')
    # NOTE: grid_search gives back several models of type "random forest regressor"
    # select model with best hyperparameters as determined by grid search
    final_rfr_best_grd_cv = grid_search.best_estimator_
    # ensure pre-processing on test set
    # don't need to fit again, already done above
    X_test_after_pipeline = full_pipeline.transform(X_test)
    # use best model to predict target var on test set
    y_hat_test = final_rfr_best_grd_cv.predict(X_test_after_pipeline)
    # get mse
    final_mse = mean_squared_error(y_test, y_hat_test)
    # get rmse
    final_rmse = np.sqrt(final_mse)
    # get mae
    final_mae = mean_absolute_error(y_test, y_hat_test)
    # compute a 95% confidence interval for the test RMSE
    confidence = 0.95
    squared_errors = (y_hat_test - y_test) ** 2
    min_95_cnfd_lvl, max_95_cnfd_lvl= np.sqrt(stats.t.interval(confidence,
                             len(squared_errors) - 1,
                             loc=squared_errors.mean(),
                             scale=stats.sem(squared_errors)))
    # create results row
    results_data = {'train_split': f"{(1 - input_test_size) * 100}%",
                    'test_split': f"{(input_test_size) * 100}%",
                    'final_rfr_best_grd_cv_mae': round(final_mae, 4),
                    'final_rfr_best_grd_cv_mse': round(final_mse, 4),
                    'final_rfr_best_grd_cv_rmse': round(final_rmse, 4),
                    'min_95_cnfd_lvl': round(min_95_cnfd_lvl, 4),
                    'max_95_cnfd_lvl': round(max_95_cnfd_lvl, 4),
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
                            file_prefix='results_grid_srch_cv_')

    # save the model in same dir for convinience
    joblib.dump(final_rfr_best_grd_cv, "final_rfr_best_grd_cv.pkl")


    return 1


# run this to train the model
# change paramters in the body of code as necessary
# run_grid_search_cv_random_forest_regression(
#         bool_var=True,
#         clean_csv_data_file_name='clean_1.csv',
#         data_in_folder_name='clean_etl_data_')