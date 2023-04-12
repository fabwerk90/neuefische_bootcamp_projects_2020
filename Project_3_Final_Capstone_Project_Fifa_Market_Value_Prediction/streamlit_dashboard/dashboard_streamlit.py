# Relevant libraries
import streamlit as st
import pandas as pd
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter, CDSView, GroupFilter

# prepare dataframes and set unique identifier to select between field players and goalkeepers later on

absolute_path_fp = "neuefische_bootcamp_projects_2020/blob/main/Project_3_Final_Capstone_Project_Fifa_Market_Value_Prediction/streamlit_dashboard/fp_data_final_connected.csv"
absolute_path_gk = "neuefische_bootcamp_projects_2020/blob/main/Project_3_Final_Capstone_Project_Fifa_Market_Value_Prediction/streamlit_dashboard/gk_data_final_connected.csv"

df_fp = pd.read_csv(absolute_path_fp, index_col=0)
df_fp["identifier"] = "fp"

df_gk = pd.read_csv(absolute_path_gk, index_col=0)
df_gk["identifier"] = "gk"
df_gk.main_position = df_gk.main_position.replace({'Torwart': "Goalkeeper"})

# creating column for over- and undervaluation
df_fp.loc[df_fp['difference'] >= 5000000, "residual_valuation"] = "Highly Undervalued by FIFA20"
df_fp.loc[(df_fp['difference'] < 5000000) & (df_fp['difference'] >= 1000000), "residual_valuation"] = "Undervalued by FIFA20"
df_fp.loc[(df_fp['difference'] < 1000000) & (df_fp['difference'] >= -1000000), "residual_valuation"] = "Similar Valuation"
df_fp.loc[(df_fp['difference'] < -1000000) & (df_fp['difference'] >= -4000000), "residual_valuation"] = "Overvalued by FIFA20"
df_fp.loc[(df_fp['difference'] < -4000000), "residual_valuation"] = "Highly Overvalued by FIFA20"

df_gk.loc[df_gk['difference'] >= 2500000, "residual_valuation"] = "Highly Undervalued by FIFA20"
df_gk.loc[(df_gk['difference'] < 2500000) & (df_gk['difference'] >= 700000), "residual_valuation"] = "Undervalued by FIFA20"
df_gk.loc[(df_gk['difference'] < 700000) & (df_gk['difference'] >= -700000), "residual_valuation"] = "Similar Valuation"
df_gk.loc[(df_gk['difference'] < -700000) & (df_gk['difference'] >= -1500000), "residual_valuation"] = "Overvalued by FIFA20"
df_gk.loc[df_gk['difference'] < -1500000, "residual_valuation"] = "Highly Overvalued by FIFA20"


# add widgets to plot
st.header("FIFA Dashboard")

st.subheader("An interactive explorer for actual and predicted market values of football players")

st.markdown("Each player is represented via a circle. To see individual attributes of each player simply hover over the circles")
st.markdown("Interact with the widgets on the left to select different players, depending on their age, rating from the FIFA20 video game or their position on the field")
st.markdown("You can also search individual players by using the text input at the left bottom (you can put the whole name or just a few letters)")


# widgets update the plot via the below defined update function

# field players or goalkeepers?
datasource_selection = st.sidebar.radio("Select field players or goalkeepers",('Field players', 'Goalkeepers'))

# age intervals
age_selection = st.sidebar.slider("Select Age Interval", 18, 40, (18, 40))

# overall ratings
rating_selection = st.sidebar.slider("Select Overall FIFA Rating", 45, 99, (45, 99))

# position selection
all_positions = df_fp.main_position.unique().tolist()
position_selection = st.sidebar.multiselect("Select one or many Positions (does not apply to Goalkeepers)", options=all_positions, default=["Centre Back", "Defensive Midfield", "Striker"])

# text input for player search (player names were converted to lowercase due to improved usability)
player_selection = st.sidebar.text_input("Search Player by full name or substring")

# define update function, so that users can interact with the plot and data is updated after every input

# select function

def update_dataframe(df_fp, df_gk, datasource_selection, age_selection, rating_selection, position_selection, player_selection):

    if datasource_selection == "Field players":
        datasource_updated_df = df_fp
        identifier = "field"
    else:
        datasource_updated_df = df_gk
        identifier = "gk"

    age_updated_df = datasource_updated_df.query(f"{age_selection[0]} <= player_age <= {age_selection[1]}")

    rating_updated_df = age_updated_df.query(f"{rating_selection[0]} <= overall <= {rating_selection[1]}")

    if identifier == "field":
        position_updated_df = rating_updated_df[rating_updated_df["main_position"].isin(position_selection)]
    else:
        position_selection_gk = ["Goalkeeper"]
        position_updated_df = rating_updated_df[rating_updated_df["main_position"].isin(position_selection_gk)]

    position_updated_df['long_name'] = position_updated_df['long_name'].str.lower()
    if player_selection:
        clean_string = player_selection.strip()
        text_filtered_df = position_updated_df[position_updated_df['long_name'].str.contains(clean_string)]
    else:
        text_filtered_df = position_updated_df

    final_df = text_filtered_df

    datasource = ColumnDataSource(
    data={
        "name": final_df["long_name"].str.title(),
        "age": final_df["player_age"],
        "overall": final_df["overall"],
        "position": final_df["main_position"],
        "continent": final_df["geographical_continent"],
        "transfermarkt_mw": final_df["actual_market_value"],
        "predicted_mw": final_df["predicted_market_value"],
        "difference": final_df["difference"],
        "valuation": final_df["residual_valuation"]
        }
    )

    return datasource


