# import unisacsi
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unisacsi.Meteo as met
import os       #just used in the example script to combine the path, not needed in other scripts


# Function: Load Data
def data_into_df(filename):
    """
    Converts a given filename into a dataframe
    """
    path_data = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/MaggieMay/converted'
    os.path.exists(path_data)  # check if the path_data exists
    df_rad = met.read_Campbell_TOA5(os.path.join(path_data, filename))
    # print(df_rad.head())
    # path_data = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/Dataframes'
    # df_rad.to_csv('TEST.csv', index=False)
    return df_rad


def plot_variables(df_rad):
    """
    Simple TEST Plot
    """
    fig, ax = plt.subplots(1,1)
    # with pd.plotting.plot_params.use('x_compat', True):
    #     # df_rad.plot(y="CM3Up_Avg [W/meter²]", ax=ax, c="b")
    #     # df_rad.plot(y="CM3Dn_Avg [W/meter²]", ax=ax, c="g")
    #     df_rad.plot(y="net", ax=ax, c="g")
    ax.set_xlabel("Time")
    ax.set_ylabel("SW_up [W/m^2]")
    # ax.grid("both")
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b'))

    df_rad.plot(y="SW_up [W/m^2]", ax=ax, color="green")


    ax.set_xlabel("Time")
    ax.set_ylabel("SW_up [W/m^2]")

    plt.show()


def download_dfs(station, filenames_array):
    """
    Used to save dfs to .csv if needed
    """
    # path_data = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/MaggieMay/converted'
    # print(path_data)
    for file in filenames_array:
        data_path = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/MaggieMay/converted'
        df_rad = met.read_Campbell_TOA5(os.path.join(data_path, file))
        to_store_path = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/Dataframes/MaggieMay_DF'
        file = os.path.splitext(file)[0]
        df_rad.to_csv(os.path.join(to_store_path, file + '.csv'), index=False)
        # df_rad.to_csv(os.path.join(to_store_path, file + '.csv'), index=False)
    return None



def stack_dfs_2(station):
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
    

    




def time_series_plot_maggie_may(vars_to_plot):
    """
    Time series plot for maggie may
    """

    df_rad_to_plot = pd.read_csv('DataDataData/Dataframes/New_MM_Combined_LatestUpdate.csv')
    df_rad_to_plot["TIMESTAMP"] = pd.to_datetime(df_rad_to_plot["TIMESTAMP"])
    df_rad_to_plot = df_rad_to_plot.set_index("TIMESTAMP")  

    fig, ax = plt.subplots(1,1)
    # with pd.plotting.plot_params.use('x_compat', True):
    #     # df_rad.plot(y="CM3Up_Avg [W/meter²]", ax=ax, c="b")
    #     # df_rad.plot(y="CM3Dn_Avg [W/meter²]", ax=ax, c="g")
    #     df_rad.plot(y="net", ax=ax, c="g")
    
    # ax.grid("both")
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))

    for var in vars_to_plot:
        df_rad_to_plot.plot(y=var, ax=ax)

    # df_rad_to_plot.plot(y=var_to_plot, ax=ax, color="green")
    # df_rad_to_plot.plot(y="SW_down [W/m^2]", ax=ax, color="green")
    # df_rad_to_plot.plot(y="LW_up [W/m^2]", ax=ax, color="green")
    # df_rad_to_plot.plot(y="LW_down [W/m^2]", ax=ax, color="green")


    ax.set_xlabel("Time")
    ax.set_ylabel("[W/m^2]")

    plt.show()  


