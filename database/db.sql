create table tcontractor
(id serial primary key
    , name varchar(255)
    , inn bigint
    , kpp bigint
    , address varchar(200)
    , description text
    , created timestamp default now()
    , modified timestamp default now()
    , deleted timestamp);


create table tzonetype
(id serial primary key, name varchar(50), description text);

insert into tzonetype(id, name) values (4,'Город'), (3,'Регион');

create table tzone
(id serial primary key
    , parent_id bigint constraint fk_zone_parent references tzone
    , zonetype_id bigint constraint fk_zone_type references tzonetype
    , name varchar(50)
    , address varchar(500)
    , description text
    , nw_latitude decimal
    , nw_longitude decimal
    , se_latitude decimal
    , se_longitude decimal
    );

insert into tzone (id, zonetype_id, name) values (1,3,'Татарстан');
insert into tzone (id, parent_id, name, zonetype_id) values
(2,1,'Набережные Челны, город',4),
(3,1,'Нижнекамск, город',4),
(4,1,'Альметьевск, город',4),
(5,1,'Зеленодольск, город',4),
(6,1,'Бугульма, город',4),
(7,1,'Елабуга, город',4),
(8,1,'Лениногорск, город',4),
(9,1,'Чистополь, город',4),
(10,1,'Заинск, город',4),
(11,1,'Азнакаево, город',4),
(12,1,'Нурлат, город',4),
(13,1,'Бавлы, город',4),
(14,1,'Менделеевск, город',4),
(15,1,'Буинск, город',4),
(16,1,'Агрыз, город',4),
(17,1,'Арск, город',4),
(18,1,'Мензелинск, город',4),
(19,1,'Мамадыш, город',4),
(20,1,'Тетюши, город',4),
(21,1,'Болгар, город',4),
(22,1,'Лаишево, город',4),
(23,1,'Иннополис, город',4);

insert into tzone (id, parent_id, zonetype_id, name, address,  nw_latitude, nw_longitude, se_latitude, se_longitude)  values (24, 1, 4, 'Казань', 'Казань', 49.062329, 55.835212,49.263752, 55.732721);

update tcontract set zone_id=24;

drop table if exists tcontract cascade ;

create table tcontract
(id serial primary key
    , name varchar(255)
    , numb varchar(255) unique
    , contract_date date
    , zone_id bigint constraint fk_contract_zone references tzone
    , main_contractor_id bigint constraint fk_contract_main_contractor references tcontractor
    , sub_contractor_id bigint constraint fk_contract_sub_contractor references tcontractor
    , address varchar(500)
    , description text
    , total_price decimal
    , contract_end date
    , responsible_user_id bigint
    , start_date timestamp
    , finish_date timestamp
    , created timestamp default now()
    , modified timestamp default now()
    , deleted timestamp);

drop table if exists tcontractobject cascade ;

create table tcontractobject
(id serial primary key
    , contract_id bigint constraint fk_contract_object references tcontract
    , contractor_id bigint constraint fk_contract_main_contractor references tcontractor
    , zone_id bigint constraint fk_contractobject_zone references tzone
    , from_latitude decimal
    , from_longitude decimal
    , to_latitude decimal
    , to_longitude decimal
    , price decimal
    , start_date timestamp
    , finish_date timestamp
    , created timestamp default now()
    , modified timestamp default now()
    , deleted timestamp);

drop table tobjectprogress cascade ;

create table tobjectprogress
(id serial primary key
    , contract_id bigint constraint fk_progress_contract references tcontract
    , contractobject_id bigint constraint fk_progress_object references tcontractobject
    , contractor_id bigint constraint fk_progress_contractor references tcontractor
    , from_latitude decimal
    , from_longitude decimal
    , to_latitude decimal
    , to_longitude decimal
    , price decimal
    , start_date timestamp
    , finish_date timestamp
    , created timestamp default now()
    , modified timestamp default now()
    , deleted timestamp);

alter table tobjectprogress add column description text;

select * from generate_series(1,10);

create function random_number(integer) returns text security definer language sql as $$
SELECT array_to_string( ARRAY ( SELECT substring('1234567890' FROM least(greatest((random()*10)::int,1),10) FOR 1) FROM generate_series(1,$1) ), '' )
$$;

