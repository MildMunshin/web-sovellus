# Web-sovellus biisinkirjoittajille ja artisteille musiikin jakamiseen

Biisinkirjottajille ja artisteille suunnattu sovellus/sivusto, jossa voi jakaa omia kappaleita ja artistiprofiileja.

Asennus:

- Asenna ja ota käyttöön Python-virtuaaliympäristö:
python3 -m venv venv
source venv/bin/activate

- Asenna flask-kirjasto:
pip install flask

Sovelluksen tämänhetkinen tila: Käyttäjä voi luoda profiilin, kirjautua sisään ja ladata profiilikuvan. Käyttäjä voi ladata sivustolle kappaleita lomakkeella, johon syötetään tiedot artistista ja kappaleen nimestä, kappaleen äänitiedosto ja kansikuva. Sovelluksen etusivu näyttää kaikki käyttäjien lataamat kappaleet, kappaleiden kansikuvan ja soittimen, jolla ne voidaan toistaa. Käyttäjillä on oma profiilisivu, jossa näkyy kyseisen käyttäjän lataamat kappaleet samaan tapaan. Kappaleilla on myös itsenäiset kappalesivut, joihin pääse linkin kautta kappaleen nimeä klikkaamalla. Käyttäjät voivat kommentoida kappaleita sekä jättää tykkäyksiä ja ei-tykkäyksiä.

Sovelluksesta puuttuu vielä mahdollisuus etsiä ja järjestää tietokohteita hakusanojen avulla, tietojen lisääminen profiilisivulle sekä erinäisiä tilastoja (toistokerrat, vierailut profiilissa jne). 
