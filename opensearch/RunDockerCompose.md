
mkdir opensearch; cd ./opensearch

**docker-compose up**

**Look for these messages:**

  opensearch-dashboards | {“type”:”log”,”@timestamp”:”2021–06–13T00:01:47Z”,”tags”:[“listening”,”info”],”pid”:1,”message”:”Server running at http://0:5601"}

In the browser:
login:
http://localhost:5601/
- Username: admin
- Password: admin
- These are the default userid and password.

