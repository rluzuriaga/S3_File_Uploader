-- SQL needed for commit 3be354d296f1c7a42ab2267d44bb798df3209bad
-- This SQL file needs to be selected using the Update Database
--   button from the program.

ALTER TABLE ffmpeg_config RENAME TO ffmpeg_config_copy;

CREATE TABLE IF NOT EXISTS ffmpeg_config (
    ffmpeg_parameters TEXT,
    file_suffix TEXT NOT NULL,
    aws_different_output_extension TEXT,
    local_save_path TEXT,
    local_different_output_extension TEXT,
    is_active INTEGER NOT NULL
);

INSERT INTO ffmpeg_config
SELECT ffmpeg_parameters, '_converted', aws_different_output_extension, local_save_path, local_different_output_extension, is_active
FROM ffmpeg_config_copy;

DROP TABLE ffmpeg_config_copy;