SELECT
    id_mutation,
    CAST(date_mutation AS DATE)          AS date_mutation,
    YEAR(CAST(date_mutation AS DATE))    AS annee,
    numero_disposition,
    nature_mutation,
    valeur_fonciere,
    code_commune,
    nom_commune,
    type_local,
    surface_reelle_bati,
    surface_terrain,
    nombre_pieces_principales,
    longitude,
    latitude
FROM {{ source('dvf', 'raw_dvf') }}