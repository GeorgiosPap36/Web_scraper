USE movies;

SELECT d.name AS director_name, COUNT(m.id) AS movie_count
FROM Directors d
LEFT JOIN Movies m ON d.id = m.director_id
GROUP BY d.id
ORDER BY movie_count DESC;

SELECT SUM(movie_count) AS total_movies
FROM (
    SELECT COUNT(m.id) AS movie_count
    FROM Directors d
    LEFT JOIN Movies m ON d.id = m.director_id
    GROUP BY d.id
) AS counts;

SELECT d.name AS genre, COUNT(m.id) AS movie_count
FROM Genres d
LEFT JOIN Movies m ON d.id = m.genre_id
GROUP BY d.id
ORDER BY movie_count DESC;

SELECT SUM(movie_count) AS total_movies
FROM (
    SELECT COUNT(m.id) AS movie_count
    FROM Genres d
    LEFT JOIN Movies m ON d.id = m.genre_id
    GROUP BY d.id
) AS counts;

SELECT d.name AS country_name, COUNT(m.id) AS movie_count
FROM Countries d
LEFT JOIN Movies m ON d.id = m.country_id
GROUP BY d.id
ORDER BY movie_count DESC;

SELECT SUM(movie_count) AS total_movies
FROM (
    SELECT COUNT(m.id) AS movie_count
    FROM Countries d
    LEFT JOIN Movies m ON d.id = m.country_id
    GROUP BY d.id
) AS counts;

WITH age_rating_counts AS (
    SELECT d.name AS country_name, COUNT(m.id) AS movie_count
    FROM AgeRatings d
    LEFT JOIN Movies m ON d.id = m.age_rating_id
    GROUP BY d.id
)
SELECT country_name, movie_count, 
       (SELECT SUM(movie_count) FROM age_rating_counts) AS total_movies
FROM age_rating_counts
ORDER BY movie_count DESC;

WITH high_score_movies AS (
    SELECT id, name, score, release_year
    FROM movies
    WHERE score > 8.5
)
SELECT id, name, score, release_year, 
       (SELECT COUNT(*) FROM high_score_movies) AS movie_count
FROM high_score_movies
ORDER BY release_year DESC;
