-- create the schema and table

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
  resource_counts object,
  event varchar,
  command varchar,
  flags array,
  endpoint varchar,
  status_code number,
  error varchar,
  local_host boolean,
  extra_data object,
  event_created_at timestamp_tz,
  event_loaded_at timestamp default sysdate() -- this is the utc timestamp
);

create sequence if not exists keys_id_seq start = 1 increment = 1;

create table if not exists api_keys (
  id integer,
  api_key varchar,
  client_id varchar,
  created_at timestamp_tz,
  expired_at timestamp_tz
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
