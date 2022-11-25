#/usr/bin/bash

# update source
git fetch origin master
git reset --hard origin/master

if test $(pgrep -f gunicorn|wc -l) -eq 0;then
	# start
	echo "server not started yet."
	gunicorn -D --worker-class="uvicorn.workers.UvicornWorker" server:app --bind 0.0.0.0:8000 --threads 8
	echo "server started."
else
	# restart
	echo "server already started."
	ps aux | grep gunicorn | grep -v grep | awk '{system("kill -HUP "$2)}'
	echo "server restarted."
fi

# build pages and deploy to webroot
cd ./portal
npm run build && cp -pr ./dist/* /var/www/html
echo "pages deployed"
