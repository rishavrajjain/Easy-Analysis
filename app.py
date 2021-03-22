import pyTigerGraph as tg
import streamlit as st
import pandas as pd
import flat_table
import plotly.express as px
from streamlit_agraph import agraph, Config, Node, Edge
import json
import matplotlib.pyplot as plt
import matplotlib
from documentation import docs

graph = tg.TigerGraphConnection(
    host="https://9f5d92a5037b47ea9431606ee29032a3.i.tgcloud.io",
    graphname="MyGraph",
    apiToken="jh0ppbq90n7lfdu0khe57vthv8n7eqij")  # make a connection to TigerGraph Box
authToken = graph.getToken(
    "jh0ppbq90n7lfdu0khe57vthv8n7eqij",
    "100000000000000000")
print(authToken)


menuItems = [
    'Tiger Graph Data Analysis',
    'Automatic Data Analysis',
    'Documentation']
st.sidebar.title('Easy Analysis')


itemSelected = st.sidebar.selectbox('', menuItems)
github = '''[ Fork/Star on Github]()'''
st.sidebar.info(github)

if itemSelected == 'Tiger Graph Data Analysis':
    st.title('Covid-19 Data Analysis')
    min_age, max_age = st.slider("Select Age Range", 0, 104, [10, 20])
    sex = st.multiselect('Sex', ['male', 'female'])

    results = graph.runInstalledQuery("ageandgender")
    # data=graph.runInstalledQuery("infectionSubgraph");
    # print(data)

    

    df = pd.DataFrame(results[0]["s2"])

    data = flat_table.normalize(df)
    data = data[['v_id',
                 'attributes.Age',
                 'attributes.Sex',
                 'attributes.Location.latitude',
                 'attributes.Location.longitude']]
    if(len(sex) == 1):
        data = data[data['attributes.Sex'] == sex[0]]

    data = data[data['attributes.Age'].between(left=min_age, right=max_age)]

    

    gender_data = data['attributes.Sex']

    test_data = gender_data.value_counts()

    age = data['attributes.Age']
    age_data = age.value_counts()

    st.write("Covid-19 Cases variation in different Genders")
    st.bar_chart(test_data)

    st.write("Covid-19 Cases variation in different ages")
    st.bar_chart(age_data)

    # Tiger Graph patient subinfection query data analysis - plot
    
    f = open('patientInfection.json')

    print('check')
    trp_data = f.read()
    print(type(trp_data))

    temp_data = json.loads(trp_data)
    temp_data = temp_data[0]
    print(type(temp_data))
    print(temp_data["@@edgeSet"][0])

    nodes = []
    edges = []
    for val in temp_data["@@edgeSet"]:
        nodes.append(Node(id=val['from_id']))
        nodes.append(Node(id=val['to_id']))
        edges.append(
            Edge(
                source=val['from_id'],
                target=val['to_id'],
                labelProperty=val['e_type'],
                renderLabel=True))

    config = Config(
        height=500,
        width=700,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        directed=True,
        collapsible=True)

    agraph(nodes, edges, config)

elif itemSelected == 'Automatic Data Analysis':
    st.title('Automatic Data Analysis')

    data = st.file_uploader("Upload a Dataset", type=["csv"])
    if data is not None:
        df = pd.read_csv(data)
        st.dataframe(df)

        if st.checkbox("Show Shape"):
            st.write(df.shape)

        if st.checkbox("Show Columns"):
            all_columns = df.columns.to_list()
            st.write(all_columns)

        if st.checkbox("Summary"):
            st.write(df.describe())

        if st.checkbox("Plot data for a column"):
            selected_column = st.selectbox("Select Columns", all_columns)
            new_df = df[selected_column]
            st.dataframe(new_df.value_counts())
            st.bar_chart(new_df.value_counts())

        if st.checkbox("Advance Plots and Analysis"):

            all_columns_names = df.columns.tolist()
            type_of_plot = st.selectbox(
                "Select Type of Plot", [
                    "area", "bar", "line"])
            selected_columns_names = st.multiselect(
                "Select Columns To Plot", all_columns_names)
            if st.button("Generate Plot"):
                st.success(
                    "Generating Customizable Plot of {} for {}".format(
                        type_of_plot, selected_columns_names))

                # Plot By Streamlit
                if type_of_plot == 'area':
                    cust_data = df[selected_columns_names]
                    st.area_chart(cust_data)

                elif type_of_plot == 'bar':
                    cust_data = df[selected_columns_names]
                    st.bar_chart(cust_data)

                elif type_of_plot == 'line':
                    cust_data = df[selected_columns_names]
                    st.line_chart(cust_data)

                


if itemSelected == 'Documentation':
    st.write('Documentation')
    st.markdown(docs())
