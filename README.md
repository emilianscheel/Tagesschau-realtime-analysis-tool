## Search Engine Ranking Tool (SERT)

```
# build image
docker build -t sert-image .

# run container
docker run -d --name sert-container -p 1151:5000 sert-image
```

### nginx

```
# nginx conf file 'search-engine-ranking-tool.conf'
server {
      server_name  sert.surayako.com;

      location / {
        proxy_pass  http://localhost:1151;
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
