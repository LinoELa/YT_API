import streamlit as st 
import pandas as pd 
from googleapiclient.discovery import build


# Configuracion de la pantalla 
st.set_page_config(page_title="Software Analítico", layout="wide")


# Funcio Prueba 
def pagina_principal():
    st.title("Pagina Princpal")
    st.write("Bienvenido a la pagina princial")
    st.write("Usa el menu del la izquieda para ver a mas youtuber")


# sidebar
st.sidebar.title("ELIGUE UN CANAL")

# Titulo
st.title("Software Analítico :red[YouTube API] - :blue[Canales:]  Ibai -  Paulino - AuronPlay")
st.subheader("* NOTA * *Toda la* ***Informacion*** *de este software analítico es en tiempo real*", divider=True)


# Id y Nombre de casa pagina
pagina = st.sidebar.selectbox("Canal : Ibai - AuronPlay - Paulino ",["Paulino", "Ibai","AuronPlay"] )




# ---------------------PAULINO------------------------
def stream_lino():
     # Set page config
    # st.set_page_config(page_title="Streamlit YouTube Channel Dashboard", layout="wide")

    def load_data():
        data = pd.read_csv("./YTEla.csv")

        # ----------------------

        # data['DATE'] = data['DATE'].dt.strftime('%d-%m-%Y')

        data['DATE'] = pd.to_datetime(data['DATE'])

        data.WATCH_HOURS = data.WATCH_HOURS.fillna(0)
        data.WATCH_HOURS = data.WATCH_HOURS.astype(int)
        
        # ----------------------


        data['NET_SUBSCRIBERS'] = data['SUBSCRIBERS_GAINED'] - data['SUBSCRIBERS_LOST']
        return data

    df = load_data()

    # Original
    df1 = df[['DATE', 'NET_SUBSCRIBERS', 'VIEWS', 'WATCH_HOURS', 'LIKES']]

    # Calculate row-wise Acumulado sum
    df2 = df1.copy()

    for column in ['NET_SUBSCRIBERS', 'VIEWS', 'WATCH_HOURS', 'LIKES']:
        df2[column] = df2[column].cumsum()

    def format_with_commas(number):
        return f"{number:,}"
 

    logo_icon = "images/streamlit-mark-color.png"
    logo_image = "images/streamlit-logo-primary-colormark-lighttext.png"
    st.logo(icon_image=logo_icon, image=logo_image)

    with st.sidebar:
        st.header("⚙️ Configuraciones⚙️ ")
        start_date = st.date_input("Fecha inicial", df['DATE'].min())
        end_date = st.date_input("Fecha final", df['DATE'].max())

        time_frame = st.selectbox(
            "Seleccione el periodo",
            ("Diario", "Acumulado"),
        )


    # Titulo - Display key metrics (Total) 
    st.subheader(":blue[YT Paulino Salvador E.]")

    st.caption("Estadísticas de todos los tiempos")

    col = st.columns(3)
    with col[0]:
        with st.container(border=True):
            st.metric("Total Subscriptores: Ganados + Perdidos", format_with_commas((df['SUBSCRIBERS_GAINED'].sum() - df['SUBSCRIBERS_LOST'].sum())))
            if time_frame == 'Diario':
                df_subscribers = df1[["DATE", "NET_SUBSCRIBERS"]].set_index(df1.columns[0])
                st.area_chart(df_subscribers, color='#29b5e8', height=150)
                
            if time_frame == 'Acumulado':
                df_subscribers = df2[["DATE", "NET_SUBSCRIBERS"]].set_index(df2.columns[0])
                st.area_chart(df_subscribers, color='#29b5e8', height=150)

    with col[1]:
        with st.container(border=True):
            st.metric("Total visualizaciones", format_with_commas(df['VIEWS'].sum()))

            if time_frame == 'Diario':
                df_views = df1[["DATE", "VIEWS"]].set_index(df1.columns[0])
                st.area_chart(df_views, color='#FF9F36', height=150)

            if time_frame == 'Acumulado':
                df_views = df2[["DATE", "VIEWS"]].set_index(df2.columns[0])
                st.area_chart(df_views, color='#FF9F36', height=150)
            
    with col[2]:
        with st.container(border=True):
            st.metric("Total Me gustas", format_with_commas(df['LIKES'].sum()))

            if time_frame == 'Diario':
                df_views = df1[["DATE", "LIKES"]].set_index(df1.columns[0])
                st.area_chart(df_views, color='#7D44CF', height=150)
                
            if time_frame == 'Acumulado':
                df_views = df2[["DATE", "LIKES"]].set_index(df2.columns[0])
                st.area_chart(df_views, color='#7D44CF', height=150)

    # with col[3]:
    #     with st.container(border=True):
    #         st.metric("Tiempo total futuro de visualización", format_with_commas((df['WATCH_HOURS'].sum())))

    #         if time_frame == 'Diario':
    #             df_views = df1[["DATE", "WATCH_HOURS"]].set_index(df1.columns[0])
    #             st.area_chart(df_views, color='#D45B90', height=150)

    #         if time_frame == 'Acumulado':
    #             df_views = df2[["DATE", "WATCH_HOURS"]].set_index(df2.columns[0])
    #             st.area_chart(df_views, color='#D45B90', height=150)

    


    # Seleccione la duración
    st.caption("Seleccione la duración")

    if time_frame == 'Diario':
        mask = (df1['DATE'].dt.date >= start_date) & (df1['DATE'].dt.date <= end_date)
        filtered_df = df1.loc[mask]
        
    if time_frame == 'Acumulado':
        mask = (df2['DATE'].dt.date >= start_date) & (df2['DATE'].dt.date <= end_date)
        filtered_df = df2.loc[mask]

    cols = st.columns(3)
    with cols[0]:
        with st.container(border=True):
            st.metric("Subsciptores - Ultimos 7 Meses", format_with_commas(filtered_df['NET_SUBSCRIBERS'].sum()))

            df_subscribers_duration = filtered_df[["DATE", "NET_SUBSCRIBERS"]].set_index(filtered_df.columns[0])
            st.area_chart(df_subscribers_duration, color='#7D44CF', height=150)

    with cols[1]:
        with st.container(border=True):
            st.metric("Visualizaciones - Ultimo 7 Meses", format_with_commas(filtered_df['VIEWS'].sum()))

            df_views_duration = filtered_df[["DATE", "VIEWS"]].set_index(filtered_df.columns[0])
            st.area_chart(df_views_duration, color='#D45B90', height=150)

    with cols[2]:
        with st.container(border=True):
            st.metric("Me Gusta - Ultimos 7 Meses", format_with_commas(filtered_df['LIKES'].sum()))

            df_likes_duration = filtered_df[["DATE", "LIKES"]].set_index(filtered_df.columns[0])
            st.area_chart(df_likes_duration, color='#29b5e8', height=150)

    # Cuadro de Mandos - DataFrame

    st.subheader("Todos los Datos")
    st.dataframe(df)



