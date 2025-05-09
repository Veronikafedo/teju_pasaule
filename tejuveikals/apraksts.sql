SELECT
    "teja"."nosaukums",
    "teja"."cena",
    "teja"."foto",
    "teja"."sastavs",
    "veikals"."vnosaukums"
FROM
    "teja"
    LEFT JOIN "veikals" ON "teja"."veikala_id" = "veikals"."id";


SELECT
    "iepakojums"."veids",
    "iepakojums"."masa"
    -- "teja"."id",
    -- "teja"."nosaukums"
FROM
    "teja"
    LEFT JOIN "iepakojums" ON "teja"."iepakojuma_id" = "iepakojums"."id";



SELECT
    "teja"."id",
    "teja"."nosaukums",
    "teja"."cena",
    "teja"."foto",
    "teja"."sastavs",
    "veikals"."vnosaukums",
    "iepakojums"."veids",
    "iepakojums"."masa",
    "razotajs"."name"
FROM
    "teja"
    LEFT JOIN "veikals" ON "teja"."veikala_id" = "veikals"."id"
    LEFT JOIN "iepakojums" ON "teja"."iepakojuma_id" = "iepakojums"."id"
    LEFT JOIN "razotajs" ON "teja"."razotaja_id" = "razotajs"."id";