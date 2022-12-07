import pandas as pd
import streamlit as st
from ampligraph.discovery import find_nearest_neighbours
from ampligraph.utils import restore_model
from py2neo import Graph
import pickle

def recommend(movie):
    neighbors, dist = find_nearest_neighbours(model, entities=[movie], n_neighbors=6, entities_subset=ls_series)
    return neighbors.tolist()[0][1:6]

def connect_db():
    uri = 'neo4j+s://57578ac4.databases.neo4j.io'
    pwd = 'Txdm49MgQiTrSNuuaL3GVb2-M5SEorV2DJDWzfTJkXg'
    graph = Graph(uri, auth=("neo4j", pwd))
    return graph

def query_db(graph):
    if len(genre) > 0 and len(actors) > 0:
        if len(actors) == 1:
            q = 'MATCH (a1:Actor)-[:ACTED_IN]->(m:TVSeries) \
                WHERE a1.name = "' + actors[0] + '" AND '
            for x in range(len(genre)):
                q += "m.genre CONTAINS('" + genre[x] + "')"
                if x != len(genre) - 1:
                    q += " AND "
            q += " RETURN m.title AS title"
        elif len(actors) == 2:
            q = 'MATCH (a1:Actor)-[:ACTED_IN]->(m:TVSeries)<-[:ACTED_IN]-(a2:Actor) \
                WHERE a1.name = "' + actors[0] + '" AND ' + 'a2.name = "' + actors[1] + '" AND '
            for x in range(len(genre)):
                q += "m.genre CONTAINS('" + genre[x] + "')"
                if x != len(genre) - 1:
                    q += " AND "
            q += " RETURN m.title AS title"
        else:
            q = 'MATCH (a1:Actor)-[:ACTED_IN]->(m:TVSeries)<-[:ACTED_IN]-(a2:Actor) \
                WHERE a1.name = "' + actors[0] + '" AND ' + 'a2.name = "' + actors[1] + '" AND '
            for x in range(len(genre)):
                q += "m.genre CONTAINS('" + genre[x] + "')"
                if x != len(genre) - 1:
                    q += " AND "
            q += ' WITH COLLECT(m.title) AS series \
            MATCH (a1:Actor)-[:ACTED_IN]->(n:TVSeries)<-[:ACTED_IN]-(a2:Actor) \
            WHERE a1.name = "' + actors[0] + '" AND a2.name = "' + actors[2] + '" AND n.title IN series \
            RETURN n.title AS title'
    elif len(genre) > 0:   
        q = "MATCH (m:TVSeries) WHERE "
        for x in range(len(genre)):
            q += "m.genre CONTAINS('" + genre[x] + "')"
            if x != len(genre) - 1:
                q += " AND "
        q += " RETURN m.title AS title"
    elif len(actors) > 0:
        if len(actors) == 1:
            q = 'MATCH (a1:Actor)-[:ACTED_IN]->(m:TVSeries) \
                WHERE a1.name = "' + actors[0] + '" RETURN m.title AS title'
        elif len(actors) == 2:
            q = 'MATCH (a1:Actor)-[:ACTED_IN]->(m:TVSeries)<-[:ACTED_IN]-(a2:Actor) \
                WHERE a1.name = "' + actors[0] + '" AND ' + 'a2.name = "' + actors[1] + '" RETURN m.title AS title'
        else:
            q = 'MATCH (a1:Actor)-[:ACTED_IN]->(m:TVSeries)<-[:ACTED_IN]-(a2:Actor) \
                WHERE a1.name = "' + actors[0] + '" AND ' + 'a2.name = "' + actors[1] + '"'
            q += ' WITH COLLECT(m.title) AS series \
            MATCH (a1:Actor)-[:ACTED_IN]->(n:TVSeries)<-[:ACTED_IN]-(a2:Actor) \
            WHERE a1.name = "' + actors[0] + '" AND a2.name = "' + actors[2] + '" AND n.title IN series \
            RETURN n.title AS title'

    r = graph.query(q)
    d = r.data()

    series_title = []
    for s in d:
        series_title.append(s['title'])

    st.write('TV Shows:', series_title)

movies_list = pickle.load(open('./tvseries_list.pkl', 'rb'))
model = restore_model('distmult_model.pkl')
ls_series = pickle.load(open('./list_series.pkl', 'rb'))
actor = pickle.load(open('./actors2.pkl', 'rb'))
movies = pd.DataFrame({'id': list(movies_list.keys()), 'title': list(movies_list.values())})
graph = connect_db()
st.title('Showslens: Knowledge Graph for TV Shows')
st.markdown("""---""")
st.header('TV Series Recommendation')
selected_movie_name = st.selectbox('Select TV Series', movies['title'].values)
if st.button('Recommend'):
    L = recommend(selected_movie_name)
    st.write(L)
st.markdown("""---""")
st.header('Explore TV Shows')

g = sorted(['Thriller', 'Drama', 'Comedy', 'Crime', 'Fantasy', 'Documentary', 'Romance', 'Action', 'Adventure', 'Sci-Fi', 'Animation', 'Short', 'Horror', 'Family', 'Western', 'Mystery'])
genre = st.multiselect('Select a Genre', g)

actors = st.multiselect(
   'Select Actors',
   actor, max_selections = 3)

if st.button('Search'):
    query_db(graph)
