import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql
conn = pymysql.connect(user="root",
                       password="DB@1234",
                       host="localhost",
                       port=3306,
                       database = "new_nhl") 
cursor = conn.cursor()

with st.sidebar:
    selected = option_menu("NHL Analytics Hub", ["Home", 'Standings','Team Info','Player Details','Game Results','Leaderboards','SQL Query'], 
       icons=["shield-check"], menu_icon="shield-fill-check", default_index=0)
    
if selected == "Home":
    st.title(" NHL Analytics Hub")
    st.write(" Hockey Data Pipeline with SQL Analysis and Streamlit Dashboard")
    st.image("C:/Users/ADMIN/Desktop/NHL_Analytics_Hub/Hockey.jpg", width = 100)
    
    col1,col2,col3 = st.columns(3)
    with col1.container(border=True):
        teams_total = pd.read_sql("select count(*) as cnt from teams", con =conn)
        st.metric("Total_teams",teams_total.iloc[0,0])
    with col2.container(border=True):
        players_total = pd.read_sql("select count(*) as cnt from players", con =conn)
        st.metric("Total_Players",players_total.iloc[0,0])
    with col3.container(border=True):
        games_total = pd.read_sql("select count(*) as cnt from games", con =conn)
        st.metric("Total_games",games_total.iloc[0,0])

if selected == "Standings":
    st.subheader("Standings")
    option = st.selectbox(
    "Top 3 Teams",
    ("First",      
     "Second", 
     "Third"))
    if option == "First":
        df = pd.read_sql("select t.team_id,t.team_name, t.conference_name,st.wins,st.points,st.streak_count from teams t join standings st on t.team_id = st.team_id order by st.points desc limit 1 offset 0", con = conn)
        st.dataframe(df)
    if option == "Second":
        df = pd.read_sql("select t.team_id,t.team_name, t.conference_name,st.wins,st.points,st.streak_count from teams t join standings st on t.team_id = st.team_id order by st.points desc limit 1 offset 1", con = conn)
        st.dataframe(df)
    if option == "Third":
        df = pd.read_sql("select t.team_id,t.team_name, t.conference_name,st.wins,st.points,st.streak_count from teams t join standings st on t.team_id = st.team_id order by st.points desc limit 1 offset 2", con = conn)
        st.dataframe(df)   

if selected == "Team Info":
    st.subheader("Team Information")
    df = pd.read_sql("select team_abbrev,team_name,conference_name,division_name from teams", con = conn)
    st.dataframe(df)

if selected == "Player Details":
    st.subheader("Player Details")
    df = pd.read_sql("select team_id,first_name,last_name,position,jersey_number from players", con = conn)
    st.dataframe(df)

if selected == "Game Results":
    st.subheader("Game Info")
    option = st.radio(
    "Game Type",
    ("Home",      
     "Away"))
    if option == "Home":
        df = pd.read_sql("select t.team_name, t.conference_name, g.home_score,venue_name from teams t join games g on t.team_id = g.home_team_id", con = conn)
        st.dataframe(df)
    if option == "Away":
        df = pd.read_sql("select t.team_name, t.conference_name, g.away_score,venue_name from teams t join games g on t.team_id = g.away_team_id", con = conn)
        st.dataframe(df)

if selected == "Leaderboards":
    st.subheader("Top 10 Goals")
    df = pd.read_sql("select t.team_name,p.first_name,p.last_name,s.goals from skater_season_stats s join players p on s.player_id = p.player_id join teams t on s.team_id = t.team_id order by s.goals desc limit 10", con = conn)
    st.dataframe(df)
    
