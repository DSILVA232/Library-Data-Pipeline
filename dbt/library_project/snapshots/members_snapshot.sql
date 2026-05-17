{ % snapshot members_snapshot %}

{{ config(
    target_schema="snapshots",
    unique_key="member_id",
    strategy="check",
    check_cols=["email","address","membership_status","city","state","postcode"] 
) 
}}

select * from {{ source('library', 'MEMBERS') }}

{% endsnapshot %}