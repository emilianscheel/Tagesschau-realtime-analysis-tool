## Tagesschau Realtime Analysis Tool (TRAT)

```sh
# flask debug
VERSION=dev ENV=dev flask --debug run --host=0.0.0.0

# build image
docker build -t emilianscheel/tagesschau-realtime-analysis-tool:latest .

# run container
docker run -d \
  -v ~/apps/tagesschau-data-fetching/data:/code/data/tagesschau-data-fetching \
  --name Tagesschau-realtime-analysis-tool-container \
  --restart=always \
  -e COMMIT_MESSAGE="${{ github.event.head_commit.message }}" \
  -e VERSION=latest
  -e ENV=production
  -p 1161:5000 emilianscheel/tagesschau-realtime-analysis-tool:latest
```

### Rebuild production container

```sh
# 1. Stop container
docker stop <container-id>

# 2. Remove container
docker rm <container-id>

# 3. Restart container with the command above
```

### Nginx Configuration

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
