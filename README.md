# Hannukah of Data Django solutions

- See link https://hanukkah.bluebird.sh/5784/data/

- See similar Django solutions to this puzzle here https://git.sr.ht/~tuxpup/hanukkah_of_data_2022

# Instructions

- Set up repo with Poetry

```bash
poetry install
```

- Copy sqlite file from website https://hanukkah.bluebird.sh/5784/data/

```bash

cp path/to/noahs.sqlite path/to/repo/src/
```

- Run migrations. Since you have an existing database, we use --fake-initial so migrations aren't applied.

```bash

poetry run python manage.py migrate --fake-initial
```

- Add superuser to use admin interface

```bash
cd src; poetry run python manage.py createsuperuser
```

- If using neovim, activate virtual env before starting:

```bash

cd path/to/your/repo; eval $(poetry env activate);
```

```

```
