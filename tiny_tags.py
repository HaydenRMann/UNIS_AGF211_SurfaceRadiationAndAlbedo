import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import unisacsi.Meteo as met # used to open TinyTag data
import matplotlib.dates as mdates
import os      


def tiny_tags_plot():
    path_data = 'DataDataData/albedo_radiation'

    # Get TinyTags data
    df_TT3_inside = met.read_Tinytag(os.path.join(path_data, "TT3_26_03_20.txt"))
    df_TT16_outside = met.read_Tinytag(os.path.join(path_data, "TT16_26_03_20.txt"))

    # Correction Coefficients: From Dr. Lukas Frank
        #   Tinytags:
        # T_ref = T + offset

        # 		offset
        # TT16 T_black 	-0.055
        # TT16 T_white 	-0.019
        # TT3 T_black  	-0.026
        # TT3 T_white  	-0.031
    
    # Snow Correction
    df_TT3_inside["T_white [degC]"]     += -0.031
    df_TT16_outside["T_white [degC]"]   += -0.019

    # Air Correction
    df_TT3_inside["T_black [degC]"]     += -0.026
    df_TT16_outside["T_black [degC]"]   += -0.055

    # Instantiate Figure
    fig, (ax_snow, ax_air) = plt.subplots(2,1, figsize=(12,6))

    # Plot snow temp (inside greenhouse)
    df_TT3_inside.plot(y="T_white [degC]", ax=ax_snow, c="lightblue", label="Inside Greenhouse (Snow)")

    # Formatting
    ax_snow.set_ylabel("temperature [degC]", c="b")
    ax_snow.tick_params(axis='y', colors="b", labelcolor="b")
    ax_snow.grid("both")
    ax_snow.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))

    # Plot snow temp (outside greenhouse)
    df_TT16_outside.plot(y="T_white [degC]", ax=ax_snow, c="darkblue", label="Outside Greenhouse (Snow)")

    # Formatting
    ax_snow.legend(loc="lower right")
    ax_snow.set_title("Snow Temperature", fontsize=14)
    ax_snow.set_ylim([-12, 7])
    
    # Timestamp of greenhouse doors being opened
    time_point = pd.Timestamp("2026-03-19 15:15")

    # Formatting
    ax_snow.set_xlabel("")
    ax_snow.set_xticklabels([])
    ax_snow.grid("both")

    # Vertical line when greenhouse was opened
    ax_snow.axvline(
        x=time_point,
        color="red",
        linestyle=":",
        linewidth=2,
        label="Greenhouse door opened",
        zorder=1
    )
    ax_snow.legend(loc="upper right", fontsize=12)

    # Plot air temperature (inside greenhouse)
    df_TT3_inside.plot(y="T_black [degC]", ax=ax_air, c="lightgreen", label = "Inside Greenhouse (Air)")

    # Formatting
    ax_air.set_ylabel("temperature [degC]", c="b")
    ax_air.tick_params(axis='y', colors="black", labelcolor="black", labelsize=12)

    ax_snow.tick_params(axis='y', colors="black", labelcolor="black", labelsize=12)

    ax_air.grid("both")
    ax_air.legend(loc="lower right")
    ax_air.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d.%b %H:%M'))

    # Plot air temperature (outside greenhouse)
    df_TT16_outside.plot(y="T_black [degC]", ax=ax_air, c="darkgreen", label = "Outside Greenhouse (Air)")
    ax_air.legend(loc="lower right")
    ax_air.set_ylim([-12, 7])
    ax_air.grid("both")
    ax_air.set_xlabel("")
    ax_air.set_title("Air Temperature", fontsize=14)
 
    # Vertical line when greenhouse was opened
    ax_air.axvline(
        x=time_point,
        color="red",
        linestyle=":",
        linewidth=2,
        label="Greenhouse door opened",
        zorder=1
    )

    # Axes formatting
    ax_air.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12]))
    ax_air.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b %H:%M'))
    ax_air.legend(loc="upper right", fontsize=12)

    ax_air.grid(True, which='major', axis='x', linestyle='-', alpha=0.7)
    for label in ax_air.get_xticklabels():
        label.set_horizontalalignment('center')

    ax_air.tick_params(axis='x', labelrotation=0, labelsize=12)

    ax_snow.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12]))
    ax_snow.xaxis.set_major_formatter(mdates.DateFormatter('%d.%b %H:%M'))
    ax_snow.legend(loc="upper right", fontsize=12)

    ax_snow.grid(True, which='major', axis='x', linestyle='-', alpha=0.7)
    for label in ax_snow.get_xticklabels():
        label.set_horizontalalignment('center')

    ax_snow.tick_params(axis='x', labelrotation=0)
    ax_snow.set_xlabel("")
    ax_snow.set_xticklabels([])

    
    # Overall figure formatting
    fig.supxlabel("Date and Time [UTC]", y=0.10, fontsize=14)
    ax_snow.set_ylabel("")
    ax_air.set_ylabel("")
    fig.supylabel("Temperature [°C]", x=0.068, y=0.52, fontsize=14)

    ax_snow.text(-0.14, 1.12, '(a)', transform=ax_snow.transAxes,
          fontsize=16, va='top', ha='left')

    ax_air.text(-0.14, 1.12, '(b)', transform=ax_air.transAxes,
           fontsize=16, va='top', ha='left')


    # Save plot
    plt.savefig('TINYTAG_MOSTRECENT_MAY5.png', dpi=600)

    # Show plot
    plt.show()


