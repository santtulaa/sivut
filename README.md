# Karhunkyttäys sivut #
Käyttäjä voi luoda ja kirjautua sisään, tarkastella muiden varauksia, sekä omia, hintoja sekä laittaa unohditko salasanasi
ylläpitäjä voi tarkastella varauksia, perua niitä, sekä varata ilmaiseksi ja muuttaa päivien hintoja


# omat muistiinpanot: #

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

python3: pääsee pois control + d

jos psql ei anna poistaa tablea, koska käytössä:
 DROP TABLE taulukonnimi CASCADE;


# Käynnistysohjeet: #
1. Kloonaa projekti omalle koneellesi 
- git clone git@github.com:santtulaa/sivut.git
2. siirry juurikansioon
3. luo kansio .env ja määritä sen sisällöksi:
DATABASE_URL=postgresql:///salmelsa
SECRET_KEY=43f71de180ba654ee56e8ade27f89807
4. seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuuden komennoilla:
- pip install -r requirements.txt
- python3 -m venv venv
- source venv/bin/activate
- pip install -r ./requirements.txt
5. Määritä vielä tietokannan skeema komennolla
- psql < schema.sql
- Huom! Halutessasi voit myös luoda oman tietokannan sovellusta varten ja lisätä taulukot sinne. Tämä onnistuu seuraavalla tavalla:
    - psql
    - CREATE DATABASE salmelsa
    - psql -d salmelsa <schema.sql       
6. Voit käynnistää sovelluksen komennolla flask run

