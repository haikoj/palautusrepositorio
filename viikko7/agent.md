Agentti (Claude Sonnet 4.5) loi toimivan web-käyttöliittymän. Testasin sovellusta manuaalisesti itse sekä katsoin, että kaikki testit menivät läpi. 

Annoin agentille vain muutamia komentoja. Agentti osasi rakentaa kaiken ongelmitta, mutta kun komensin sen testaamaan testejä, se ei osannut ajaa niitä aluksi terminaalista. Tässä vaiheessa meni melko kauan. Lisäksi pari testiä ei mennyt läpi toisin kuin agentti vakuutti, mutta se sai ne lopulta korjattua.

Agentti ymmärsi komentoni osin väärin, koska se kyllä käytti olemassa olevaa koodia, mutta siirsi sitä app.py:hyn ja vanhoista muuttamattomista tiedostoista tuli käyttämättömiä. Sovellus toimii kuitenkin siis samalla logiikalla, mutta huomasin että minun olisi pitänyt olla paljon tarkempi komennoissani ja selittää haluamani asiat laajemmin, jotta lopputuloksesta olisi tullut mahdollisimman halutunlainen.  

Pytest-testit ovat hyvin kattavat ja niitä on yhteensä 70. Niissä testataan mm. eri pelimoodien alustus, eteneminen ja pelin päättyminen sekä muistin toimiminen advanced_ai moodissa.

Agentin tekemä koodi on selkeää ja ymmärrettävää.
