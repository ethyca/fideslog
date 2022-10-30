# Fideslog: Privacy-Respecting Usage Analytics

_A part of the [greater Fides ecosystem](https://github.com/ethyca/fides)._

[![Latest Release Version][release-image]][release-url]
[![Latest Deployment][deploy-image]][actions-url]
[![License][license-image]][license-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![Twitter][twitter-image]][twitter-url]

![Fideslog banner](./assets/fideslog.png "Fideslog banner")

## Overview

Fideslog is the [API server](./fideslog/api/), [developer SDK](./fideslog/sdk/), and [supporting infrastructure](./.github/workflows/deploy.yml) intended to provide Ethyca with an understanding of user interactions with fides tooling. Analytics are only used either as a factor in Ethyca's internal product roadmap determination process, or as insight into product adoption. Information collected by fideslog is received via HTTPs request, stored in a secure database, and never shared with third parties for any reason unless required by law.

## Using Fideslog

Ethyca's mission is to build trustworthy software. Fideslog requires that analytics data can only be collected after receiving explicit consent from the user. While the specific workflow to establish user consent will be unique to each application, the process must generally adhere to the following principles. Each SDK library exposes convenience functions, methods, and/or constants to assist with adherence to these guidelines:

1. Notify the user of Ethyca's request for analytics data as soon as possible
1. Describe the intended usage of the collected data clearly, completely, and concisely
1. Provide a simple and accessible mechanism for a user to opt-out of data collection
1. Do not repeatedly ask for consent; store the user's decision as state within the application or its configuration

### The Fideslog API

<!-- The ReDoc version of the documentation is embedded here because it doesn't allow users to easily make requests, and it looks prettier than the default documentation. -->
The fideslog API server exposes the endpoints that handle interactions with analytics event data. For a complete list of available endpoints, as well as request requirements and response details, see [the automatically generated API spec documentation](https://fideslog.ethyca.com/redoc).

### The Fideslog SDKs

The official fideslog SDK libraries are the recommended means by which to automate the submission of analytics data to the fideslog API server from any application. For language-specific documentation, best practice recommendations, and code examples, see the dedicated README for each library:

- **Python** ([README](./fideslog/sdk/python/README.md)): Available via [PyPI](https://pypi.org/project/fideslog/).

## Getting Started

### Installation

The simplest way to run the API server locally is via [Docker](https://www.docker.com/get-started/) and Make. Ensure that both tools are installed, and clone this repository. Then, from the repository's root directory, run the following command:

```sh
make api
```

By default, this will start an instance of the fideslog API server on `localhost:8080`, and attach to the container. Log output will be written to `stdout` within the container instance.

| :memo: Note | The API server will error when using only the provided [`fideslog.toml` configuration file](./fideslog.toml) and no additional environment variables. See [Enabling Database Access for Local Development](#enabling-database-access-for-local-development) below for configuration changes necessary to ensure a successful connection to the supporting database. |
|:-----------:|:---|

### Configuration

The recommended way to configure the fideslog API server is with a `fideslog.toml` configuration file, but local environment variables may be used to override any values. The fideslog API server will look for a configuration file in the following locations (ordered by priority):

1. A path defined by a `FIDESLOG__CONFIG_PATH` environment variable
1. The current working directory
1. The parent directory of the current working directory
1. The user's `$HOME` directory

If no configuration file is found in any of the above locations, the default configuration values (specified in the table below) will be used. If any environment variables are set, they will continue to override the defaults.

#### Options

|        Name          | Configuration File Section |      Environment Variable Name        |  Type   | Required |     Default      | Description |
|:--------------------:|:--------------------------:|:-------------------------------------:|:-------:|:--------:|:----------------:|-------------|
|      `account`       |        `[database]`        |    `FIDESLOG__DATABASE_ACCOUNT`       | String  |    Yes   |                  | The Snowflake account in which the fideslog database can be found. Ethyca employees may access this value internally. |
|      `database`      |        `[database]`        |    `FIDESLOG__DATABASE_DATABASE`      | String  |    No    |      `"raw"`     | The name of the Snowflake database in which analytics events should be stored. |
|     `db_schema`      |        `[database]`        |   `FIDESLOG__DATABASE_DB_SCHEMA`      | String  |    No    |     `"fides"`    | The Snowflake database schema to target. |
|   `encryption_key`   |        `[database]`        |  `FIDESLOG__DATABASE_ENCRYPTION_KEY`  | String  |    No    |     `"fides"`    | The AES encryption key to use when encrypting user email addresses at rest. |
|     `password`       |        `[database]`        |    `FIDESLOG__DATABASE_PASSWORD`      | String  |    Yes   |                  | The password associated with the Snowflake account for `user`. Ethyca employees may access this value internally. |
|       `role`         |        `[database]`        |      `FIDESLOG__DATABASE_ROLE`        | String  |    No    | `"event_writer"` | The permissions with which to access the specified Snowflake `database`.  |
|       `user`         |        `[database]`        |      `FIDESLOG__DATABASE_USER`        | String  |    Yes   |                  | The ID of the user with which to authenticate to Snowflake. Ethyca employees may access this value internally. |
|     `warehouse`      |        `[database]`        |   `FIDESLOG__DATABASE_WAREHOUSE`      | String  |    No    |   `"fides_log"`  | The Snowflake data warehouse in which the fideslog database can be found. |
|    `destination`     |        `[logging]`         |   `FIDESLOG__LOGGING_DESTINATION`     | String  |    No    |    `"stdout"`    | The absolute path to a file or directory in which logs should be stored. If a directory is passed, a `fideslog.log` file will be created in that directory. |
|       `level`        |        `[logging]`         |      `FIDESLOG__LOGGING_LEVEL`        | String  |    No    |     `"INFO"`     | The desired logging level. Accepts `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. Case insensitive. |
|       `host `        |         `[server]`         |       `FIDESLOG__SERVER_HOST`         | String  |    No    |    `"0.0.0.0"`   | The hostname on which the API server should respond. |
|    `hot_reload`      |         `[server]`         |     `FIDESLOG__SERVER_HOT_RELOAD`     | Boolean |    No    |      `False`     | Whether or not to automatically apply code changes during local development. |
|       `port`         |         `[server]`         |        `FIDESLOG__SERVER_PORT`        | Integer |    No    |      `8080`      | The port number on which the API server should listen. |
| `request_rate_limit` |         `[server]`         | `FIDESLOG__SERVER_REQUEST_RATE_LIMIT` | String  |    No    |  `"100/minute"`  | The amount of requests allowed per IP address per unit time. |

#### Example Configuration File

| :warning: WARNING | Never commit changes to the included [`fideslog.toml` file](./fideslog.toml) to version control! |
|:-----------------:|:-------------------------------------------------------------------------------------------------|

```toml
# fideslog.toml

[database]
account = "--REDACTED--"
database = "raw"
db_schema = "fides"
password = "--REDACTED--"
role = "event_writer"
user = "--REDACTED--"
warehouse = "fides_log"

[logging]
level = "info"

[server]
host = "localhost"
hot_reload = true
port = 8080
```

#### Enabling Database Access for Local Development

The `account`, `user`, and `password` configuration options mentioned above must be populated for the fideslog API server to successfully connect to the supporting database. Only Ethyca employees may access these values internally. For convenience, the included [`fideslog.env` file](./fideslog.env) will automate the process of populating the required values as environment variables, as long as the user's local environment includes the following:

```sh
# Add to .zshrc, .bash_profile, etc.

export SNOWFLAKE_ACCOUNT="--REDACTED--"
export SNOWFLAKE_DB_USER="--REDACTED--"
export SNOWFLAKE_DB_PASSWORD="--REDACTED--"
```

### Deployment

The creation of a new tag in this repository will trigger [the deployment workflow](./.github/workflows/deploy.yml) via GitHub Actions.

In general, tags are only created as part of creating a new release. All releases must include a changelog. Any breaking changes to the API and/or SDK libraries will result in a new major version release/tag. To ensure compatibility, any pull requests resulting in breaking API changes must also include updates to all SDK libraries.

## Learn More

The Fides core team is committed to providing a variety of documentation to help get you started using Fideslog.  As such, all interactions are governed by the [Fides Code of Conduct](https://ethyca.github.io/fides/community/code_of_conduct/).

### Support

Join the conversation on [Slack](https://fid.es/join-slack) and [Twitter](https://twitter.com/ethyca)!

### Contributing

We welcome and encourage all types of contributions and improvements!  Please see our [contribution guide](https://ethyca.github.io/fides/development/overview/) to opening issues for bugs, new features, and security or experience enhancements.

Read about the [Fides community](https://ethyca.github.io/fides/community/hints_tips/) or dive into the [development guides](https://ethyca.github.io/fides/development/overview) for information about contributions, documentation, code style, testing and more. Ethyca is committed to fostering a safe and collaborative environment, such that all interactions are governed by the [Fides Code of Conduct](https://ethyca.github.io/fides/community/code_of_conduct/).

## License

The Fides ecosystem of tools ([Fideslog](https://github.com/ethyca/fideslog), [Fidesops](https://github.com/ethyca/fidesops) and [Fidesctl](https://github.com/ethyca/fides)) are licensed under the [Apache Software License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
Fides tools are built on [Fideslang](https://github.com/ethyca/fideslang), the Fides language specification, which is licensed under [CC by 4](https://github.com/ethyca/fideslang/blob/main/LICENSE).

Fides is created and sponsored by Ethyca: a developer tools company building the trust infrastructure of the internet. If you have questions or need assistance getting started, let us know at fides@ethyca.com!



[release-image]:https://img.shields.io/github/v/release/ethyca/fideslog
[release-url]: https://github.com/ethyca/fideslog/releases
[deploy-image]: https://github.com/ethyca/fideslog/actions/workflows/deploy.yml/badge.svg
[actions-url]: https://github.com/ethyca/fideslog/actions
[license-image]: https://img.shields.io/:license-Apache%202-blue.svg
[license-url]: https://www.apache.org/licenses/LICENSE-2.0.txt
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black/
[mypy-image]: http://www.mypy-lang.org/static/mypy_badge.svg
[mypy-url]: http://mypy-lang.org/
[twitter-image]: https://img.shields.io/twitter/follow/ethyca?style=social
[twitter-url]: https://twitter.com/ethyca
