SELECT 
    quarter1_job_posting.job_location,
    quarter1_job_posting.job_via,
    quarter1_job_posting.job_posted_date::DATE,
    quarter1_job_posting.salary_year_avg
FROM (
    SELECT *
    FROM january_jobs
    UNION ALL
    SELECT *
    FROM february_jobs
    UNION ALL
    SELECT *
    FROM march_jobs
) AS quarter1_job_posting

WHERE
 quarter1_job_posting.salary_year_avg > 70000 AND quarter1_job_posting.job_title_short = 'Data Analyst'
ORDER BY
    quarter1_job_posting.salary_year_avg DESC