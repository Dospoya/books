CREATE TYPE contributor_role as ENUM ('author', 'editor', 'illustrator');

CREATE TABLE audit (
    created_at TIMESTAMPTZ DEFAULT now (),
    updated_at TIMESTAMPTZ DEFAULT now ()
);

CREATE TABLE book (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    rating DECIMAL(3, 1) CHECK (rating BETWEEN 0.0 AND 10.0),
    description TEXT,
    published_year INT CHECK (published_year BETWEEN 1450 AND 2100)
) INHERITS (audit);

CREATE TABLE genre (id UUID PRIMARY KEY, name TEXT UNIQUE NOT NULL) INHERITS (audit);

CREATE TABLE contributor (id UUID PRIMARY KEY, full_name TEXT NOT NULL) INHERITS (audit);

CREATE TABLE book_genre (
    book_id UUID REFERENCES book (id) ON DELETE CASCADE,
    genre_id UUID REFERENCES genre (id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, genre_id)
) INHERITS (audit);

CREATE TABLE book_contributor (
    book_id UUID REFERENCES book (id) ON DELETE CASCADE,
    contributor_id UUID REFERENCES contributor (id) ON DELETE CASCADE,
    role contributor_role NOT NULL,
    PRIMARY KEY (book_id, contributor_id, role)
) INHERITS (audit);
