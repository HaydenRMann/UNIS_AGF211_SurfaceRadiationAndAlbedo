"""

Author: Hayden Mann

Description: Plots shortwave radiation balance, longwave radiation balance,
net radiation balance, and albedo.

"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from data_analysis import stack_dfs_2



def get_data():
    """
    Grabs the data from data_analysis.py and returns
    two dataframes: one for Layla (experimental station)
    and one for Maggie May (control station). Called in main().
    """

    df_layla = stack_dfs_2(False)
    df_maggie_may = stack_dfs_2(True)

    # Adjust for swapped LW sensors: See section on data processing in our paper if confused.
    cutoff = pd.Timestamp("2026-03-18 14:27:00")    
    df_layla["LW_down_cor"] = np.where(df_layla.index <= cutoff, df_layla["LW_up [W/m^2]"],df_layla["LW_down [W/m^2]"])
    df_layla["LW_up_cor"] = np.where(df_layla.index <= cutoff, df_layla["LW_down [W/m^2]"],df_layla["LW_up [W/m^2]"])
    df_layla["LW_up [W/m^2]"] = df_layla["LW_up_cor"]
    df_layla["LW_down [W/m^2]"] = df_layla["LW_down_cor"]
    df_layla["Net Radiation [W/m^2]"] = -1 * df_layla["SW_up [W/m^2]"] + df_layla["SW_down [W/m^2]"] - df_layla["LW_up [W/m^2]"] + df_layla["LW_down [W/m^2]"]
    df_maggie_may["Net Radiation [W/m^2]"] = -1 * df_maggie_may["SW_up [W/m^2]"] + df_maggie_may["SW_down [W/m^2]"] - df_maggie_may["LW_up [W/m^2]"] + df_maggie_may["LW_down [W/m^2]"]

    # align matrices by their timestamp indices
    df_layla, df_maggie_may = df_layla.align(df_maggie_may, join="inner")

    # This was used to adjust SW. See paper appendix. We had incoming SW sensors next to each other that measured
    # very different values, despite being in the same conditions
    mask = df_maggie_may["SW_down [W/m^2]"] > 20
    layla_vals = df_layla.loc[mask, "SW_down [W/m^2]"]
    maggie_vals = df_maggie_may.loc[mask, "SW_down [W/m^2]"]
    ratios = layla_vals / maggie_vals
    ratios = ratios.replace([np.inf, -np.inf], np.nan)
    mean_ratio = np.mean(ratios)
    #print(mean_ratio)
    df_layla["SW_down [W/m^2]"] = df_layla["SW_down [W/m^2]"] / mean_ratio

    
    # Albedo Calculation: Limited to when SW_down is greater than 20 [W/m^2]
    df_layla["SW_Down_Filter_Above_20 [W/m^2]"] = df_layla['SW_down [W/m^2]'].where(df_layla['SW_down [W/m^2]'] > 20)
    df_layla["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] = df_layla['SW_up [W/m^2]'].where(df_layla['SW_down [W/m^2]'] > 20)
    df_maggie_may["SW_Down_Filter_Above_20 [W/m^2]"] = df_maggie_may['SW_down [W/m^2]'].where(df_maggie_may['SW_down [W/m^2]'] > 20)
    df_maggie_may["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] = df_maggie_may['SW_up [W/m^2]'].where(df_maggie_may['SW_down [W/m^2]'] > 20)
    df_layla["Albedo"] =  df_layla["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] / df_layla["SW_Down_Filter_Above_20 [W/m^2]"] 
    df_maggie_may["Albedo"] =  df_maggie_may["SW_Up_Filter_Above_20_SW_Down [W/m^2]"] / df_maggie_may["SW_Down_Filter_Above_20 [W/m^2]"] 

    # 15 minute rolling average to smooth data
    df_L_smooth = df_layla.rolling(window=15).mean()
    df_MM_smooth = df_maggie_may.rolling(window=15).mean()

    # Returns a dataframe for Layla (experimental), and Maggie May (control)
    return df_L_smooth, df_MM_smooth



    
def two_station_plotting(df_L, df_MM, variables, colors, labels, y_unit, y_min, y_max, title):
    """
    Is used to plot shortwave and longwave radiation time series plots for both stations, within the same plot.
    Called in main().
    """

    # Formatting
    fig, (ax_L, ax_MM) = plt.subplots(2, 1, figsize=(12, 6)) 
    if title == "Shortwave Radiation": height = 170
    else: height = 322

    # Plot on each axis
    for i in range(len(variables)):
        df_L.plot(y=variables[i], ax=ax_L, c=colors[i], label=labels[i])

    for i in range(len(variables)):
        df_MM.plot(y=variables[i], ax=ax_MM, c=colors[i+2], label=labels[i])

    # Formatting Experimental Station Axes
    ax_L.tick_params(axis='both', which='major', labelsize=12)
    ax_L.grid("both")
    ax_L.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))
    ax_L.set_xlabel("")
    ax_L.set_xticklabels([])
    ax_L.set_ylim([y_min, y_max])
    ax_L.set_title("Experimental Station", fontsize=14)

    # Define timestamps for experimental regime lines
    t0 = df_L.index[0]
    t1 = pd.Timestamp("2026-03-18 10:47:00")
    t2 = pd.Timestamp("2026-03-18 17:47:00")
    t3 = pd.Timestamp("2026-03-19 15:15:00")
    t4 = df_L.index[-1]

    # Plot vertical lines representing the experimental regimes
    ax_L.axvline(x=t1, color='black', linestyle=':', label="Experimental\nRegime")
    ax_L.axvline(x=t2, color='black', linestyle=':')
    ax_L.axvline(x=t3, color='black', linestyle=':')

    # Label the experimental regimes
    if title == "Shortwave Radiation": ax_L.legend(loc="center left", fontsize=12)
    else:  ax_L.legend(loc="lower right", fontsize=12)

    ax_L.text(t0 + (t1 - t0)/2, height, "Snow", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax_L.text(t1 + (t2 - t1)/2, height, "Water", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax_L.text(t2 + (t3 - t2)/2, height, "Snow - Closed Greenhouse", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax_L.text(t3 + (t4 - t3)/2, height, "Snow - Open Greenhouse", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Formatting Control Station Axes
    ax_MM.tick_params(axis='both', which='major', labelsize=12)
    ax_MM.tick_params(axis='x', labelrotation=0)
    ax_MM.grid("both")
    ax_MM.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))
    if title == "Shortwave Radiation": ax_MM.legend(loc="center left", fontsize=12)
    else:  ax_MM.legend(loc="lower right", fontsize=12)
    ax_MM.set_xlabel("")
    ax_MM.set_ylim([y_min, y_max])
    ax_MM.set_title("Control Station", fontsize=14)
    plt.setp(ax_MM.get_xticklabels(), ha='center')
    
    # Overall formatting
    fig.supylabel(title + r' [W m$^{-2}$]', x=0.063, y=0.55, fontsize=14)
    fig.supxlabel("Date and Time [UTC]", y=0.10, fontsize=14)
    ax_L.text(-0.13, 1.12, '(a)', transform=ax_L.transAxes,
          fontsize=16, va='top', ha='left')

    ax_MM.text(-0.13, 1.12, '(b)', transform=ax_MM.transAxes,
           fontsize=16, va='top', ha='left')

    # Save plot to current folder
    if title == "Shortwave Radiation": plt.savefig('SW_MOSTRECENT_MAY5.png', dpi=600)
    else: plt.savefig('LW_MOSTRECENT_MAY5.png', dpi=600)
    
    # Show plot
    plt.show()


def net_radiation_plot(df_L, df_MM):
    """
    Plots net radiation for the control station (Layla) and the experimental station
    (Maggie May) onto one plot. Called in main().
    """

    # Formatting
    fig, ax = plt.subplots(1,1, figsize=(12, 5))
    
    # Plot both data onto the same axes
    df_MM.plot(y="Net Radiation [W/m^2]", ax=ax, c="blue", label="Control Station")
    df_L.plot(y="Net Radiation [W/m^2]", ax=ax, c="darkgreen", label="Experimental Station")
    
    # Formatting axes
    ax.set_ylabel("[W/m^2]")
    ax.tick_params(axis='y', colors="black", labelcolor="black")
    ax.grid("both")
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))
    ax.set_xlabel("")
    ax.set_ylim([-130, 30])

    # Shading the area under (or above) the net radiation curve. Can toggle off.
    ax.fill_between(df_L.index, df_L["Net Radiation [W/m^2]"], 0, alpha=0.2, color="darkgreen")
    ax.fill_between(df_MM.index, df_MM["Net Radiation [W/m^2]"], 0, alpha=0.2, color="blue")

    # Define timestamps for vertical lines of the experimental regime timestamps
    t0 = df_L.index[0]
    t1 = pd.Timestamp("2026-03-18 10:47:00")
    t2 = pd.Timestamp("2026-03-18 17:47:00")
    t3 = pd.Timestamp("2026-03-19 15:15:00")
    t4 = df_L.index[-1]

    # Plot vertical lines representing the experimental regime timestamps
    ax.axvline(x=t1, color='darkgreen', linestyle=':', label="Experimental Station Regime")
    ax.axvline(x=t2, color='darkgreen', linestyle=':')
    ax.axvline(x=t3, color='darkgreen', linestyle=':')
    ax.axhline(y=0, color="red", linestyle="--")

    # Formatting legend
    plt.legend(bbox_to_anchor=(0.663, 0.46), loc='upper left', fontsize=12)

    # Labels for the experimental regimes placed between intervals
    ax.text(t0 + (t1 - t0)/2, -110, "Snow", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.text(t1 + (t2 - t1)/2, -110, "Water", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.text(t2 + (t3 - t2)/2, -110, "Snow (Closed Greenhouse)", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.text(t3 + (t4 - t3)/2, -110, "Snow (Open Greenhouse)", ha='center', fontsize=12, color="darkgreen",
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # More final formatting
    ax.set_xlabel("Date and Time [UTC]", fontsize=14, labelpad=10)
    ax.set_ylabel("Net Radiation Balance "+ r' [W m$^{-2}$]', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='x', labelrotation=0)

    # Save figure
    plt.savefig('NET_MOSTRECENT_MAY5.png', dpi=600)

    # Show figure
    plt.show()


def albedo_plot(df_L, df_MM):
    """
    Plots albedo for the control station (Layla) and the experimental station
    (Maggie May) onto one plot. Separate fx from the net radiation fx because
    the axes labels were being difficult here. Called in main().
    """

    # Formatting
    fig, ax = plt.subplots(1,1, figsize=(12, 4))

    # Plot albedo for both stations on the same axes
    df_MM.plot(y="Albedo", ax=ax, c="black", label="Control Station")
    df_L.plot(y="Albedo", ax=ax, c="red", label="Experimental Station")

    # Formatting axes
    ax.tick_params(axis='y', colors="black", labelcolor="black")
    ax.grid("both")
    ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))
    ax.set_xlabel("")
    ax.set_ylim([0, 1])

    # Define timestamps for experimental regime timeline
    t0 = df_L.index[0]
    t1 = pd.Timestamp("2026-03-18 10:47:00")
    t2 = pd.Timestamp("2026-03-18 17:47:00")
    t3 = pd.Timestamp("2026-03-19 15:15:00")
    t4 = df_L.index[-1]

    # Print statments for the means of the different experimental regimes
    print("Maggie May")
    print(df_MM["Albedo"].mean())

    print("Layla: Snow")
    print(df_L["Albedo"][t0:t1].mean())

    print("Layla: Water")
    print(df_L["Albedo"][t1:t2].mean())

    print("Layla: Closed Greenhouse")
    print(df_L["Albedo"][t2:t3].mean())

    print("Layla: Open Greenhouse")
    print(df_L["Albedo"][t3:t4].mean())

    print("Layla: All Snow")
    combined = pd.concat([
        df_L["Albedo"][t0:t1],
        df_L["Albedo"][t2:t3],
        df_L["Albedo"][t3:t4]
    ])

    print("Layla: All Snow")
    print(combined.mean())


    # Vertical lines for experimental regimes
    ax.axvline(x=t1, color='red', linestyle=':', label="Experimental Station Regime")
    ax.axvline(x=t2, color='red', linestyle=':')
    ax.axvline(x=t3, color='red', linestyle=':')

    # Regime labels
    ax.text(t0 + (t1 - t0)*65/80, 0.9, "Snow", ha='center', color="red", fontsize=12, 
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.text(t1 + (t2 - t1)/2, 0.9, "Water", ha='center', color="red", fontsize=12, 
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.text(t2 + (t3 - t2)/2, 0.9, "Snow (Closed Greenhouse)", ha='center', color="red", fontsize=12, 
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    ax.text(t3 + (t4 - t3)/2, 0.9, "Snow (Open Greenhouse)", ha='center', color="red", fontsize=12, 
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # Formatting: Axes were tricky here... this is why this is separate from the net radiation plot
    ax.set_xlabel("Date and Time [UTC]", fontsize=16, labelpad=10)
    ax.set_ylabel("Albedo", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=14)        
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b %H:%M'))
    ax.legend(loc="lower right", fontsize=12)
    ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.7)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment('center')
    ax.tick_params(axis='x', labelrotation=0)
    fig.tight_layout()

    # Save figure
    plt.savefig('ALBEDO_MOSTRECENT_MAY5.png', dpi=600)

    # plot figure
    plt.show()


def range_and_times(df_L, df_M, var, unit):
    """
    Used to print statistics (mean/min/max) for data analyis. Must be passed
    a singular valid variable: var. Called in main().
    """

    # Define timestamps for experimental regimes
        # LAYLA
        # t0 -> t1: untouched snoiw
        # t1 -> t2: Layla over water
        # t2 -> t3: greenhouse Layla closed
        # t3 -> t4: greenhouse opened

        # MAGGIE MAY
        # t0 -> t4: Control
    t0 = df_L.index[0]
    t1 = pd.Timestamp("2026-03-18 10:47:00")
    t2 = pd.Timestamp("2026-03-18 17:47:00")
    t3 = pd.Timestamp("2026-03-19 15:15:00")
    t4 = df_L.index[-1]


    # """
    # This section prints out mean/min/max for each regime for a certain variable
    # Variable paramter: "var"
    # """
    print("\n")
    print(var)
    print("\n")
    print("Maggie May Overall Mean: " + str(df_M[var].mean()) + unit)
    print("Maggie May Overall Min: " + str(df_M[var].min()) + unit + "at " + str(df_M[var].idxmin()))
    print("Maggie May Overall Max: " + str(df_M[var].max()) + unit + "at " + str(df_M[var].idxmax()))
    print("\n")
    print("Layla Overall Mean: " + str(df_L[var].mean()) + unit)
    print("Layla Overall Min: " + str(df_L[var].min()) + unit + "at " + str(df_L[var].idxmin()))
    print("Layla Overall Max: " + str(df_L[var].max()) + unit + "at " + str(df_L[var].idxmax()))
    print("\n")

    print("Layla Snow Mean: " + str(df_L[var][t0:t1].mean()) + unit)
    print("Maggie May Mean during Layla Snow: " + str(df_M[var][t0:t1].mean()) + unit)
    print("Layla Water Mean: " + str(df_L[var][t1:t2].mean()) + unit)
    print("Maggie May Mean during Layla Water: " + str(df_M[var][t1:t2].mean()) + unit)
    print("Layla Closed Greenhouse Mean: " + str(df_L[var][t2:t3].mean()) + unit)
    print("Maggie May Mean during Layla Closed Greenhouse: " + str(df_M[var][t2:t3].mean()) + unit)
    print("Layla Open Greenhouse Mean: " + str(df_L[var][t3:t4].mean()) + unit)
    print("Maggie May Mean during Layla Open Greenhouse: " + str(df_M[var][t3:t4].mean()) + unit)
    print("\n")

    print("Layla Snow Min: " + str(df_L[var][t0:t1].min()) + unit + "at " + str(df_L[var][t0:t1].idxmin()))
    print("Maggie May Value during Layla Snow Min: " + str(df_M[var][df_L[var][t0:t1].idxmin()]))
    print("Layla Snow Max: " + str(df_L[var][t0:t1].max()) + unit + "at " + str(df_L[var][t0:t1].idxmax()))
    print("Maggie May Value during Layla Snow Max: " + str(df_M[var][df_L[var][t0:t1].idxmax()]))
    print("\n")

    print("Layla Water Min: " + str(df_L[var][t1:t2].min()) + unit + "at " + str(df_L[var][t1:t2].idxmin()))
    print("Maggie May Value during Layla Water Min: " + str(df_M[var][df_L[var][t1:t2].idxmin()]))
    print("Layla Water Max: " + str(df_L[var][t1:t2].max()) + unit + "at " + str(df_L[var][t1:t2].idxmax()))
    print("Maggie May Value during Layla Water Max: " + str(df_M[var][df_L[var][t1:t2].idxmax()]))
    print("\n")

    print("Layla Closed Greenhouse Min: " + str(df_L[var][t2:t3].min()) + unit + "at " + str(df_L[var][t2:t3].idxmin()))
    print("Maggie May Value during Layla Closed Greenhouse Min: " + str(df_M[var][df_L[var][t2:t3].idxmin()].mean()))
    print("Layla Closed Greenhouse Max: " + str(df_L[var][t2:t3].max()) + unit + "at " + str(df_L[var][t2:t3].idxmax()))
    print("Maggie May Value during Layla Closed Greenhouse Max: " + str(df_M[var][df_L[var][t2:t3].idxmax()].mean()))
    print("\n")

    print("Layla Open Greenhouse Min: " + str(df_L[var][t3:t4].min()) + unit + "at " + str(df_L[var][t3:t4].idxmin()))
    print("Maggie May Value during Layla Open Greenhouse Min: " + str(df_M[var][df_L[var][t3:t4].idxmin()].mean()))
    print("Layla Open Greenhouse Max: " + str(df_L[var][t3:t4].max()) + unit + "at " + str(df_L[var][t3:t4].idxmax()))
    print("Maggie May Value during Layla Open Greenhouse Max: " + str(df_M[var][df_L[var][t3:t4].idxmax()].mean()))
    print("\n")



