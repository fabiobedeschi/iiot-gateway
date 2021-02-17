create table waste_bins (
    uuid text primary key not null,
    filling int not null,
    max_filling int not null,
    created_at timestamp with time zone not null default NOW(),
    updated_at timestamp with time zone not null default NOW()
);

create table users (
    uuid text primary key not null,
    delta int not null,
    created_at timestamp with time zone not null default NOW(),
    updated_at timestamp with time zone not null default NOW()
);
