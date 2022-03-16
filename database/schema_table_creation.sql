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

-- instead of maintaining dualing ddl statements,
-- uses cloning to create copy of the structure and data in a test schema

-- This should result in only the schema being changed when passing test events. 

-- TODO: create a task to execute the clone on some regular cadence
---------------------------------------------------

create or replace schema fides_test clone fides;

show tables in schema raw.fides_test;
