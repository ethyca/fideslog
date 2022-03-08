# fideslog
Privacy respecting usage analytics collection.

## Development

The following environment variables must be set in order to successfully run the API server locally:

```
export SNOWFLAKE_ACCOUNT=[see 1Password]
export SNOWFLAKE_DB_USER=[see 1Password]
export SNOWFLAKE_DB_PASSWORD=[see 1Password]
```

## Sample Working Implementation
_(Working from a local installation)_

First, start up a local api server
```
$ make api
```

Next create a virtual environment, install fideslog, and open up a python env
```bash
$ python3 -m venv env && source env/bin/activate
$ pip install -e .
$ python
```

The following below should work as is (provided you have a populated `fideslog.toml`/ environment variables)
```python
import platform
from importlib.metadata import version
import asyncio
from datetime import datetime, timezone
from fideslog.sdk.python import event, client

product_name = "fideslog"

fideslog_client = client.AnalyticsClient(
    client_id="test_client_id",
    os=platform.system(),
    product_name=product_name,
    production_version=version(product_name),
)

fideslog_event = event.AnalyticsEvent(
    event="test_event",
    event_created_at=datetime.now(timezone.utc),
)

asyncio.run(fideslog_client.send(event=fideslog_event))
```

Example structure of a minimum working payload
```json
{
    "client_id": "test_client_id",
    "event": "test_event",
    "event_created_at": "2022-02-21 19:56:11Z",
    "os": "darwin",
    "product_name": "fideslog",
    "production_version": "1.2.3"
}
```


## Example of an opt-out routine

All opt-out functionality will reside in the fides family tool implementing `fideslog`

The current copy to be used is as follows:
> Fides needs your permission to send Ethyca a limited set of anonymous usage statistics.
> Ethyca will only use this anonymous usage data to improve the product experience, and will never collect sensitive or personal data.
>
> ***
> Don't believe us? Check out the open-source code here:
>     https://github.com/ethyca/fideslog
> ***
>
> To opt-out of all telemetry, press "n". To continue with telemetry, press any other key.


### Sample storing of values for fideslog
All values are currently stored in the fides tool configuration toml file, as below:
```toml
[cli]
analytics_id = "some_generated_anonymous_unique_id"

[user]
analytics_opt_out = false
```


### Generating a unique id

Using Pydantic defaults will create a unique ID if one doesn't exist:

```python
from fideslog.sdk.python.utils import generate_client_id, FIDESCTL_CLI

class CLISettings(FidesSettings):
    """Class used to store values from the 'cli' section of the config."""

    local_mode: bool = False
    server_url: str = "http://localhost:8080"
    analytics_id: str = generate_client_id(FIDESCTL_CLI)

    class Config:
        env_prefix = "FIDESCTL__CLI__"
```


### Gaining consent in a conspicuous way


A user should be asked only once if they would like to provide anonymous analytics to Ethyca.

Integrating with an initial workflow (i.e. `fidesctl init`) is a great way to capture and generate the required values up front.

Additionally, having a catch in the top-most level click command can provide an alternative method to ask only once for permission.


### Implementing the sdk

There are two items required for successfully sending an event to `fideslog`: `AnalyticsClient` & `AnalyticsEvent`

`AnalyticsClient` establishes some (relatively) constant properties that are required upon instantiation.

`AnalyticsEvent` is much more variable in makeup and can contain a number of extra properties for tacking purposes. Some of these will depend on the fides ecosystem being tracked (`endpoint` should align with `api` events for instance) with only the `event` and `event_created_at` properties required to send an event.

Example function of sending an event:
```python
def opt_out_anonymous_usage(
    analytics_values: Optional[Dict] = None, config_path: str = ""
) -> bool:
    """
    This function handles the verbiage and response of opting
    in or out of anonymous usage analytic tracking.

    If opting out, return True to set the opt out config.
    """
    opt_in = input(OPT_OUT_COPY)
    if analytics_values:
        analytics_values["user"]["analytics_opt_out"] = bool(opt_in.lower() == "n")
        update_config_file(analytics_values)
    return bool(opt_in.lower() == "n")
```


Click allows for embedding a call to a function at higher levels of grouped commands. This will allow for consistent capturing of event data without having to touch every single implemented command. For nested groups however, you will likely be required to have function calls at the lower-tier group level as well. (i.e. `fidesctl export organization` will require an event on the `export` function to return the invoked subcommand)

Example at top-level cli group:
```python
if not ctx.obj["CONFIG"].user.analytics_opt_out:
    send_anonymous_event(
        command=ctx.invoked_subcommand, client_id=ctx.obj["CONFIG"].cli.analytics_id
    )
```

Example at nested cli group:
```python
if not ctx.obj["CONFIG"].user.analytics_opt_out:
    command = " ".join(filter(None, [ctx.info_name, ctx.invoked_subcommand]))
    send_anonymous_event(
        command=command, client_id=ctx.obj["CONFIG"].cli.analytics_id
    )
```