def update_plot(datasource):

    # build filter for over- and undervaluation
    high_underval_filter = [GroupFilter(column_name='valuation', group='Highly Undervalued by FIFA20')]
    high_underval_view = CDSView(source=datasource,filters=high_underval_filter)

    underval_filter = [GroupFilter(column_name='valuation', group='Undervalued by FIFA20')]
    underval_view = CDSView(source=datasource,filters=underval_filter)

    accept_range_filter = [GroupFilter(column_name='valuation', group='Similar Valuation')]
    accept_range_view = CDSView(source=datasource,filters=accept_range_filter)

    overval_filter = [GroupFilter(column_name='valuation', group='Overvalued by FIFA20')]
    overval_view = CDSView(source=datasource, filters=overval_filter)

    high_overval_filter = [GroupFilter(column_name='valuation', group='Highly Overvalued by FIFA20')]
    high_overval_view = CDSView(source=datasource, filters=high_overval_filter)

    # tooltips

    TOOLTIPS = """
        <div>
            <div>
                    <span style="font-size: 14px; font-weight: bold;">@name</span>
            </div>
            <div>
                    <span style="font-size: 12px;">Age: @age</span>
            </div>
            <div>
                    <span style="font-size: 12px;">Main Position: @position</span>
            </div>
            <div>
                    <span style="font-size: 12px;">FIFA-Rating: @overall</span>
            </div>
            <div>
                    <span style="font-size: 12px;">Transfermarkt MV: @transfermarkt_mw{0,0}</span>
            </div>
            <div>
                    <span style="font-size: 12px;">Predicted MV: @predicted_mw{0,0}</span>
            </div>
    """

    # toolbar

    select_tools = ["pan,wheel_zoom,box_zoom,reset,save,crosshair"]

    # define our basic plot
    plot = figure(title='', 
                x_axis_label='Actual market value in €', 
                y_axis_label='Predicted market value in €',
                x_range=(0, 26000000), 
                y_range=(0, 26000000),
                y_axis_location="right",
                plot_height=500, plot_width=900,
                tools=select_tools,
                toolbar_location="below",
                tooltips=TOOLTIPS)

    plot.outline_line_width = 2
    plot.outline_line_alpha = 1
    plot.toolbar.autohide = True
        
    # draw actual data as a circle glyph on the plot
    plot.circle("transfermarkt_mw", "predicted_mw", source=datasource, size=8,
                color='seagreen', legend='Highly Undervalued by FIFA20', view=high_underval_view)

    plot.circle("transfermarkt_mw", "predicted_mw", source=datasource, size=8,
                color='yellowgreen', legend='Undervalued by FIFA20', view=underval_view)

    plot.circle("transfermarkt_mw", "predicted_mw", source=datasource, size=8,
                color='cornflowerblue', legend='Similar Valuation', view=accept_range_view)

    plot.circle("transfermarkt_mw", "predicted_mw", source=datasource, size=8,
                color='coral', legend='Overvalued by FIFA20', view=overval_view)

    plot.circle("transfermarkt_mw", "predicted_mw", source=datasource, size=8,
                color='maroon', legend='Highly Overvalued by FIFA20', view=high_overval_view)

    # legend configuration
    plot.legend.location ='top_left'
    plot.legend.title = 'Click legend to hide/display data'
    plot.legend.title_text_font_style = "bold"
    plot.legend.title_text_font_size = "12pt"
    plot.legend.title_text_color = "white"
    plot.legend.label_text_font = "arial"
    plot.legend.label_text_font_size = "10pt"
    plot.legend.background_fill_color = "ghostwhite"
    plot.legend.border_line_color = "white"
    plot.legend.border_line_width = 4
    plot.legend.border_line_alpha = 0.5

    plot.legend.click_policy = 'hide'

    # convert axis to readable format
    plot.yaxis.formatter=NumeralTickFormatter(format="0,0")
    plot.xaxis.formatter=NumeralTickFormatter(format="0,0")

    # configurate axis ticks
    plot.xaxis.axis_label_text_font_size = "15pt"
    plot.xaxis.major_label_text_font_size = "12pt"
    plot.xaxis.axis_label_text_font_style = "normal"
    plot.xaxis.axis_label_text_font = "arial"
    plot.xaxis.axis_label_text_color = "white"


    plot.yaxis.axis_label_text_font_size = "15pt"
    plot.yaxis.major_label_text_font_size = "12pt"
    plot.yaxis.axis_label_text_font_style = "normal"
    plot.yaxis.axis_label_text_font = "arial"
    plot.yaxis.axis_label_text_color = "white"

    return plot

plot_datasource = update_dataframe(df_fp, df_gk, datasource_selection, age_selection, rating_selection, position_selection, player_selection)
plot = update_plot(plot_datasource)


# add a html description to the layout

doc = curdoc()
doc.theme = "dark_minimal"
doc.add_root(plot)

st.bokeh_chart(plot)