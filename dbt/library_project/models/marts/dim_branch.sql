SELECT 
    {{ dbt_utils.generate_surrogate_key(['branch']) }} AS branch_id,
    branch as branch_name
FROM (
    SELECT DISTINCT branch
    FROM {{ref('stg_staff')}}

)