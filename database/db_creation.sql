//create the database, role, and warehouse

use role accountadmin;
create database if not exists raw;
create warehouse if not exists fides_log;

use role securityadmin;

create role if not exists fides_log;


//add a user for fideslog

create user fides_log password=******************* default_role=fides_log default_warehouse=fides_log default_namespace='raw'; -- replace the asterisks with an appropriate password

// grants for role and user (I know I am forgetting some here...)

grant usage on warehouse fides_log to role fides_log;

grant usage, create schema, monitor on database raw to role fides_log;

grant usage on future schemas in database raw to role fides_log;

grant role fides_log to role sysadmin;

grant role fides_log to user fides_log;

// create the schema and table

use role fides_log;
use warehouse fides_log;
use database raw;

show schemas in database raw;

create schema fides;
use schema fides;

create table anonymous_usage_events (
  event_id number autoincrement start 1 increment 1,
  client_id varchar,
  product_name varchar,
  production_version varchar,
  event varchar,
  cli_command varchar,
  cli_flags array, -- unsure on if we want to use this or not
  endpoint varchar,
  status_code number,
  manifests variant,
  local boolean,
  os varchar,
  docker boolean,
  event_created_at timestamp_tz,
  event_loaded_at timestamp default sysdate() // this is the utc timestamp
);
