import joblib
import pandas as pd
from feed_input_to_saved_model import create_input_to_saved_model
from save_output import save_output_predictions


def predict_using_saved_model(bool_start=False,
                              saved_model_pkl_file_name='final_rfr_best_grd_cv.pkl',
                              saved_model_pkl_file_path=None,
                              input_X=None,
                              num_rows = 10):
    # create input
    input_X = create_input_to_saved_model(
        bool_var=False,
        folder_name='clean_etl_data_',
        sub_folder_name='random_forest_regression',
        file_name='clean_part_1.csv',
        num_rows = num_rows)
    # print("input_X=\n", input_X)
    # Load from file
    saved_model = joblib.load(saved_model_pkl_file_name)
    # Make predictions
    y_hat = saved_model.predict(input_X.values)
    # print("y_hat=\n", y_hat)
    # compile results into df
    # create results df
    df_results = pd.DataFrame(input_X)
    # print("df_results=\n",df_results)
    df_results['y_hat'] = y_hat
    # print("df_results=\n", df_results)
    # save predictions
    save_output_predictions(input_df=df_results,
                            output_dir_name='output_predictions_',
                            output_sub_dir_name='random_forest_regression',
                            counter=1,
                            input_index_label='row_index',
                            file_prefix='predict_by_pkl_model_')

    return 1



predict_using_saved_model(bool_start=True,
                          saved_model_pkl_file_name='final_rfr_best_grd_cv.pkl',
                          saved_model_pkl_file_path=None,
                          input_X=None,
                          num_rows = 10)