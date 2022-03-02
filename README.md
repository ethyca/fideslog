# fideslog
Privacy respecting usage analytics collection.


## Sample Working Implementation
_(Working from a local installation)_



First, start up a local api server
```
$ make api
```

Next create a virtual environment, install fideslog, and open up a python env
```
$ python3 -m venv env && source env/bin/activate
$ pip install -e .
$ python
```

The following below should work as is (provided you have a populated `fideslog.toml`)
```
import asyncio
from datetime import datetime, timezone

from fideslog.sdk.python import event, client

API_KEY = "12345"


fideslog_client = client.AnalyticsClient(
    api_key=API_KEY,
    client_id="test_client_id",
    os="Darwin",
    product_name="fideslog",
    production_version="1.2.3",
)

fideslog_event = event.AnalyticsEvent(
    event="test_event",
    event_created_at=datetime.now(timezone.utc),
)

asyncio.run(fideslog_client.send(event=fideslog_event))
```

Example structure of a minimum working payload
```
{
    "client_id": "test_client_id",
    "event": "test_event",
    "event_created_at": "2022-02-21 19:56:11Z",
    "os": "darwin",
    "product_name": "fideslog",
    "production_version": "1.2.3"
}
```
