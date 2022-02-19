-- create the database, role, and warehouse

use role accountadmin;
create database if not exists raw;
create warehouse if not exists fides_log;

use role securityadmin;

create role if not exists event_writer;


-- add a user for fideslog

create user event_writer password=******************* default_role=event_writer default_warehouse=fides_log default_namespace='raw'; -- replace the asterisks with an appropriate password

-- grants for role and user

grant usage on warehouse fides_log to role event_writer;

grant usage, create schema, monitor on database raw to role event_writer;

grant usage on future schemas in database raw to role event_writer;

grant role event_writer to role sysadmin;

grant role event_writer to user event_writer;

-- create the schema and table

use role event_writer;
use warehouse fides_log;
use database raw;

show schemas in database raw;

create schema if not exists fides;
use schema fides;

create table if not exists anonymous_usage_events (
  event_id number autoincrement start 1 increment 1,
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

create table if not exists api_keys (
  api_key varchar,
  client_id varchar,
  created_at timestamp_tz,
  expired_at timestamp_tz
)

create table if not exists cli_api_mapping (
  id number autoincrement start 1 increment 1,
  api_id varchar,
  cli_id varchar,
  created_at timestamp_tz,
  updated_at timestamp_tz,
  constraint unique_api_cli_map unique (api_id, cli_id) not enforced 
)


show tables in schema raw.fides;


-- downgrade, destroy, etc.

/*
use role accountadmin;
-- drop warehouse fides_log;
drop database raw;
use role securityadmin;
drop role fides_log;
drop user fides_log;
*/