if selected == "SQL Query":
    option = st.selectbox(
    "Choose a Query",
    ("List of all Teams",      
     "Player counts Age wise", 
     "Home teams and their venues", 
     "Team wise goals data",
     "Player wise Top 10 penalties",
     "Russian Player Details",
     "Team wise Goalies Win-loss Data",
     "Position wise Skater Shots",
     "Country wise Height Weight of players",
     "Total streak counts",
     "Top 10 Teams",
     "Top Player per team",
     "Best performing teams",
     "Players contribution - Top 3 per team",
     "Goalie vs Team Performance"
    ))     
    if option == "List of all Teams":
        Query = "select team_name,conference_name,division_name from teams"
        st.text_area("SQL Query",Query,height = "content")
        if st.button("Run Query"):
            df = pd.read_sql("select team_name,conference_name,division_name from teams", con = conn)
            st.dataframe(df)
            
    if option == "Player counts Age wise":
        Query = "select count(*) as No_of_players, TIMESTAMPDIFF(year, birth_date, CURDATE()) as age,year(birth_date) as birth_year from players group by age,birth_year order by No_of_players Desc"
        st.text_area("SQL Query",Query,height = "content")
        if st.button("Run Query"):
            df = pd.read_sql("select count(*) as No_of_players, TIMESTAMPDIFF(year, birth_date, CURDATE()) as age,year(birth_date) as birth_year from players group by age,birth_year order by No_of_players Desc", con = conn)
            st.dataframe(df)
            
    if option == "Home teams and their venues":
        Query = "select t.team_abbrev,t.team_name, g.venue_name from teams t join games g on t.team_id = g.home_team_id"
        st.text_area("SQL Query",Query,height = "content")
        if st.button("Run Query"):
            df = pd.read_sql("select t.team_abbrev,t.team_name, g.venue_name from teams t join games g on t.team_id = g.home_team_id;", con = conn)
            st.dataframe(df)
            
    if option == "Team wise goals data":
         Query = "select t.team_abbrev, max(gs.goals) as Max_goals ,max(gs.assists) as Max_assists,max(gs.points) as Max_points from teams t join game_stats gs on t.team_id = gs.team_id group by t.team_id"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select t.team_abbrev, max(gs.goals) as Max_goals ,max(gs.assists) as Max_assists,max(gs.points) as Max_points from teams t join game_stats gs on t.team_id = gs.team_id group by t.team_id", con = conn)
            st.dataframe(df)
             
    if option == "Player wise Top 10 penalties":
         Query = "select p.first_name, p.last_name, max(gs.penalty_min) as Penalty from players p join game_stats gs on p.player_id = gs.player_id group by gs.player_id order by max(gs.penalty_min) desc limit 10"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select p.first_name, p.last_name, max(gs.penalty_min) as Penalty from players p join game_stats gs on p.player_id = gs.player_id group by gs.player_id order by max(gs.penalty_min) desc limit 10", con = conn)
            st.dataframe(df)
             
    if option == "Russian Player Details":
         Query = "select t.team_abbrev,p.first_name,p.last_name,p.birth_country from teams t join players p on p.team_id = t.team_id where birth_country = 'RUS'"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select t.team_abbrev,p.first_name,p.last_name,p.birth_country from teams t join players p on p.team_id = t.team_id where birth_country = 'RUS'", con = conn)
            st.dataframe(df)
             
    if option == "Team wise Goalies Win-loss Data":
         Query = "select gss.team_id as Team_id,t.team_abbrev as Team_Abbrev, sum(gss.games_played) as Total_games_played, sum(gss.wins) as Total_wins, sum(gss.losses) as Total_losses,sum(gss.ot_losses) as Total_ot_losses from goalie_season_stats gss join teams t on gss.team_id = t.team_id group by gss.team_id, t.team_abbrev"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select gss.team_id as Team_id,t.team_abbrev as Team_Abbrev, sum(gss.games_played) as Total_games_played, sum(gss.wins) as Total_wins, sum(gss.losses) as Total_losses,sum(gss.ot_losses) as Total_ot_losses from goalie_season_stats gss join teams t on gss.team_id = t.team_id group by gss.team_id, t.team_abbrev", con = conn)
            st.dataframe(df)
             
    if option == "Position wise Skater Shots":
         Query = "select p.position, avg(sss.shots) as Average_Shots from players p join skater_season_stats sss on p.player_id = sss.player_id group by p.position"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select p.position, avg(sss.shots) as Average_Shots from players p join skater_season_stats sss on p.player_id = sss.player_id group by p.position", con = conn)
            st.dataframe(df)
             
    if option == "Country wise Height Weight of players":
         Query = "select birth_country as Birth_Country, max(height_cm) as Max_height, min(height_cm) as Min_height,max(weight_kg) as Max_weight, , min(weight_kg) as Min_weight from players group by birth_country"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select birth_country as Birth_Country, max(height_cm) as Max_height, min(height_cm) as Min_height,max(weight_kg) as Max_weight, min(weight_kg) as Min_weight from players group by birth_country", con = conn)
            st.dataframe(df)
             
    if option == "Total streak counts":
         Query = "select streak_type,sum(streak_count) as Total_streak_count from standings group by streak_type"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select streak_type,sum(streak_count) as Total_streak_count from standings group by streak_type", con = conn)
            st.dataframe(df)
             
    if option == "Top 10 Teams":
         Query = "select t.team_name as Team_name, st.games_played as Games_Played, sum(st.goals_for) as Total_goals, sum(gs.goals) as Goals_per_game from teams t join standings st on st.team_id = t.team_id join game_stats gs on gs.team_id = st.team_id group by t.team_name, st.games_played order by total_goals desc limit 10"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select t.team_name as Team_name, st.games_played as Games_Played, sum(st.goals_for) as Total_goals, sum(gs.goals) as Goals_per_game from teams t join standings st on st.team_id = t.team_id join game_stats gs on gs.team_id = st.team_id group by t.team_name, st.games_played order by total_goals desc limit 10", con = conn)
            st.dataframe(df)
             
    if option == "Top Player per team":
         Query = "select * from (select gs.team_id as Team_id,t.team_name as Team_name, concat(p.first_name,p.last_name) as Player_name, sum(gs.goals) as Goals, sum(gs.assists) as Assists,sum(gs.points) as Points,row_number() over (partition by gs.team_id order by sum(gs.points) desc) as rn from players p join teams t on t.team_id = p.team_id join game_stats gs on gs.player_id = p.player_id group by Team_id,Team_name, Player_name) ranked where rn =1"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select * from (select gs.team_id as Team_id,t.team_name as Team_name, concat(p.first_name,p.last_name) as Player_name, sum(gs.goals) as Goals, sum(gs.assists) as Assists,sum(gs.points) as Points,row_number() over (partition by gs.team_id order by sum(gs.points) desc) as rn from players p join teams t on t.team_id = p.team_id join game_stats gs on gs.player_id = p.player_id group by Team_id,Team_name, Player_name) ranked where rn =1", con = conn)
            st.dataframe(df)
             
    if option == "Best performing teams":
         Query = "select t.team_name, st.wins, st.losses, st.points, st.goals_for, st.goals_against,((st.wins/st.games_played) * 100) as win_percentage, (st.goals_for - st.goals_against) as goal_diff from teams t join standings st on t.team_id = st.team_id where ((st.wins/st.games_played) * 100 > 60) and (st.goals_for - st.goals_against) > 0"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select t.team_name, st.wins, st.losses, st.points, st.goals_for, st.goals_against,((st.wins/st.games_played) * 100) as win_percentage,(st.goals_for - st.goals_against) as goal_diff from teams t join standings st on t.team_id = st.team_id where ((st.wins/st.games_played) * 100 > 60) and (st.goals_for - st.goals_against) > 0", con = conn)
            st.dataframe(df)
             
    if option == "Players contribution - Top 3 per team":
         Query = "select team_name, first_name, last_name, goals, goals_for, players_percentage from (select t.team_name, p.first_name,p.last_name,ss.goals, st.goals_for, round((ss.goals/st.goals_for) * 100,2) as players_percentage, row_number() over (partition by t.team_name order by ss.goals desc) as rn from teams t join standings st on t.team_id = st.team_id join players p on t.team_id = p.team_id join skater_season_stats ss on p.player_id = ss.player_id) ranked where rn < 4"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select team_name, first_name, last_name, goals, goals_for, players_percentage from (select t.team_name, p.first_name,p.last_name,ss.goals, st.goals_for, round((ss.goals/st.goals_for) * 100,2) as players_percentage, row_number() over (partition by t.team_name order by ss.goals desc) as rn from teams t join standings st on t.team_id = st.team_id join players p on t.team_id = p.team_id join skater_season_stats ss on p.player_id = ss.player_id) ranked where rn < 4", con = conn)
            st.dataframe(df)

    if option == "Goalie vs Team Performance":
         Query = "select Goalie_name, Team_name, Save_percent, Goalie_wins, Goalie_Losses, Team_points from (select concat(p.first_name,p.last_name) as Goalie_name, t.team_name as Team_name, round((gss.save_pct *100),2) as Save_percent, gss.wins as Goalie_wins, gss.losses as Goalie_Losses, st.points as Team_points, row_number() over (partition by t.team_name order by Save_pct desc) as rn from teams t join standings st on t.team_id = st.team_id join players p on t.team_id = p.team_id join goalie_season_stats gss on gss.player_id = p.player_id) ranked where rn = 1"
         st.text_area("SQL Query",Query,height = "content")
         if st.button("Run Query"):
            df = pd.read_sql("select Goalie_name, Team_name, Save_percent, Goalie_wins, Goalie_Losses, Team_points from (select concat(p.first_name,p.last_name) as Goalie_name, t.team_name as Team_name, round((gss.save_pct *100),2) as Save_percent, gss.wins as Goalie_wins, gss.losses as Goalie_Losses, st.points as Team_points, row_number() over (partition by t.team_name order by Save_pct desc) as rn from teams t join standings st on t.team_id = st.team_id join players p on t.team_id = p.team_id join goalie_season_stats gss on gss.player_id = p.player_id) ranked where rn = 1", con = conn)
            st.dataframe(df)