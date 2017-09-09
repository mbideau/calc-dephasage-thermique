#!/usr/bin/env python
#
# calcule le déphasage thermique d'un matériaux
# @source: https://www.autoconstruction.info/sites/www.autoconstruction.info/IMG/pdf/guide.pdf
#

import argparse
from sys import stdout, stderr, exit, exc_info
from math import sqrt;

CONST_vitesse_transfert = 72.5
CONST_DEPHASAGE = 1.38
CONST_PRINT_VALUE_SIZE = 5

def init_parser():
    parser = argparse.ArgumentParser( \
        description="Calcule le déphasage thermique d\'un matériau. Pour plus d'informations, voir: https://www.autoconstruction.info/sites/www.autoconstruction.info/IMG/pdf/guide.pdf" \
    )
    parser.add_argument( \
        'conductivite', help='La conductivité (en W/m.°C).' \
    )
    parser.add_argument( \
        'masse_volumique', help='La masse volumique (en kg/m3).' \
    )
    parser.add_argument( \
        'chaleur_specifique', help='La chaleur spécifique (en Wh/kg.°C).' \
    )
    parser.add_argument( \
        '-e', '--epaisseur', dest='epaisseur', type=float, default=1.0, help="L'épaisseur (en m, par défaut vaut: 1 m)." \
    )
    parser.add_argument( \
        '-f', '--format-machine', dest='format_machine', action='store_true', help='Affiche toutes les valeurs en colonnes.' \
    )
    parser.add_argument( \
        '-v', '--vitesse-seulement', dest='vitesse_seulement', action='store_true', help='Affiche unique la vitesse de déphasage (en cm/h).' \
    )
    parser.add_argument( \
        '-d', '--dephasage-seulement', dest='dephasage_seulement', action='store_true', help='Affiche uniquement le déphasage (en h).' \
    )
    return parser


def calc_capacite_thermique(masse_volumique, chaleur_specifique):
    """
    Return float

    Calcule la capacité thermique d'un matériaux en fonction de ses caractéristiques.
    La capacité thermique d’un matériau est le produit de sa masse volumique par sa chaleur spécifique.
            C = ρ * c
    où :
            ρ : masse volumique (kg/m3)
            c : chaleur spécifique (Wh/kg.°C)
    """
    return masse_volumique * chaleur_specifique


def calc_diffusivite(conductivite, capacite_thermique):
    """
    Return float

    Calcule la diffusitivté d'un matériaux en fonction de ses caractéristiques.
    La diffusivité est le rapport de la conductivité d’un corps à sa capacité thermique :
            d = λ / cρ
    où :
            d : diffusivité (m 2 /h)
            λ : conductivité (W/m.°C)
            cρ: capacité thermique (Wh/m3.°C)
    """
    return conductivite / (capacite_thermique)


def calc_dephasage(diffusivite, epaisseur):
    """
    Return float

    Calcule le déphasage thermique d'un matériaux pour une épaisseur donnée.
    Le déphasage d’une onde de chaleur de période journalière peut se calculer de façon approchée par l’expression :
            D = 1.38 * e * sqrt(1 /d)
    où :
            D : déphasage en (h)
            e : épaisseur de la paroi en (m)
            d : diffusivité (m 2 /h)
    """
    return CONST_DEPHASAGE * epaisseur * sqrt(1 / diffusivite)


def calc_vitesse_transfert(diffusivite):
    """
    Return float

    Calcule la vitesse de déphasage thermique d'un matériaux.
    Pour caractériser un matériau, il est peut-être plus parlant d’exprimer le déphasage en terme de vitesse de transfert de l’onde de chaleur à travers la paroi. Cette vitesse v en cm/h est donnée par la relation suivante tirée de la précédente :
            v = 72.5 / sqrt(1 / d)
    où :
            d : diffusivité (m 2 /h).
    """
    return CONST_vitesse_transfert / sqrt(1 / diffusivite)


def main():
	
    parser = init_parser()
    args = parser.parse_args()

    # convertit les arguments (string) en décimales (float)
    conductivite = float(args.conductivite.replace(',', '.'))
    masse_volumique = float(args.masse_volumique.replace(',', '.'))
    chaleur_specifique = float(args.chaleur_specifique.replace(',', '.'))
    epaisseur = args.epaisseur

    # calcule la capacité thermique
    capacite_thermique = calc_capacite_thermique(masse_volumique, chaleur_specifique)
    # calcule la diffusivite
    diffusivite = calc_diffusivite(conductivite, capacite_thermique)
    diffusivite_x1000 = diffusivite * 1000

    if args.vitesse_seulement:
        print(calc_vitesse_transfert(diffusivite))
    elif args.dephasage_seulement:
        print(calc_dephasage(diffusivite, epaisseur))
    elif args.format_machine:
        dephasage = calc_dephasage(diffusivite, epaisseur)
        vitesse_transfert = calc_vitesse_transfert(diffusivite)
        print("%.0f %.2f %.2f %.2f" % (capacite_thermique, diffusivite_x1000, vitesse_transfert, dephasage))
    else:
        print("Données entrées")
        print("\t        Conductivité: " + "{:.2f}".format(conductivite).rjust(CONST_PRINT_VALUE_SIZE) + " W/m.°C")
        print("\t     Masse volumique: " + "{:.0f}".format(masse_volumique).rjust(CONST_PRINT_VALUE_SIZE) + " kg/m3")
        print("\t  Chaleur specifique: " + "{:.3f}".format(chaleur_specifique).rjust(CONST_PRINT_VALUE_SIZE) + " Wh/kg.°C")
        print("\t           Épaisseur: " + "{:.2f}".format(epaisseur).rjust(CONST_PRINT_VALUE_SIZE) + " m")
        print("")
        print("Résultats")
        print("\t  Capacité thermique: " + "{:.0f}".format(capacite_thermique).rjust(CONST_PRINT_VALUE_SIZE) + " Wh/m3.°C")
        print("\t         Diffusivité: " + "{:.2f}".format(diffusivite_x1000).rjust(CONST_PRINT_VALUE_SIZE) + " 10^-3 m2/h")
        vitesse_transfert = calc_vitesse_transfert(diffusivite)
        print("\tVitesse de transfert: " + "{:.2f}".format(vitesse_transfert).rjust(CONST_PRINT_VALUE_SIZE) + " cm/h")
        dephasage = calc_dephasage(diffusivite, epaisseur)
        print("\t           Déphasage: " + "{:.2f}".format(dephasage).rjust(CONST_PRINT_VALUE_SIZE) + " h")


if __name__ == "__main__":
    main()