def albedo_plot_and_calc(csv):
    """
    Calculates albedo (limited to when SW_down >= 20 W/m^2)
    Plots time series
    """
    df_rad_to_plot = pd.read_csv(csv)
    df_rad_to_plot["TIMESTAMP"] = pd.to_datetime(df_rad_to_plot["TIMESTAMP"])
    df_rad_to_plot = df_rad_to_plot.set_index("TIMESTAMP")  

    df_rad_to_plot["SW_Down_Filter_Above_20 [W/m^2]"] = df_rad_to_plot['SW_down [W/m^2]'].where(df_rad_to_plot['SW_down [W/m^2]'] > 20)
    df_rad_to_plot["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] = df_rad_to_plot['SW_up [W/m^2]'].where(df_rad_to_plot['SW_down [W/m^2]'] > 20)

    if "_L_" in csv:
        df_rad_to_plot["ALBEDO (Layla)"] = df_rad_to_plot["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] / df_rad_to_plot["SW_Down_Filter_Above_20 [W/m^2]"]
    else: 
        df_rad_to_plot["ALBEDO (Maggie May)"] = df_rad_to_plot["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] / df_rad_to_plot["SW_Down_Filter_Above_20 [W/m^2]"]


    # print(df_rad_to_plot["ALBEDO (Snow - Maggie May)"].mean())

    fig, ax = plt.subplots(1,1)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))

    # for var in vars_to_plot:
    #     df_rad_to_plot.plot(y=var, ax=ax)

    if "_L_" in csv:
        df_rad_to_plot.plot(y="ALBEDO (Layla)", ax=ax)
    else: 
        df_rad_to_plot.plot(y="ALBEDO (Maggie May)", ax=ax)
    ax.set_xlabel("Time")
    # ax.set_ylabel("[W/m^2]")
    ax.set_ylim([0, 1])

    plt.show()  
    

def net_rad_and_plot(csv):
    df_rad_to_plot = pd.read_csv(csv)

    fig, ax = plt.subplots(1,1)
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))

    # for var in vars_to_plot:
    #     df_rad_to_plot.plot(y=var, ax=ax)

    df_rad_to_plot["NET Radiation [W/m^2]"] = df_rad_to_plot["SW_up [W/m^2]"] - df_rad_to_plot["SW_down [W/m^2]"] + df_rad_to_plot["LW_up [W/m^2]"] - df_rad_to_plot["LW_down [W/m^2]"]

    if "_L_" in csv:
        df_rad_to_plot.plot(y="NET Radiation [W/m^2]", ax=ax)
    else: 
        df_rad_to_plot.plot(y="NET Radiation [W/m^2]", ax=ax)
    ax.set_xlabel("Time")
    # ax.set_ylabel("[W/m^2]")
    # ax.set_ylim([0, 1])

    plt.show()  

    return None


def main():

    """
    Simple TEST Plot of One Variable
    """
    # filename = "TOA5_CR3000_MaggieMay_Res_data_1_min_1_2026_03_18_0001.dat"
    # df_rad = data_into_df(filename)
    # df_rad.head()
    # plot_variables(df_rad)


    """
    # Section to download .dat and convert to .csv (which we can store)
    """

    # station = '/MaggieMay/converted'
    # filenames_array = ['TOA5_CR3000_MaggieMay_Res_data_1_min_0_2026_03_17_1756.dat',
    #                     'TOA5_CR3000_MaggieMay_Res_data_1_min_1_2026_03_18_0001.dat', 'TOA5_CR3000_MaggieMay_Res_data_1_min_2_2026_03_18_0833.dat']
    # download_dfs(station, filenames_array)

    """
    Section to horizontally concatenate auto
    """

    # Maggie May
    stack_dfs_2(True)

    # Layla
    stack_dfs_2(False)


    """
    # Maggie May Plot (see above section on concatenation)
        Can change the word inside quotation to change variable to plot
    """
    # # variables: "SW_up [W/m^2]", "SW_down [W/m^2]", "LW_up [W/m^2]", "LW_down [W/m^2]"  
    # all_vars =  ["SW_up [W/m^2]", "SW_down [W/m^2]", "LW_up [W/m^2]", "LW_down [W/m^2]"]
    SW_vars = ["SW_up [W/m^2]", "SW_down [W/m^2]" ]
    # LW_vars = ["LW_up [W/m^2]", "LW_down [W/m^2]"] 


    """
    For 3.19 presentation
    """
    # time_series_plot_maggie_may(SW_vars)
    # time_series_plot_maggie_may(LW_vars)



    """
    PLOTS
    """

    ### Albedo
    # Layla
    # albedo_plot_and_calc("DataDataData/Dataframes/New_L_Combined_LatestUpdate.csv")
    # # Maggie May
    # albedo_plot_and_calc("DataDataData/Dataframes/New_MM_Combined_LatestUpdate.csv")

    ### Net Radiation
    # Layla
    # net_rad_and_plot("DataDataData/Dataframes/New_L_Combined_LatestUpdate.csv")
    # # Maggie May
    # net_rad_and_plot("DataDataData/Dataframes/New_MM_Combined_LatestUpdate.csv")





main()


# Current Goals:
# Combine the layla data together, with correction for the incorrect sensor placements at the start
# Multi plots
# Update dataframe/csv with albedo column + whatever other data products we might want


# LAYLA plots - temp loggers + radiation
# net radiation
#