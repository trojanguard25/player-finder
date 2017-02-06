delete from is_pitcher;

insert into is_pitcher (key_person, pitcher, hitter)
values ('d925a4af','Y','N');
insert into is_pitcher (key_person, pitcher, hitter)
values ('da772931','N','Y');
insert into is_pitcher (key_person, pitcher, hitter)
values ('87747efc','N','Y');
insert into is_pitcher (key_person, pitcher, hitter)
values ('0fc35bba','N','Y');

insert into is_pitcher
select
batter.key_person as key_person,
CASE 
   WHEN batter.pas < pitcher.bfs
               THEN 'Y' 
               ELSE 'N'
	END as pitcher,
CASE 
   WHEN batter.pas > pitcher.bfs
               THEN 'Y' 
               ELSE 'N'
	END as batter from 
(select b.pas as pas, c.key_person as key_person from chadwickbureau c 
join (select count(a.atbatID) as pas, a.batterID as id from mlb.atbats a where a.batterID <> 0 group by a.batterID) b
on c.key_mlbam = b.id) batter
 join
(select b.bfs as bfs, c.key_person as key_person from chadwickbureau c 
join (select count(a.atbatID) as bfs, a.pitcherID as id from mlb.atbats a where a.pitcherID <> 0 group by a.pitcherID) b
on c.key_mlbam = b.id) pitcher
on batter.key_person = pitcher.key_person;

insert into is_pitcher
select
batter.key_person as key_person,
#batter.pas, pitcher.bfs,
'N',
'Y' from 
(select b.pas as pas, c.key_person as key_person from chadwickbureau c 
join (select count(a.atbatID) as pas, a.batterID as id from mlb.atbats a where a.batterID <> 0 group by a.batterID) b
on c.key_mlbam = b.id) batter
left join
(select b.bfs as bfs, c.key_person as key_person from chadwickbureau c 
join (select count(a.atbatID) as bfs, a.pitcherID as id from mlb.atbats a where a.pitcherID <> 0 group by a.pitcherID) b
on c.key_mlbam = b.id) pitcher
on batter.key_person = pitcher.key_person
where pitcher.bfs IS NULL;

insert into is_pitcher
select
pitcher.key_person as key_person,
#batter.pas, pitcher.bfs,
'Y',
'N' from 
(select b.pas as pas, c.key_person as key_person from chadwickbureau c 
join (select count(a.atbatID) as pas, a.batterID as id from mlb.atbats a where a.batterID <> 0 group by a.batterID) b
on c.key_mlbam = b.id) batter
right join
(select b.bfs as bfs, c.key_person as key_person from chadwickbureau c 
join (select count(a.atbatID) as bfs, a.pitcherID as id from mlb.atbats a where a.pitcherID <> 0 group by a.pitcherID) b
on c.key_mlbam = b.id) pitcher
on batter.key_person = pitcher.key_person
where batter.pas IS NULL;

