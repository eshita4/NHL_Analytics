 /* Top 3 teams */
 select t.division_name, sum(st.wins), sum(st.losses), sum(st.points)
 from teams t join standings st 
 on t.team_id = st.team_id group by t.division_name;
 
 /*List of all Teams*/
 select team_name,conference_name,division_name from teams;
 
 /*Player count Age wise */
 select count(*) as No_of_players, TIMESTAMPDIFF(year, birth_date, CURDATE()) as age,year(birth_date) as birth_year
 from players group by age,birth_year order by No_of_players Desc;
 
 /*Home teams and their venues*/
 select t.team_abbrev,t.team_name, g.venue_name from teams t join games g on t.team_id = g.home_team_id;
 
 /* Team wise goals data*/
 select t.team_abbrev, max(gs.goals) as Max_goals ,max(gs.assists) as Max_assists,max(gs.points) as Max_points
 from teams t join game_stats gs 
 on t.team_id = gs.team_id group by t.team_id;
 
 /* Player wise Top 10 penalties*/
 select p.first_name, p.last_name, max(gs.penalty_min) as Penalty 
 from players p join game_stats gs on p.player_id = gs.player_id 
 group by gs.player_id order by max(gs.penalty_min) desc limit 10;
 
 /*Russian Player Details*/
 select t.team_abbrev,p.first_name,p.last_name,p.birth_country from teams t join players p on p.team_id = t.team_id 
 where birth_country = 'RUS';
 
 /*Team wise Goalies Win-loss Data */
 select gss.team_id as Team_id,t.team_abbrev as Team_Abbrev, sum(gss.games_played) as Total_games_played, 
 sum(gss.wins) as Total_wins, sum(gss.losses) as Total_losses,  sum(gss.ot_losses) as Total_ot_losses
 from goalie_season_stats gss
 join teams t on gss.team_id = t.team_id
 group by gss.team_id, t.team_abbrev;
 
 /* Position wise Skater Shots*/
 select p.position, avg(sss.shots) as Average_Shots 
 from players p join skater_season_stats sss 
 on p.player_id = sss.player_id group by p.position;
 select streak_type,sum(streak_count) as Total_streak_count from standings group by streak_type;
 
 /*Country wise Height Weight of players*/
 select birth_country as Birth_Country, max(height_cm) as Max_height, max(weight_kg) as Max_weight, min(height_cm) as Min_height, min(weight_kg) as Min_weight 
 from players group by birth_country;

/* Total streak counts*/
select streak_type,sum(streak_count) as Total_streak_count from standings group by streak_type;

 /* Top 10 Teams*/
 select t.team_name as Team_name, st.games_played as Games_Played, sum(st.goals_for) as Total_goals, sum(gs.goals) as Goals_per_game
  from teams t
  join standings st on st.team_id = t.team_id
  join game_stats gs on gs.team_id = st.team_id
  group by t.team_name, st.games_played
  order by total_goals desc limit 10;
  
 /* Top Player per team */
  select * from
  (select gs.team_id as Team_id,t.team_name as Team_name, concat(p.first_name,p.last_name) as Player_name, 
  sum(gs.goals) as Goals, sum(gs.assists) as Assists,  sum(gs.points) as Points, 
  row_number() over 
  (partition by gs.team_id 
  order by sum(gs.points) desc) as rn
  from players p 
  join teams t on t.team_id = p.team_id 
  join game_stats gs on gs.player_id = p.player_id 
  group by Team_id,Team_name, Player_name) ranked
  where rn =1;
  
/* Best performing teams with win percentage > 60 and positive goals*/
select t.team_name, st.wins, st.losses, st.points, st.goals_for,
st.goals_against, ((st.wins/st.games_played) * 100) as winning_percentage,
(st.goals_for - st.goals_against) as goal_difference
from teams t join standings st on t.team_id = st.team_id 
where ((st.wins/st.games_played) * 100 > 60) and (st.goals_for - st.goals_against) > 0;

/* Players contribution - Top 3 per team*/
select team_name, first_name, last_name, goals, goals_for, players_percentage from 
(select t.team_name, p.first_name,p.last_name,ss.goals, st.goals_for, round((ss.goals/st.goals_for) * 100,2) as players_percentage,
 row_number() over (
  partition by t.team_name
  order by ss.goals desc) as rn
 from teams t join standings st on t.team_id = st.team_id
 join players p on t.team_id = p.team_id
 join skater_season_stats ss on p.player_id = ss.player_id) ranked
 where rn < 4;
 
 /* Goalie vs Team Performance*/
 select Goalie_name, Team_name, Save_percent, Goalie_wins, Goalie_Losses, Team_points from
 (select concat(p.first_name,p.last_name) as Goalie_name, t.team_name as Team_name, 
 round((gss.save_pct *100),2) as Save_percent,
 gss.wins as Goalie_wins, gss.losses as Goalie_Losses, st.points as Team_points,
 row_number() over (partition by t.team_name order by Save_pct desc) as rn 
 from teams t join standings st on t.team_id = st.team_id 
 join players p on t.team_id = p.team_id 
 join goalie_season_stats gss on gss.player_id = p.player_id) ranked
 where rn = 1;