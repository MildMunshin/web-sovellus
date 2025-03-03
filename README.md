# Web-sovellus biisinkirjoittajille ja artisteille musiikin jakamiseen

Biisinkirjottajille ja artisteille suunnattu sovellus/sivusto, jossa voi jakaa omia kappaleita ja artistiprofiileja.

## Asennus:

* Kloonaa repositorio ja siirry juurikansioon

```git clone https://github.com/MildMunshin/web-sovellus.git```

```cd web-sovellus```
  
* Asenna ja ota käyttöön Python-virtuaaliympäristö:

```python3 -m venv venv```

```source venv/bin/activate```

* Asenna ja käynnistä flask:

```pip install flask```

```flask run```

* Kokeile sovellusta testiprofiileilla (vapaaehtoinen):

```Username: MirrohMirroh, Salasana: mirroh123```

```Username: CyberGirl, Salasana: CG123```

## Sovelluksen tämänhetkinen tila: 

Käyttäjä voi luoda profiilin, kirjautua sisään ja ladata profiilikuvan. Käyttäjä voi ladata sivustolle kappaleita lomakkeella, johon syötetään tiedot artistista ja kappaleen nimestä, kappaleen äänitiedosto ja kansikuva. Sovelluksen etusivu näyttää kaikki käyttäjien lataamat kappaleet, kappaleiden kansikuvan ja soittimen, jolla ne voidaan toistaa. Käyttäjillä on oma profiilisivu, jossa näkyy käyttäjän profiiliteksti/bio, profiilikuva, sekä kyseisen käyttäjän lataamat kappaleet. Kappaleilla on myös itsenäiset kappalesivut, joihin pääse linkin kautta kappaleen nimeä klikkaamalla. Käyttäjät voivat kommentoida kappaleita sekä jättää tykkäyksiä ja ei-tykkäyksiä. Käyttäjät voivat myös etsiä kappaleita artistin, kappaleen nimen tai tyylilajin perusteella.
