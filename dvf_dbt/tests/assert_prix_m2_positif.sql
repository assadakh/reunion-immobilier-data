-- Vérifie qu’aucun prix_m2 de int_ventes_simples n’est ≤ 0.
SELECT id_mutation, nom_commune, valeur_fonciere, surface_reelle_bati, prix_m2
FROM {{ ref('int_ventes_simples') }}
WHERE prix_m2 <= 0