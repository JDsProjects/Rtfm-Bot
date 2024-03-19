BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "RTFM_DICTIONARY" (
	"name"	varchar(255),
	"link"	varchar(255)
);
INSERT INTO "RTFM_DICTIONARY" ("name","link") VALUES ('dpy-latest','https://discordpy.readthedocs.io/en/stable/'),
 ('dpy-latest-jp','https://discordpy.readthedocs.io/ja/latest/'),
 ('python','https://docs.python.org/3/'),
 ('python-jp','https://docs.python.org/ja/3/'),
 ('master','https://discordpy.readthedocs.io/en/latest/'),
 ('jishaku','https://jishaku.readthedocs.io/en/latest/'),
 ('asyncpg','https://magicstack.github.io/asyncpg/current/'),
 ('tweepy','https://docs.tweepy.org/en/latest/'),
 ('aiogifs','https://aiogifs.readthedocs.io/en/latest/'),
 ('python-cse','https://python-cse.readthedocs.io/en/latest/'),
 ('wavelink','https://wavelink.readthedocs.io/en/latest/'),
 ('motor','https://motor.readthedocs.io/en/stable/'),
 ('dagpi','https://asyncdagpi.readthedocs.io/en/latest/'),
 ('pymongo','https://pymongo.readthedocs.io/en/stable/'),
 ('pymongo-latest','https://pymongo.readthedocs.io/en/latest/'),
 ('aiohttp','https://docs.aiohttp.org/en/stable/'),
 ('aiohttp-latest','https://docs.aiohttp.org/en/latest/'),
 ('wand','https://docs.wand-py.org/en/stable/'),
 ('pillow','https://pillow.readthedocs.io/en/stable/'),
 ('aiosqlite','https://aiosqlite.omnilib.dev/en/stable/'),
 ('pytube','https://pytube.io/en/latest/'),
 ('vt-py','https://virustotal.github.io/vt-py/'),
 ('black','https://black.readthedocs.io/en/stable/'),
 ('asyncpraw','https://asyncpraw.readthedocs.io/en/latest/'),
 ('edpy','https://enhanced-dpy.readthedocs.io/en/latest/'),
 ('tweepy','https://docs.tweepy.org/en/latest/');
COMMIT;