def TT_data_analysis():
    """

    Provided the data needed to build our report.

    Data Dict:
    # Snow
    df_TT3_inside["T_white [degC]"]  
    df_TT16_outside["T_white [degC]"]  
    # Air
    df_TT3_inside["T_black [degC]"]   
    df_TT16_outside["T_black [degC]"] 

    greenhouse_toggle = pd.Timestamp("2026-03-19 15:15")
    """
    path_data = '/Users/hmann/Library/CloudStorage/OneDrive-BowdoinCollege/Documents/UNIS/AGF211/CruiseWork/DataDataData/albedo_radiation'
    df_TT3_inside = met.read_Tinytag(os.path.join(path_data, "TT3_26_03_20.txt"))
    df_TT16_outside = met.read_Tinytag(os.path.join(path_data, "TT16_26_03_20.txt"))

    inside_snow = df_TT3_inside["T_white [degC]"]  
    inside_air = df_TT3_inside["T_black [degC]"]   

    outside_snow = df_TT16_outside["T_white [degC]"] 
    outside_air = df_TT16_outside["T_black [degC]"] 


    # Mean/min/max for each regime
    print("In GH / In snow Overall Mean: " + str(inside_snow.mean()))
    print("In GH / In air Overall Mean: " + str(inside_air.mean()))
    print("Out GH / In snow Overall Mean: " + str(outside_snow.mean()))
    print("Out GH / In Air Overall Mean: " + str(outside_air.mean()))

    print("In GH / In snow Overall Min: " + str(inside_snow.min()))
    print("In GH / In air Overall Min: " + str(inside_air.min()))
    print("Out GH / In snow Overall Min: " + str(outside_snow.min()))
    print("Out GH / In Air Overall Min: " + str(outside_air.min()))

    print("In GH / In snow Overall Max: " + str(inside_snow.max()))
    print("In GH / In air Overall Max: " + str(inside_air.max()))
    print("Out GH / In snow Overall Max: " + str(outside_snow.max()))
    print("Out GH / In Air Overall Max: " + str(outside_air.max()))


    print("In GH / In snow Closed GH Mean: " + str(inside_snow.mean()))
    print("In GH / In air Closed GH Mean: " + str(inside_air.mean()))

    print("In GH / In snow Closed GH Min: " + str(inside_snow.min()))
    print("In GH / In air Closed GH Min: " + str(inside_air.min()))

    print("In GH / In snow Closed GH Max: " + str(inside_snow.max()))
    print("In GH / In air Closed GH Max: " + str(inside_air.max()))


    tp1 = pd.Timestamp("2026-03-19 8:00")
    tp2 = pd.Timestamp("2026-03-19 16:00")
    diff = inside_air[tp1:tp2].mean() - outside_air[tp1:tp2].mean()
    print(diff)

    tp3 = pd.Timestamp("2026-03-20 8:00")
    tp4 = pd.Timestamp("2026-03-20 12:00")
    diff = inside_air[tp3:tp4].mean() - outside_air[tp3:tp4].mean()
    print(diff)

    tp1 = pd.Timestamp("2026-03-19 8:00")
    tp2 = pd.Timestamp("2026-03-19 16:00")
    diff = inside_snow[tp1:tp2].mean() - outside_snow[tp1:tp2].mean()
    print(diff)

    tp3 = pd.Timestamp("2026-03-20 8:00")
    tp4 = pd.Timestamp("2026-03-20 12:00")
    diff = inside_snow[tp3:tp4].mean() - outside_snow[tp3:tp4].mean()
    print(diff)


    #  Additional code needed for our report results
    # t_greenhouse_closed = pd.Timestamp("2026-03-18 17:47:00")
    # t_greenhouse_opened = pd.Timestamp("2026-03-19 15:15:00")
    # print("HEREHERHEHRE")
    # t_startinggreenhouse = pd.Timestamp("2026-03-18 17:47:00")
    # t_nodev = pd.Timestamp("2026-03-19 08:00:00")
    # print(inside_snow[t_startinggreenhouse:t_nodev].mean())
    # print(outside_snow[t_startinggreenhouse:t_nodev].mean())
    # print(inside_air[t_startinggreenhouse:t_nodev].mean())
    # print(outside_air[t_startinggreenhouse:t_nodev].mean())

    return None




def read_Tinytag_csv(path):
    """
    Fx hard coded by H. Mann to read tinytag CSVs because he didn't realize that UNIS provided
    code to already do this.
    """

    import pandas as pd

    df = pd.read_csv(
        path,
        encoding="latin1",
        skiprows=5,
        dayfirst=True
    )

    # Rename columns to match your existing code
    df.columns = ["Index", "Time", "T_black [degC]", "T_white [degC]"]

    # Parse time
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    
    # Clean temperature values
    for col in ["T_black [degC]", "T_white [degC]"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("°C", "", regex=False)
            .str.strip()
            .astype(float)
        )

    return df

def main():
    """
    Toggle required fxs
    """

    # Plot
    tiny_tags_plot()

    # Data (lots of print - clear terminal for ease)
    TT_data_analysis()

main()