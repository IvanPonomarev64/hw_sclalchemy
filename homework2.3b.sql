create table if not exists genre (
	id serial primary key,
	genre_name varchar(100) not null unique
);
create table if not exists executor (
	id serial primary key,
	executor_name varchar(100) not null	
);
create table if not exists genre_executor (
    genre_id integer references genre(id),
    executor_id integer references executor(id),
    constraint genre_executor_pk primary key (genre_id, executor_id)
);
create table if not exists album (
	id serial primary key,
	album_name varchar(100) not null,
	year_of_release integer not null
);
create table if not exists executor_album (
    executor_id integer references executor(id),
    album_id integer references album(id),
    constraint executor_album_pk primary key (executor_id, album_id)
);
create table if not exists track (
	id serial primary key,
	track_name varchar(100) not null unique,
	duration integer not null,
	album_id integer references album(id)
);
create table if not exists collection_of_songs (
    id serial primary key,
    collection_name varchar(100) not null unique,
    year_of_release integer not null
);
create table if not exists track_collection (
    track_id integer references track(id),
    collection_of_songs_id integer references collection_of_songs(id),
    constraint track_collection_pk primary key (track_id, collection_of_songs_id)
);