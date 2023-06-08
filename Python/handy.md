To check dates etc of releases:

```
wget https://pypi.org/pypi/tca-beam/json
```

jq one-liner to see all dates:

```
curl -s https://pypi.org/pypi/tca-beam/json | jq -r '.releases | to_entries[] | .key + " " + (.value[0].upload_time)'
```

Gives:

```
0.3.4 2023-06-05T15:00:46
0.3.5 2023-06-05T17:02:17
0.4.0 2023-06-06T10:23:49
0.5.0 2023-06-07T20:39:43
0.5.1 2023-06-07T20:54:59
0.5.2 2023-06-07T20:55:46
```