def main():
    # grab data (may take a second)
    df_layla, df_maggie_may = get_data()

    # Set colors, labels
    standard_colors = ["lightgreen", "darkgreen", "lightblue", "darkblue"]
    standard_LW_SW_labels = ["Outgoing", "Incoming"]

    """
    Shortwave Radiation
    """
    df_L, df_MM, variables, colors, labels, y_unit, y_min, y_max, title = df_layla, df_maggie_may, ["SW_up [W/m^2]", "SW_down [W/m^2]"],  standard_colors, standard_LW_SW_labels, "[W/m^2]", -10, 200, "Shortwave Radiation"
    two_station_plotting(df_L, df_MM, variables, colors, labels, y_unit, y_min, y_max, title)

    """
    Longwave Radiation
    """
    df_L, df_MM, variables, colors, labels, y_unit, y_min, y_max, title = df_layla, df_maggie_may, ["LW_up [W/m^2]", "LW_down [W/m^2]"],  standard_colors, standard_LW_SW_labels, "[W/m^2]", 100, 350, "Longwave Radiation"
    two_station_plotting(df_L, df_MM, variables, colors, labels, y_unit, y_min, y_max, title)

    """
    Net Radiation
    """
    net_radiation_plot(df_layla, df_maggie_may)

    """
    Albedo
    """
    albedo_plot(df_layla, df_maggie_may)


    
    """
    Data Analysis Section
    """
    
    # Calculates and prints for all raw radiation values
    vars = ["SW_up [W/m^2]", "SW_down [W/m^2]","LW_up [W/m^2]","LW_down [W/m^2]", "Net Radiation [W/m^2]"]
    for var in vars:
        range_and_times(df_layla, df_maggie_may, var, " [W/m^2]")

    # Calculates and prints for Albedo
    range_and_times(df_layla, df_maggie_may, "Albedo", "")
    

main()