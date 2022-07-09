# pro_champ_bot
Bot that collects stats and builds from wins of pro players on your desired champion

# Stack
- Python 3.7
- Libraries:
  - beautifulsoup4 - web parsing
  - pillow - image manipulation

# Env-file template
* URL=... # url from probuildstats.com with desired champion
* TOKEN=... # your telegram bot token
* CHAT_ID=... # chat id where you want to send notifications

# Installation
Clone repository, create an env-file and fill it out according to the template above:
```
git@github.com:SpaceJesusJPG/pro_champ_bot.git
```
Change directory to the root of the project and build the image:
```
cd pro_champ_bot
```
```
docker build -t pro_champ_bot .
```
And then just run the image:
```
docker image run pro_champ_bot
```
