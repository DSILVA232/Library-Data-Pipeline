SELECT 
    {{ dbt_utils.generate_surrogate_key(['role']) }} AS role_id,
    role as role_name
FROM (
    SELECT DISTINCT role
    FROM {{ref('stg_staff')}}

)