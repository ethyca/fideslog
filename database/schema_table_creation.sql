-- create the production schema and tables

use role event_writer;
use warehouse fides_log;
use database raw;

show schemas in database raw;

create schema if not exists fides;
use schema fides;

create sequence if not exists event_id_seq start = 1 increment = 1;

create table if not exists anonymous_usage_events (
  event_id integer,
  client_id varchar,
  product_name varchar,
  production_version varchar,
  os varchar,
  docker boolean,
  resource_counts varchar,
  event varchar,
  command varchar,
  flags varchar,
  endpoint varchar,
  status_code number,
  error varchar,
  local_host boolean,
  extra_data varchar,
  event_created_at timestamp_tz,
  event_loaded_at timestamp default sysdate() -- this is the utc timestamp
);

create sequence if not exists mapping_id_seq start = 1 increment = 1;

create table if not exists cli_api_mapping (
  id integer,
  api_id varchar,
  cli_id varchar,
  created_at timestamp_tz,
  updated_at timestamp_tz,
  constraint unique_api_cli_map unique (api_id, cli_id) not enforced 
);


show tables in schema raw.fides;

---------------------------------------------------
-- create the test schema and tables

-- instead of maintaining dualing ddl statements, copy the
-- production table structure. A second set of steps defines a
-- multi-step routine to backup test data, copy the production table
-- structure again, and restore test data to the recreated table

-- This should result in only the schema being changed when passing test events. 
---------------------------------------------------

-- initial schema and table creation

create schema if not exists fides_test;
use schema fides_test;

create sequence if not exists event_id_seq start = 1 increment = 1;

create or replace table raw.fides_test.anonymous_usage_events like raw.fides.anonymous_usage_events;

create sequence if not exists mapping_id_seq start = 1 increment = 1;

create or replace table raw.fides_test.cli_api_mapping like raw.fides.cli_api_mapping;


-- attempt to recreate the test table with any prod updates

-- -- create a backup of the test data
create or replace table raw.fides_test.anonymous_usage_events_bak clone raw.fides_test.anonymous_usage_events;
create or replace table raw.fides_test.cli_api_mapping_bak clone raw.fides_test.cli_api_mapping;

-- -- re-create an empty copy of the prod data table
create or replace table raw.fides_test.anonymous_usage_events like raw.fides.anonymous_usage_events;
create or replace table raw.fides_test.cli_api_mapping like raw.fides.cli_api_mapping;


-- -- attempt to reinsert the data from the test data backup to the replaced test table
insert into raw.fides_test.anonymous_usage_events
select * from raw.fides_test.anonymous_usage_events_bak;

insert into raw.fides_test.cli_api_mapping
select * from raw.fides_test.cli_api_mapping_bak;

-- -- clean up backup table (if successfuly reinserted)
drop table raw.fides_test.anonymous_usage_events_bak;
drop table raw.fides_test.cli_api_mapping_bak;
