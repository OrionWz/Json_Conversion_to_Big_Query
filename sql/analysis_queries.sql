-- 1) How well do inferred genders align with RandomUser's gender field?
SELECT
    gender_reported,
    gender_inferred,
    COUNT(*) AS n
FROM users
GROUP BY gender_reported, gender_inferred
ORDER BY n DESC;

-- 2) Strongest nationalize.io predictions: top inferred country and average confidence
SELECT
    nationality_inferred AS top_country_guess,
    ROUND(AVG(nationality_probability), 3) AS avg_confidence,
    COUNT(*) AS people
FROM users
WHERE nationality_inferred IS NOT NULL
GROUP BY nationality_inferred
ORDER BY people DESC, avg_confidence DESC
LIMIT 15;

-- 3) Biggest disagreements between RandomUser age and agify.io estimate
SELECT
    first_name,
    last_name,
    age_reported,
    age_inferred,
    ABS(age_reported - age_inferred) AS age_gap
FROM users
WHERE age_inferred IS NOT NULL
ORDER BY age_gap DESC
LIMIT 20;

-- 4) RandomUser nationality codes (nat) vs. nationalize's top guess
SELECT
    nationality_code AS randomuser_nat,
    nationality_inferred AS nationalize_top,
    COUNT(*) AS n
FROM users
WHERE nationality_inferred IS NOT NULL
GROUP BY nationality_code, nationality_inferred
ORDER BY n DESC
LIMIT 25;

-- 5) "High confidence" genderize predictions among names that disagree with RandomUser
SELECT
    first_name,
    last_name,
    gender_reported,
    gender_inferred,
    ROUND(gender_probability, 3) AS gender_confidence
FROM users
WHERE gender_inferred IS NOT NULL
  AND gender_reported IS NOT NULL
  AND LOWER(gender_reported) != LOWER(gender_inferred)
  AND gender_probability >= 0.85
ORDER BY gender_probability DESC
LIMIT 25;

-- 6) Average reported age by inferred gender (interesting when sample mixes many regions)
SELECT
    gender_inferred,
    ROUND(AVG(age_reported), 1) AS avg_reported_age,
    COUNT(*) AS n
FROM users
WHERE gender_inferred IS NOT NULL AND age_reported IS NOT NULL
GROUP BY gender_inferred;
