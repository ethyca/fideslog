# Fideslog: Python SDK

[![Latest Release Version][release-image]][release-url]
[![Latest Deployment][deploy-image]][actions-url]
[![License][license-image]][license-url]
[![Code style: black][black-image]][black-url]
[![Checked with mypy][mypy-image]][mypy-url]
[![Twitter][twitter-image]][twitter-url]

![Fideslog banner](../../../assets/fideslog.png "Fideslog banner")

## Overview

Fideslog is the [API server](../../api/), [developer SDK](../../sdk/), and [supporting infrastructure](../../../.github/workflows/deploy.yml) intended to provide Ethyca with an understanding of user interactions with fides tooling. Analytics are only used either as a factor in Ethyca's internal product roadmap determination process, or as insight into product adoption. Information collected by fideslog is received via HTTPs request, stored in a secure database, and never shared with third parties for any reason unless required by law.

This library is the recommended means by which to automate the submission of analytics data to the fideslog API server from a Python application.

## Installation

Install the fideslog Python SDK using a package manager. It is available via [PyPI](https://pypi.org/project/fideslog/). For a complete list of available release versions and their associated release notes, see [the Releases tab](https://github.com/ethyca/fideslog/releases) in the repository.

```sh
pip install fideslog
```

## Usage

### Establishing User Consent

| :memo: Note | See Ethyca's [guidelines for establishing user consent](../../../README.md#using-fideslog) for a list of requirements for collecting analytics. |
|:-----------:|:---|

It is recommended to display the content of the `OPT_OUT_COPY` constant exposed by [the `utils.py` file](./utils.py) as a means of informing users of the application's intent to collect analytics data **as early as possible within the usage workflow of the application**. If the application uses a CLI interface, the content of the `OPT_OUT_PROMPT` constant (also exposed by [the `utils.py` file](./utils.py)) can be displayed to collect explicit consent.

If the application is stateful, store the user's response within the top-level state-maintaining mechanism.

If the application is stateless, store the user's response within the application's configuration. If the application is configured with a TOML file, it is recommended to enable a `[user]` section, and store the consent within an `analytics_opt_out` configuration option. For example:

```toml
[user]
analytics_opt_out = false
```

### Identifying the Sending Application

The SDK exposes an `AnalyticsClient` class from [the `client.py` file](./client.py). Ideally only a single instance of `AnalyticsClient` will be necessary to establish the application-level details of all analytics event data emitted by the application.

The `utils.py` file exposes [the `generate_client_id()` function](https://github.com/ethyca/fideslog/blob/3dcebe735a64286d8638435a55094fbd020c153b/fideslog/sdk/python/utils.py#L22-L32), which should be used only once per application instance in order to safely generate a fully anonymized, globally unique identifier. For stateless applications, it is recommended to store this value in an `analytics_id` configuration option, or in an instance-specific database.

#### Example

```python
from platform import system

from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.utils import generate_client_id

CLIENT_ID: str = generate_client_id(b"a_fides_tool")  # utils.py also exposes some helpful bytestrings


def get_version() -> str:
    return "1.0.0"

def in_developer_mode() -> bool:
    return False

client = AnalyticsClient(
    client_id=CLIENT_ID,
    developer_mode=in_developer_mode(),
    extra_data={
        "this data": "will be included with every event sent by this client",
        "include": "any context that every event requires",
        "never include": "identifying information of any kind",
    },
    os=system(),
    product_name="a_fides_tool",
    production_version=get_version(),
)
```

### Sending Analytics Data

The SDK exposes an `AnalyticsEvent` class from [the `event.py` file](./event.py). Create a new instance of `AnalyticsEvent` for every discrete event that should be persisted. Then, use the `AnalyticsClient.send()` method to make a request to the fideslog API server and persist the event.

#### Example

Building on the example from the previous section:

```python
from datetime import datetime, timezone
from platform import system

from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.utils import generate_client_id

CLIENT_ID: str = generate_client_id(b"a_fides_tool")  # utils.py exposes some helpful bytestrings


def get_version() -> str:
    return "1.0.0"

def in_developer_mode() -> bool:
    return False

def in_docker_container() -> bool:
    return True

def running_on_local_host() -> bool:
    return False

client = AnalyticsClient(
    client_id=CLIENT_ID,
    developer_mode=in_developer_mode(),
    extra_data={
        "this data": "will be included with every event sent by this client",
        "include": "any context that every event requires",
        "never include": "identifying information of any kind",
    },
    os=system(),
    product_name="a_fides_tool",
    production_version=get_version(),
)

cli_command_event = AnalyticsEvent(
    command="cli_command_name sub_command_name",
    docker=in_docker_container(),
    event="cli_command_executed",
    error=None,
    event_created_at=datetime.now(tz=timezone.utc),
    extra_data={
        "this data": "will be included only on this event",
        "it will": "overwrite keys included in the client's extra_data",
        "include": "any context that this event requires",
        "never include": "identifying information of any kind",
    },
    flags=["--dry", "-v"],
    local_host=running_on_local_host(),
    resource_counts={
        "datasets": 7,
        "policies": 26,
        "systems": 9,
    },
    status_code=0,
)

client.send(cli_command_event)
```

### Handling Exceptions

The SDK exposes an `AnalyticsError` type from [the `exceptions.py` file](./exceptions.py). In the event that an exception is raised by this library, it will either be a literal `AnalyticsError`, or inherit from `AnalyticsError`. In general, it is not recommended to raise these exceptions within application code, to prevent breaking the application and/or user workflow; these exceptions are intended to be written to log output, and otherwise ignored.

#### Example

Building on the example from the previous section:

```python
from datetime import datetime, timezone
from platform import system

from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.event import AnalyticsEvent
from fideslog.sdk.python.exceptions import AnalyticsError
from fideslog.sdk.python.utils import generate_client_id

CLIENT_ID: str = generate_client_id(b"a_fides_tool")  # utils.py exposes some helpful bytestrings


def get_version() -> str:
    return "1.0.0"

def in_developer_mode() -> bool:
    return False

def in_docker_container() -> bool:
    return True

def running_on_local_host() -> bool:
    return False

try:
    client = AnalyticsClient(
        client_id=CLIENT_ID,
        developer_mode=in_developer_mode(),
        extra_data={
            "this data": "will be included with every event sent by this client",
            "include": "any context that every event requires",
            "never include": "identifying information of any kind",
        },
        os=system(),
        product_name="a_fides_tool",
        production_version=get_version(),
    )

    cli_command_event = AnalyticsEvent(
        command="cli_command_name sub_command_name",
        docker=in_docker_container(),
        event="cli_command_executed",
        error=None,
        event_created_at=datetime.now(tz=timezone.utc),
        extra_data={
            "this data": "will be included only on this event",
            "it will": "overwrite keys included in the client's extra_data",
            "include": "any context that this event requires",
            "never include": "identifying information of any kind",
        },
        flags=["--dry", "-v"],
        local_host=running_on_local_host(),
        resource_counts={
            "datasets": 7,
            "policies": 26,
            "systems": 9,
        },
        status_code=0,
    )

    client.send(cli_command_event)

except AnalyticsError as err:   # It is not recommended to raise this exception,
    print(err)                  # to prevent interrupting the application workflow.
else:
    print("Analytics event sent")
```

### Registering Users

The SDK exposes a `Registration` class from [the `registration.py` file](./registration.py). Create a new instance of `Registration` for every user that should be registered. Then, use the `AnalyticsClient.register()` method to make a request to the fideslog API server and register the user.

#### Example

Building on the example from a previous section:

```python
from platform import system

from fideslog.sdk.python.client import AnalyticsClient
from fideslog.sdk.python.registration import Registration
from fideslog.sdk.python.utils import generate_client_id

CLIENT_ID: str = generate_client_id(b"a_fides_tool")  # utils.py exposes some helpful bytestrings


def get_version() -> str:
    return "1.0.0"

def in_developer_mode() -> bool:
    return False

client = AnalyticsClient(
    client_id=CLIENT_ID,
    developer_mode=in_developer_mode(),
    extra_data={
        "this data": "will be included with every event sent by this client",
        "include": "any context that every event requires",
        "never include": "identifying information of any kind",
    },
    os=system(),
    product_name="a_fides_tool",
    production_version=get_version(),
)

user_registration = Registration(
    email="user@example.com",
    organization="Example Organization, LLC",
)

client.register(user_registration)
```

## Contributing

We welcome and encourage all types of contributions and improvements!  Please see our [contribution guide](https://ethyca.github.io/fides/development/overview/) to opening issues for bugs, new features, and security or experience enhancements.

Read about the [Fides community](https://ethyca.github.io/fides/community/hints_tips/) or dive into the [development guides](https://ethyca.github.io/fides/development/overview) for information about contributions, documentation, code style, testing and more. Ethyca is committed to fostering a safe and collaborative environment, such that all interactions are governed by the [Fides Code of Conduct](https://ethyca.github.io/fides/community/code_of_conduct/).

### Support

Join the conversation on [Slack](https://fid.es/join-slack) and [Twitter](https://twitter.com/ethyca)!

## License

Fideslog and the fides ecosystem of tools are licensed under the [Apache Software License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
Fides tools are built on [fideslang](https://github.com/ethyca/privacy-taxonomy), the fides language specification, which is licensed under [CC by 4](https://github.com/ethyca/privacy-taxonomy/blob/main/LICENSE).

Fides is created and sponsored by [Ethyca](https://ethyca.com/): a developer tools company building the trust infrastructure of the internet. If you have questions or need assistance getting started, let us know at fides@ethyca.com!



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
