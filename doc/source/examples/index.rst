:Author: Marie-Dominique Van Damme
:Version: 1.0
:License: --
:Date: 08/04/2026


End-to-End Examples
====================


À partir de trajectoires synthétiques
--------------------------------------

Cet exemple, décliné en une version *quickstart* et une version détaillée, offre une introduction rapide à **footprint2graph**. Il permet aux utilisateurs d’expérimenter la chaîne de traitement et de se familiariser avec ses principales étapes et paramètres. Il s’appuie sur la génération de trajectoires simulées à partir d’un réseau, ce qui facilite les tests dès lors qu’un réseau est disponible sous la forme d’un ensemble de géométries représentant les arêtes du graphe.


.. nbgallery::
    :name: quickstart-gallery
    :glob:

    Quickstart
    DetailedQuickstart
    


Génération des jeux de données publiés
---------------------------------------

Ces trois exemples contiennent le code source utilisé pour générer trois jeux de données publiés dans l'entrepôt de données `Recherche Data Gouv <https://entrepot.recherche.data.gouv.fr/dataverse/intforout>`_. Ces jeux de données couvrent :

* une petite zone située dans le Parc naturel régional des Bauges ;
* deux petites zones situées dans la vallée de Chamonix.

Ces trois exemples font partie d'un livrable du Work Package 2 du `projet de recherche IntForOut <https://www.umr-lastig.fr/intforout/>`_.

Les données GNSS ont été produites et fournies par la plateforme **Outdoorvision**, un service qui met à disposition des traces partagées volontairement par des utilisateurs lors de leurs activités de plein air. La plateforme est soutenue par le *Pôle Ressources National Sports de Nature* (**PRNSN**). Dans le cadre du projet de recherche IntForOut, les traces ont été extraites de la plateforme, puis nettoyées, filtrées et anonymisées.


**Réseaux de mobilité pédestre** :

.. nbgallery::
    :name: intforout-gallery
    :glob:

    PedestrianGraphPlanDeLaLimace
    PedestrianGraphPlanpraz
    PedestrianGraphPlanDeLAiguille


