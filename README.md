Karhunkyttäys sivut
Käyttäjä voi luoda ja kirjautua sisään, tarkastella muiden varauksia, sekä omia, hintoja sekä laittaa unohditko salasanasi
ylläpitäjä voi tarkastella varauksia, perua niitä, sekä varata ilmaiseksi ja muuttaa päivien hintoja


omat muistiinpanot:

miten laittaa psql päälle
start-pg.sh
sammuu control+c
ja jos unohdit sammuttaa niin: kill $(ps x|grep pgsql/bin/postgres|grep -v grep|awk '{print $1}')

miten laittaa venv päälle:
source/venv/bin/activate
ja lopettaa: deactivate

miten run: flask run

jos juokset muiden sovelluksen, niin voit ladata requirementsit tuolt
pip install -r requirements.txt

jos on juoksemmassa jo toinen ohjelma niin saat tietää sen komennolla lsof -i:5000
ja voit tappaa sen kill "pid numero", jos ei toimi voit tappaa sen kill -9 "pid numero"