if pagina == "Paulino":
    stream_lino()

# --------------------- IBAI --------------------

elif pagina == 'Ibai':

    def ibai_streamlit():
        # Configuración de la API de YouTube
        API_KEY = "AIzaSyDvZHKzCxTayMVbJzAsPuzfyvyZdxTSPEc"  # Reemplaza con tu clave de la API de YouTube
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        # ID del canal de Ibai
        channel_id = "UCaY_-ksFSQtTGk0y1HA_3YQ"

        # Función para obtener detalles del canal
        def get_channel_details(youtube, channel_id):
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=channel_id
            )
            response = request.execute()

            item = response["items"][0]
            channel_data = {
                "Nombre del Canal": item["snippet"]["title"],
                "ID del Canal": item["id"],
                "Suscriptores": int(item["statistics"].get("subscriberCount", 0)),
                "Visualizaciones Totales": int(item["statistics"].get("viewCount", 0)),
                "Cantidad de Videos": int(item["statistics"].get("videoCount", 0)),
            }
            return pd.DataFrame([channel_data])

        # Función para obtener datos de videos recientes
        def get_videos(youtube, playlist_id):
            videos = []
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=10
            )
            response = request.execute()

            for item in response["items"]:
                video_id = item["contentDetails"]["videoId"]
                video_details = get_video_details(youtube, video_id)
                videos.append(video_details)

            return pd.DataFrame(videos)

        # Función para obtener detalles de un video
        def get_video_details(youtube, video_id):
            request = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            item = response["items"][0]

            return {
                "Título del Video": item["snippet"]["title"],
                "Fecha de Subida": item["snippet"]["publishedAt"],
                "Visualizaciones": int(item["statistics"].get("viewCount", 0)),
                "Comentarios": int(item["statistics"].get("commentCount", 0)),
            }


        # Titulo - Display key metrics (Total) 
        st.subheader(":blue[YT Ibai Llanos]")


        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

        # Obtener detalles del canal
        #st.subheader("Información Principal de Canal de Ibai")
        channel_data = get_channel_details(youtube, channel_id)
        st.dataframe(channel_data)

        # Obtener la lista de reproducción de subidas
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Obtener datos de videos recientes
        st.subheader("Info 10 Videos mas Recientes de AuronPlay")


        videos_data = get_videos(youtube, playlist_id)
        st.dataframe(videos_data)

        # Visualización de estadísticas
        st.subheader("Visualización - Videos ")
        st.bar_chart(videos_data.set_index("Título del Video")[["Visualizaciones", "Videos"]])

        # DataFrame Completo 
        
        # Visualización de estadísticas
        st.subheader("Full Informacion")
        st.dataframe(channel_data)

    # Llamar a la función principal
    # if __name__ == "__main__":
    ibai_streamlit()

