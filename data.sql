BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "RTFM_DICTIONARY" (
	"name"	TEXT,
	"link"	TEXT
);
INSERT INTO "RTFM_DICTIONARY" ("name","link") VALUES ('aiogifs','https://aiogifs.readthedocs.io/en/latest/'),
 ('aiosqlite','https://aiosqlite.omnilib.dev/en/stable/'),
 ('dagpi','https://asyncdagpi.readthedocs.io/en/latest/'),
 ('asyncpraw','https://asyncpraw.readthedocs.io/en/latest/'),
 ('black','https://black.readthedocs.io/en/stable/'),
 ('master','https://discordpy.readthedocs.io/en/latest/'),
 ('dpy-latest-jp','https://discordpy.readthedocs.io/ja/latest/'),
 ('aiohttp-latest','https://docs.aiohttp.org/en/latest/'),
 ('aiohttp','https://docs.aiohttp.org/en/stable/'),
 ('python','https://docs.python.org/3/'),
 ('python-jp','https://docs.python.org/ja/3/'),
 ('sqlalchemy','https://docs.sqlalchemy.org/en/20/'),
 ('tweepy','https://docs.tweepy.org/en/latest/'),
 ('wand','https://docs.wand-py.org/en/stable/'),
 ('fastapi','https://fastapi.tiangolo.com/'),
 ('jishaku','https://jishaku.readthedocs.io/en/latest/'),
 ('asyncpg','https://magicstack.github.io/asyncpg/current/'),
 ('motor','https://motor.readthedocs.io/en/stable/'),
 ('pillow','https://pillow.readthedocs.io/en/stable/'),
 ('pymongo-latest','https://pymongo.readthedocs.io/en/latest/'),
 ('pymongo','https://pymongo.readthedocs.io/en/stable/'),
 ('python-cse','https://python-cse.readthedocs.io/en/latest/'),
 ('pytube','https://pytube.io/en/latest/'),
 ('quart','https://quart.palletsprojects.com/en/latest/'),
 ('vt-py','https://virustotal.github.io/vt-py/'),
 ('wavelink','https://wavelink.readthedocs.io/en/latest/');
COMMIT;
