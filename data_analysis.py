"""

Author: Hayden Mann

Description: This program acts as a supporter to rad_plots_adjustedSW.py. It is not
run on its own. Its purpose is to help with data infrastructure.

"""


import unisacsi.Meteo as met
    # Available online. Not necessary (only used to open files, but can be hardcoded) 
import os       


def data_into_df(filename):
    """
    Converts a given filename into a dataframe
    """
    path_data = 'DataDataData/MaggieMay/converted'
    os.path.exists(path_data)  # check if the path_data exists
    df_rad = met.read_Campbell_TOA5(os.path.join(path_data, filename))
    return df_rad



def download_dfs(station, filenames_array):
    """
    Used to save dfs to .csv, if needed
    """
    for file in filenames_array:
        data_path = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/MaggieMay/converted'
        df_rad = met.read_Campbell_TOA5(os.path.join(data_path, file))
        to_store_path = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/Dataframes/MaggieMay_DF'
        file = os.path.splitext(file)[0]
        df_rad.to_csv(os.path.join(to_store_path, file + '.csv'), index=False)
    return None



def stack_dfs_2(station):
    """
    Used to stack data into a single dataframe
    """
    if station is True:
        path_data = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/MaggieMay/converted/1min'
        os.path.exists(path_data)  # check if the path_data exists
        df_rad = met.read_Campbell_TOA5(os.path.join(path_data, "TOA5*"))
    else:
        path_data = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/albedo_radiation'
        os.path.exists(path_data)  # check if the path_data exists
        df_rad = met.read_Campbell_TOA5(os.path.join(path_data, "CR1000*"))

    to_store_path = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/Dataframes'
    if station is True:
        df_rad.to_csv(os.path.join(to_store_path, 'New_MM_Combined_LatestUpdate' + '.csv'))
        return df_rad
    else:
        df_rad.to_csv(os.path.join(to_store_path, 'New_L_Combined_LatestUpdate' + '.csv'))
        return df_rad


