-- create the database, role, and warehouse

use role accountadmin;
create database if not exists raw;
create warehouse if not exists fides_log;

use role securityadmin;

create role if not exists event_writer;


-- add a user for fideslog

create user fides_tool password=******************* default_role=event_writer default_warehouse=fides_log default_namespace='raw'; -- replace the asterisks with an appropriate password

-- grants for role and user

grant usage on warehouse fides_log to role event_writer;

grant usage, create schema, monitor on database raw to role event_writer;

grant usage on future schemas in database raw to role event_writer;

grant role event_writer to role sysadmin;

grant role event_writer to user fides_tool;
