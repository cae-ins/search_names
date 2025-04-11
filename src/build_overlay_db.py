import polars as pl
from pathlib import Path

files_dir = Path("../files")  # Dossier au même niveau que le répertoire actuel

# Charger le CSV avec les bonnes colonnes
df = pl.read_csv(
    files_dir/ "nom_prenoms_lower_trim.csv",
    separator=",",  # Ajuster selon le séparateur réel
    new_columns=["nom", "prenoms", "sexe", "age"],
    dtypes={
        "nom": pl.Utf8,
        "prenoms": pl.Utf8,
        "sexe": pl.Categorical,  # Optimisation mémoire
        "age": pl.UInt8
    }
)

df_exploded = df.with_columns(
    pl.col("prenoms").str.split(" ").alias("prenoms_split")
).explode("prenoms_split").rename({"prenoms_split": "prenom_explode"})

stats = (
    pl.concat([
        df_exploded.select(
            pl.col("prenom_explode").alias("nom"), 
            "sexe"
        ).with_columns(type=pl.lit("prenoms")),
        
        df.select(
            pl.col("nom").alias("nom"),
            "sexe"
        ).with_columns(type=pl.lit("famille"))
    ])
    .group_by("nom", "sexe", "type")
    .agg(count=pl.len())
    .pivot(
        values="count",
        index="nom",
        columns=["sexe", "type"],
        aggregate_function="sum"
    )
    .fill_null(0)
    .rename({
        '{"Féminin","famille"}': "nombre_femme_nom_famille",
        '{"Féminin","prenoms"}': "nombre_femme_prenom",
        '{"Masculin","famille"}': "nombre_homme_nom_famille",
        '{"Masculin","prenoms"}': "nombre_homme_prenom"  # Correction orthographique
    })
    
)

prenom_unique_stats = (
    df_exploded.filter(pl.col("prenoms") == pl.col("prenom_explode"))
    .group_by("prenom_explode")
    .agg(prenom_unique=pl.len())
)

final_stats = (
    stats.join(
        prenom_unique_stats,
        left_on="nom",
        right_on="prenom_explode",
        how="left"
    )
    .with_columns(
        partie_prenom=pl.col("nombre_homme_prenom") + pl.col("nombre_femme_prenom"),
        nom_famille=pl.col("nombre_homme_nom_famille") + pl.col("nombre_femme_nom_famille"),
        prenom_unique=pl.coalesce("prenom_unique", 0)
    )
    .select([
        "nom",
        "partie_prenom",
        "nom_famille",
        "prenom_unique",
        "nombre_homme_prenom",
        "nombre_homme_nom_famille",
        "nombre_femme_prenom",
        "nombre_femme_nom_famille"
    ])
)

final_stats.write_parquet(
     files_dir / "nom_prenoms_overlay_vf_lower_trim.parquet",
       compression="zstd"
)