create function random_value(integer) returns integer security definer language sql as $$ select least(greatest((random()*$1)::int,1),$1) $$;

select least(greatest((random()*23)::int,1),23);

insert into tcontractor(id, name, inn, kpp, address)
select generate_series, 'Подрядчик '||generate_series, 1650e8+random_number(8)::bigint, 165001001,'Улица Мира д '||random_number(1) from generate_series(5,15);

truncate table tcontract;

insert into tcontract (id, name, numb, contract_date, zone_id, main_contractor_id, sub_contractor_id, address, total_price)
select generate_series, 'Контракт '||generate_series, generate_series, now() - random_number(2)::int*interval '1 month', random_value(23), random_value(15),
       random_value(15), 'Улица Мира д '||random_number(1), random_value(40)*1000 from generate_series(1,100);

select random(), random();

insert into tcontractobject (contract_id, contractor_id, zone_id, from_latitude, from_longitude, to_latitude, to_longitude, price, start_date, finish_date)
select id, contractor_id, zone_id, lat, lon, lat+random()/1000, lon-random()/1000, total_price/2, contract_date+random_value(10)*interval '1 day', contract_date+30+random_value(10) from
    (select c.id, case when random()<0.5 then main_contractor_id else sub_contractor_id end contractor_id, zone_id, coalesce(total_price,2000) total_price, contract_date
          , nw_latitude+(se_latitude-nw_latitude)*random() lat, nw_longitude-(nw_longitude-se_longitude)*random() lon
            from tcontract c, tzone z where z.id=c.zone_id) a;

insert into tcontractobject (contract_id, contractor_id, zone_id, from_latitude, from_longitude, to_latitude, to_longitude, price, start_date, finish_date)
select contract_id, contractor_id, zone_id, to_latitude, to_longitude, to_latitude-random()/1000, to_longitude+random()/1000,  price, finish_date, finish_date+(30+random_value(10))*interval '1 day'from tcontractobject;

insert into tobjectprogress (contract_id, contractobject_id, contractor_id, from_latitude, from_longitude, to_latitude,  to_longitude, price, start_date, finish_date)
select contract_id, id, contractor_id, from_latitude, from_longitude, (from_latitude+to_latitude)/2, (from_longitude+to_longitude)/2, price/2, start_date, start_date+(finish_date-start_date)/2 from tcontractobject;

update tcontract c set start_date=o.start_date, finish_date=o.finish_date from (select contract_id, min(start_date) start_date, max(finish_date) finish_date from tcontractobject group by contract_id)
    o where o.contract_id=c.id;

create or replace function func_home(phash text, pdata json) returns json security definer language plpgsql as $$
declare vRes json := '[{ "lat": 55.796289, "lng": 49.108795, "name": "Самый лучший объект", "zone": "Татарстан, г. Казань" }]';
begin
    select json_object_agg(key,value) into vRes from (
        with dta as (select count(distinct contract_id) contracts, count(1) objects, sum(price) total_price from tcontractobject)
        select 'in_progress' as key, json_agg(row_to_json(r)) as value from (select round(avg(from_latitude),5) lat, round(avg(to_longitude),5) lon, c.name, p.name||','||z.name as zone
        from tcontract c, tcontractobject o, tzone z, tzone p where c.start_date<=now() and c.finish_date>now() and c.id=o.contract_id and c.zone_id=z.id and z.parent_id=p.id group by  c.name, p.name, z.name) r
        union all select 'total_contracts', to_json(contracts) from dta
        union all select 'total_objects', to_json(objects) from dta
        union all select 'total_price', to_json(total_price) from dta
    ) c;
    return vRes;
end
$$;

drop view if exists vcontractors_total;

