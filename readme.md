# Generate AS2 reports summary

Git clone `https://github.com/w3c/activitystreams` into `/path/to/activitystreams/repo` then run:

```
sudo docker build -t reports .
sudo docker run -it --rm -v /path/to/activitystreams/repo:/usr/src/app/activitystreams --name as2 reports
```