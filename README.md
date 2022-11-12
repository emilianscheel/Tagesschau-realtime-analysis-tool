## Tagesschau Realtime Analysis Tool (TRAT)

```
# flask debug
flask --debug run --host=0.0.0.0

# build image
docker build -t tagesschau-realtime-analysis-tool .

# run container
docker run -d -v ~/apps/tagesschau-data-fetching/data:/code/data/tagesschau-data-fetching --name Tagesschau-realtime-analysis-tool-container -p 1161:5000 Tagesschau-realtime-analysis-tool
```

### nginx

```
# nginx conf file 'Tagesschau-realtime-analysis-tool.conf'
server {
      server_name  trat.surayako.com;

      location / {
        proxy_pass  http://localhost:1161;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
        proxy_redirect off;
      }
}
```

### Links

- Tutorial vom 12.11.22: https://arshovon.com/blog/develop-flask-app-using-docker-and-bootstrap/