create or replace view vcontractors_total as
select row_number() over () id, case when grouping(o.name)=1 then 'ВСЕГО' else o.name end
     , case when grouping(o.name)=1 then 'по системе' when grouping(to_char(c.contract_date,'yyyy'))=1 then 'Итого '||o.name else to_char(c.contract_date,'yyyy') end as year
     --, case when grouping(o.name)=1 then 'по системе' when grouping(to_char(c.contract_date,'TMMonth yyyy'))=1 then 'Итого '||o.name else to_char(c.contract_date,'TMMonth yyyy') end as month
     , count(1) contracts_cnt, sum(c.total_price) contracts_price
    , count(case when now()>=c.start_date and now()<coalesce(c.finish_date,now()+interval '1 sec') then 1 end) contracts_active
     , sum(case when now()>=c.start_date and now()<c.finish_date then c.total_price end) contracts_active_price
    , sum(j.cnt) objects_cnt, sum(j.active_cnt) objects_active, sum(j.progress)/sum(j.price) objects_progress, null accidents_month
    from tcontractor o, tcontract c left join (select contract_id, count(1) cnt, sum(o.price) price, sum(p.price) progress
    , count(case when now()>=start_date and now()<coalesce(finish_date,now()+interval '1 sec') then 1 end) active_cnt from
        tcontractobject o left join (select contractobject_id, sum(price) price from tobjectprogress group by 1) p on p.contractobject_id=o.id group by 1) j on j.contract_id=c.id
    where c.main_contractor_id=o.id group by rollup (o.name, to_char(c.contract_date,'yyyy'));

create or replace view vzones_total as
select row_number() over () id, case when grouping(z.name)=1 then 'ВСЕГО' else z.name end
     , case when grouping(z.name)=1 then 'по системе' when grouping(to_char(c.contract_date,'yyyy'))=1 then 'Итого '||z.name else to_char(c.contract_date,'yyyy') end as year
     --, case when grouping(o.name)=1 then 'по системе' when grouping(to_char(c.contract_date,'TMMonth yyyy'))=1 then 'Итого '||o.name else to_char(c.contract_date,'TMMonth yyyy') end as month
     , count(1) contracts_cnt, sum(c.total_price) contracts_price
    , count(case when now()>=c.start_date and now()<coalesce(c.finish_date,now()+interval '1 sec') then 1 end) contracts_active
     , sum(case when now()>=c.start_date and now()<c.finish_date then c.total_price end) contracts_active_price
    , sum(j.cnt) objects_cnt, sum(j.active_cnt) objects_active, sum(j.progress)/sum(j.price) objects_progress, null accidents_month
    from tzone z, tcontract c left join (select contract_id, count(1) cnt, sum(o.price) price, sum(p.price) progress
    , count(case when now()>=start_date and now()<coalesce(finish_date,now()+interval '1 sec') then 1 end) active_cnt from
        tcontractobject o left join (select contractobject_id, sum(price) price from tobjectprogress group by 1) p on p.contractobject_id=o.id group by 1) j on j.contract_id=c.id
    where c.zone_id=z.id group by rollup (z.name, to_char(c.contract_date,'yyyy'));

drop view if exists vcontract_objects;

create or replace view v_object_progress as
    select row_number() over () id
    , to_char(c.contract_date,'yyyy') as year
    , to_char(c.contract_date,'TMMonth yyyy') as month
    , o.contract_id
    , o.contractor_id
    , c.zone_id
    , p.price
    , p.price finished_price
    , p.price/o.price progress
    , p.cnt finished_count
    , o.start_date
    , o.finish_date
from tcontractobject o, (select contractobject_id, sum(price) price, count(1) cnt from tobjectprogress group by 1) p, tcontract c
        where o.contractor_id is not null and p.contractobject_id=o.id and o.contract_id=c.id  and c.start_date<=now() and coalesce(c.finish_date,now()+interval '1 min') > now();


create or replace function func_done(phash text, pdata json) returns json security definer language plpgsql as $$
declare vRes json := '{"ok": true}';
begin
    with dta as (select conid, xstart, ystart, xstop, ystop, price, description from json_to_record(pdata)
        as x (conid int, xstart decimal, ystart decimal, xstop decimal, ystop decimal, price decimal, description text))
    insert into tobjectprogress (contract_id, contractobject_id, contractor_id, from_latitude, from_longitude, to_latitude, to_longitude, price, description, finish_date)
    select c.id, o.id, o.contractor_id, d.xstart, d.ystart, d.xstop, d.ystop, d.price, d.description, now() from dta d, tcontractobject o, tcontract c
        where o.id=d.conid and o.contract_id=c.id and not exists
        (select 1 from tobjectprogress p where p.contractobject_id=o.id and p.from_latitude=d.xstart and p.from_longitude=d.ystart);
    return vRes;
end
$$;
