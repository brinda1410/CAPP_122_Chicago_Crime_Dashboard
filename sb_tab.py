import pandas as pd
import plotly.express as px
from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Read csv

merged_filename = "data/merged_data.csv"
small_bus = pd.read_csv(merged_filename)

#WARD,FS AGENCIES,SB FUNDS,MICRO LOANS,ARSON,ASSAULT,BATTERY,BURGLARY,CONCEALED CARRY LICENSE VIOLATION,CRIM SEXUAL ASSAULT,CRIMINAL DAMAGE,CRIMINAL SEXUAL ASSAULT,CRIMINAL TRESPASS,DECEPTIVE PRACTICE,GAMBLING,HOMICIDE,HUMAN TRAFFICKING,INTERFERENCE WITH PUBLIC OFFICER,INTIMIDATION,KIDNAPPING,LIQUOR LAW VIOLATION,MOTOR VEHICLE THEFT,NARCOTICS,NON-CRIMINAL,OBSCENITY,OFFENSE INVOLVING CHILDREN,OTHER NARCOTIC VIOLATION,OTHER OFFENSE,PROSTITUTION,PUBLIC INDECENCY,PUBLIC PEACE VIOLATION,RITUALISM,ROBBERY,SEX OFFENSE,STALKING,THEFT,WEAPONS VIOLATION,Commercial,General Commercial,General Industrial,General commercial,General industrial,Industrial,Landlord,Manufacturing,Mixed-Use: Retail and Commercial,Mixed-Use: Retail and Residential,Office,Retail,Warehousing,After School Program,Basic Street Outreach,Behavioral Health Support (At-Risk Youth),CHA After School Program,Caregiver Services,Chicago Children’s Advocacy Center,Child Care Only,Chore Services,Clinical Services,Community Hospitality Center (Drop-In Centers),Community Re-Entry Support Centers,Comprehensive Fitness,Congregate Dining,Counseling and Case Management Services,Court House Domestic Violence,Digital Literacy Program,Early Childhood/Family Initiative,Early Head Start,Early Head Start Support Services,Early Head Start Support Services – Child Care Partnership,Early Head Start – Child Care Partnership,Early Head Start – RTL,Early Learning for Immigrant Families,Emergency Food Assistance for At-Risk Population,Emergency Shelter,Employment Preparation and Placement Program,FUSE-Families,Family Violence Prevention Initiative,Greencorps Program,Head Start,Head Start Support Services,Head Start Support Services – RTL,Head Start – RTL,Health and Wellness Promotion,Home Delivered Meals,Homeless Prevention,Homeless Youth Engagement: Youth Drop-In Centers,Homeless Youth Overnight Shelter: Low-Threshold,Homelessness Prevention,Housing Relocation Counseling for At-Risk Seniors,Industry-Specific Training and Placement Program,Intensive Case Advocacy and Support For At-Risk Seniors,Intensive Youth Services,Interim Housing,Interim Housing-Youth,JISC,Legal Advocacy and Case Management,Legal Services,Legal Services for Victims of Domestic Violence,Low Threshold Youth Overnight Shelter,Mentoring,Mobile Outreach Human Services,Neighborhood Clean-up,Older Relatives Raising Children,One Summer Chicago +PLUS Program,Out of School Time Programming - School Year Only,Out of School Time Programming - Summer Only,Out of School Time Programming - Summer and School Breaks,Out of School Time Programming - Year Round,Out-of-School Time – Year Round Program,Outreach and Engagement,Outreach and Engagement Coordinator,Permanent Housing with Short-term Supports,Permanent Supportive Housing,Plan to End Homelessness,Project Based Transitional Housing,Public Benefits Outreach and Enrollment,RISE,Rapid Re-housing Program,Resource and Information Management,Safe Havens Program,Satellite Senior Centers,Scattered Site Transitional,Senior Community Service Employment Program (SCSEP),Shelter Plus Care,Specialized Outreach and Engagement Services,Specialized Servcies:  Clinical Services,Specialized Services:  SSI/SSDI,Summer Youth Employment Program,Summer Youth Program,Supervised Visitation and Safe Exchange,System Coordinator,Tax Preparation Assistance,Technical Assistance and Training,Transitional Jobs Program,Youth Drop-In Center,Youth Outreach Program,Youth Work Experience Program,Youth Working for Success,Youth-Intentional Permanent Supportive Housing,Children Services,Domestic Violence,Homeless Services,Human Services Delivery,Senior Services,Workforce Services,Youth Services,Accion,CNI,WBDC,Arts/Crafts Production,Auto/Vehicle,Beauty/Salon Services,Catering,Clothing Design/Mfg,Clothing/Material Production,Construction,Construction/Repair,Day Care,Education,Electronics,Entertainment,Entertainment/Manufacturing,Enviromental Consulting,"Fashion, jewelry, art and sewing/ jewelry classes",Food/Beverage,IT/Manufacturing,Manufacturing - Microloans,Medical Services,Other Services,Other Services - Barbershop,Other Services - Childcare,Other Services - Cosmetology,Other Services - Education,Other Services - Tire Repair,Other Services -Childcare,Professional/Off Svc,Real Estate Consultant,Restaurant - Full Service,Retail Sales ,Retail Sales - Other,Retail Services - Other,Retail Stores,Retail sales,Service,Transportation,Wholesale,transportation
#project_name, ward, incentive_amount,"\
      #  "total_project_cost, jobs_created_aspirational, jobs_retained_aspirational"


# Subset ward and crime-type columns
SB = small_bus.loc[:, 'WARD': 'SB FUNDS']

SB.drop(['FS AGENCIES'], axis = 1, inplace = True)
SB.dropna( axis = 0, inplace = True)
print(SB)
col_names = SB.columns[1:] # without WARD column

# App Layout - DCC and HTML components
sb_layout = html.Div([
        html.H2("Small Bussines Data", style = {'text-align': 'left'}),
        html.Br(),
        html.Label(['Total project cost'], style={'font-weight': 'bold', "text-align": "left"}),
        html.Br(),
        dcc.Dropdown(id = "small_bussines_incentives",
                   # options = [{"label": str(x), "value": x} for x in col_names], 
                    value = col_names[0],
                    multi = False,
                    style = {'width': "40%"}),
        #html.Div(id = 'output_container', children = []),
        dcc.Graph(id = 'bar_graph_small_bussines_incentives_type_by_ward', figure = {})
    ])

# Connect Plotly graphs with Dash Core Components
@app.callback(
    Output(component_id = 'bar_graph_small_bus_incent_by_ward', component_property = 'figure'),
    [Input(component_id = 'small_bussines_incentives', component_property = 'value')]
    )

def update_graph(sb_slctd):
    '''
    Define the callback function to render filtered
    pandas dataframe based on user's input value in Dropdown
    'small_bussines_incentives'
    '''
    #container_crime = "The crime type selected by the user is {}".format(sb_slctd)
    SB_copy = small_bus.copy()
    SB_copy.dropna(subset=[sb_slctd], inplace = True)
    graphtitle = sb_slctd.lower().capitalize() + 'small business incentives disaggregated at ward-level'
    fig = px.bar(SB_copy, x = 'WARD', y = sb_slctd, title = graphtitle)
    return fig