# --------------------------------- Auron Play

elif pagina == 'AuronPlay':

    def auron_streamlit():
        # Configuración de la API de YouTube
        API_KEY = "AIzaSyDvZHKzCxTayMVbJzAsPuzfyvyZdxTSPEc"  # Reemplaza con tu clave de la API de YouTube
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        # ID del canal de AuronPlay
        channel_id = "UCyQqzYXQBUWgBTn4pw_fFSQ"
        

        # Función para obtener detalles del canal
        def get_channel_details(youtube, channel_id):
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=channel_id
            )
            response = request.execute()

            item = response["items"][0]
            channel_data = {
                "Nombre del Canal": item["snippet"]["title"],
                "ID del Canal": item["id"],
                "Suscriptores": int(item["statistics"].get("subscriberCount", 0)),
                "Visualizaciones Totales": int(item["statistics"].get("viewCount", 0)),
                "Cantidad de Videos": int(item["statistics"].get("videoCount", 0)),
            }
            return pd.DataFrame([channel_data])

        # Función para obtener datos de videos recientes
        def get_videos(youtube, playlist_id):
            videos = []
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=10
            )
            response = request.execute()

            for item in response["items"]:
                video_id = item["contentDetails"]["videoId"]
                video_details = get_video_details(youtube, video_id)
                videos.append(video_details)

            return pd.DataFrame(videos)

        # Función para obtener detalles de un video
        def get_video_details(youtube, video_id):
            request = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            item = response["items"][0]

            return {
                "Título del Video": item["snippet"]["title"],
                "Fecha de Subida": item["snippet"]["publishedAt"],
                "Visualizaciones": int(item["statistics"].get("viewCount", 0)),
                "Comentarios": int(item["statistics"].get("commentCount", 0)),
            }

        # Configuración principal de la app
        
        # Titulo 
        st.subheader(":blue[YT Auron Play]")


        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

        # Obtener detalles del canal
       #st.subheader("Información Principal de Canal de AuronPlay")
        channel_data = get_channel_details(youtube, channel_id)
        st.dataframe(channel_data)

        # Obtener la lista de reproducción de subidas
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Obtener datos de videos recientes
        st.subheader("Info 10 Videos mas Recientes de AuronPlay")
        videos_data = get_videos(youtube, playlist_id)
        st.dataframe(videos_data)

        # Visualización de estadísticas
        st.subheader("Visualizació")
        st.bar_chart(videos_data.set_index("Título del Video")[["Videos", "Visualización"]])

        # DataFrame Completo 
        
        # Visualización de estadísticas
        st.subheader("Full Informacion")
        st.dataframe(channel_data)


    
        

    # Llamar a la función principal
    # if __name__ == "__main__":
    auron_streamlit()





# Error 
st.subheader("", divider=True)
st.subheader("* NOTA * *En caso de error, seria por haber alcanzado el limite diario de solicitudes a API de YouTube, que son :  10.000/dia*", divider=True)
