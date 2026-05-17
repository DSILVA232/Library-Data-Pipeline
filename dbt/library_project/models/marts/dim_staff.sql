SELECT
    staff_id,
    full_name,
    b.branch_id,
    r.role_id,
    hire_date
FROM {{ref('stg_staff')}} as s

LEFT JOIN {{ref('dim_branch')}} as b 
    ON s.branch = b.branch_name

LEFT JOIN {{ref('dim_role')}} as r 
    ON s.role = r.role_name