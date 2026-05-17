SELECT *
FROM {{ref('fact_loans')}}
WHERE due_date < loan_date

UNION ALL

SELECT *
FROM {{ref('fact_loans')}}
WHERE return_date < loan_date

UNION ALL


SELECT *
FROM {{ref('fact_loans')}}
WHERE return_date > due_date and is_late = False

UNION ALL

SELECT *
FROM {{ref('fact_loans')}}
WHERE return_date <= due_date and is_late = True