# stars7

it is a project trying to prove that patterns don't exist or do exist in 7-star lottery


```shell
python -m cProfile -o data/profile.out app.py
```

```shell
git pull origin master --force
```

```shell
npm run build
npm run preview > /dev/null 2>&1 &

python3 -m uvicorn server:app --host=0.0.0.0 --reload > /tmp/uvicorn.log 2>&1 &
```

```shell
# crontab
35,45,55 20,21 * * 0,2,5 python3 /home/ubuntu/app/stars7/app.py > /dev/null 2>&1 &
```