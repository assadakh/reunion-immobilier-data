WITH ventes AS (
    SELECT *
    FROM {{ ref('stg_dvf') }}
    WHERE nature_mutation = 'Vente'
),

mutations_simples AS (
    SELECT id_mutation
    FROM ventes
    WHERE type_local IN ('Maison', 'Appartement', 'Local industriel. commercial ou assimilé')
    GROUP BY id_mutation
    HAVING COUNT(*) = 1
),

locaux AS (
    SELECT
        v.*,
        v.valeur_fonciere / v.surface_reelle_bati         AS prix_m2,
        v.valeur_fonciere / v.surface_reelle_bati < 500   AS hors_marche
    FROM ventes v
    INNER JOIN mutations_simples m ON v.id_mutation = m.id_mutation
    WHERE v.type_local IN ('Maison', 'Appartement', 'Local industriel. commercial ou assimilé')
      AND v.surface_reelle_bati > 0
      AND v.valeur_fonciere > 1000
)

SELECT * FROM locaux