# calc-dephasage-thermique

Calcul du déphasage thermique d'un matériau.
D'après les informations trouvées sur le site www.autoconstruction.info.

## Utilisation

```
usage: calc-dephasage-thermique.py [-h] [-e EPAISSEUR] [-f] [-v] [-d] conductivite masse_volumique chaleur_specifique

Calcule le déphasage thermique d'un matériau. Pour plus d'informations, voir: 
https://www.autoconstruction.info/sites/www.autoconstruction.info/IMG/pdf/guide.pdf

positional arguments:
  conductivite          La conductivité (en W/m.°C).
  masse_volumique       La masse volumique (en kg/m3).
  chaleur_specifique    La chaleur spécifique (en Wh/kg.°C).

optional arguments:
  -h, --help                           show this help message and exit
  -e EPAISSEUR, --epaisseur EPAISSEUR  L'épaisseur (en m, par défaut vaut: 1 m).
  -f, --format-machine                 Affiche toutes les valeurs en colonnes.
  -v, --vitesse-seulement              Affiche unique la vitesse de déphasage (en cm/h).
  -d, --dephasage-seulement            Affiche uniquement le déphasage (en h).
```

_Testé avec python 3.5.3 sous Linux Debian 8._

