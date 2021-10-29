#!/usr/bin/env python3
import discord
import markovify
import sqlite3
import time
import os
import sys
import random

denychannels = [320301531687682059]
adjs = ["abandoned", "able", "absolute", "adorable", "adventurous", "academic", "acceptable", "acclaimed", "accomplished", "accurate", "aching", "acidic", "acrobatic", "active", "actual", "adept", "admirable", "admired", "adolescent", "adorable", "adored", "advanced", "afraid", "affectionate", "aged", "aggravating", "aggressive", "agile", "agitated", "agonizing", "agreeable", "ajar", "alarmed", "alarming", "alert", "alienated", "alive", "all", "altruistic", "amazing", "ambitious", "ample", "amused", "amusing", "anchored", "ancient", "angelic", "angry", "anguished", "animated", "annual", "another", "antique", "anxious", "any", "apprehensive", "appropriate", "apt", "arctic", "arid", "aromatic", "artistic", "ashamed", "assured", "astonishing", "athletic", "attached", "attentive", "attractive", "austere", "authentic", "authorized", "automatic", "avaricious", "average", "aware", "awesome", "awful", "awkward", "babyish", "bad", "back", "baggy", "bare", "barren", "basic", "beautiful", "belated", "beloved", "beneficial", "better", "best", "bewitched", "big", "big-hearted", "biodegradable", "bite-sized", "bitter", "black", "black-and-white", "bland", "blank", "blaring", "bleak", "blind", "blissful", "blond", "blue", "blushing", "bogus", "boiling", "bold", "bony", "boring", "bossy", "both", "bouncy", "bountiful", "bowed", "brave", "breakable", "brief", "bright", "brilliant", "brisk", "broken", "bronze", "brown", "bruised", "bubbly", "bulky", "bumpy", "buoyant", "burdensome", "burly", "bustling", "busy", "buttery", "buzzing", "calculating", "calm", "candid", "canine", "capital", "carefree", "careful", "careless", "caring", "cautious", "cavernous", "celebrated", "charming", "cheap", "cheerful", "cheery", "chief", "chilly", "chubby", "circular", "classic", "clean", "clear", "clear-cut", "clever", "close", "closed", "cloudy", "clueless", "clumsy", "cluttered", "coarse", "cold", "colorful", "colorless", "colossal", "comfortable", "common", "compassionate", "competent", "complete", "complex", "complicated", "composed", "concerned", "concrete", "confused", "conscious", "considerate", "constant", "content", "conventional", "cooked", "cool", "cooperative", "coordinated", "corny", "corrupt", "costly", "courageous", "courteous", "crafty", "crazy", "creamy", "creative", "creepy", "criminal", "crisp", "critical", "crooked", "crowded", "cruel", "crushing", "cuddly", "cultivated", "cultured", "cumbersome", "curly", "curvy", "cute", "cylindrical", "damaged", "damp", "dangerous", "dapper", "daring", "darling", "dark", "dazzling", "dead", "deadly", "deafening", "dear", "dearest", "decent", "decimal", "decisive", "deep", "defenseless", "defensive", "defiant", "deficient", "definite", "definitive", "delayed", "delectable", "delicious", "delightful", "delirious", "demanding", "dense", "dental", "dependable", "dependent", "descriptive", "deserted", "detailed", "determined", "devoted", "different", "difficult", "digital", "diligent", "dim", "dimpled", "dimwitted", "direct", "disastrous", "discrete", "disfigured", "disgusting", "disloyal", "dismal", "distant", "downright", "dreary", "dirty", "disguised", "dishonest", "dismal", "distant", "distinct", "distorted", "dizzy", "dopey", "doting", "double", "downright", "drab", "drafty", "dramatic", "dreary", "droopy", "dry", "dual", "dull", "dutiful", "each", "eager", "earnest", "early", "easy", "easy-going", "ecstatic", "edible", "educated", "elaborate", "elastic", "elated", "elderly", "electric", "elegant", "elementary", "elliptical", "embarrassed", "embellished", "eminent", "emotional", "empty", "enchanted", "enchanting", "energetic", "enlightened", "enormous", "enraged", "entire", "envious", "equal", "equatorial", "essential", "esteemed", "ethical", "euphoric", "even", "evergreen", "everlasting", "every", "evil", "exalted", "excellent", "exemplary", "exhausted", "excitable", "excited", "exciting", "exotic", "expensive", "experienced", "expert", "extraneous", "extroverted", "extra-large", "extra-small", "fabulous", "failing", "faint", "fair", "faithful", "fake", "false", "familiar", "famous", "fancy", "fantastic", "far", "faraway", "far-flung", "far-off", "fast", "fat", "fatal", "fatherly", "favorable", "favorite", "fearful", "fearless", "feisty", "feline", "female", "feminine", "few", "fickle", "filthy", "fine", "finished", "firm", "first", "firsthand", "fitting", "fixed", "flaky", "flamboyant", "flashy", "flat", "flawed", "flawless", "flickering", "flimsy", "flippant", "flowery", "fluffy", "fluid", "flustered", "focused", "fond", "foolhardy", "foolish", "forceful", "forked", "formal", "forsaken", "forthright", "fortunate", "fragrant", "frail", "frank", "frayed", "free", "French", "fresh", "frequent", "friendly", "frightened", "frightening", "frigid", "frilly", "frizzy", "frivolous", "front", "frosty", "frozen", "frugal", "fruitful", "full", "fumbling", "functional", "funny", "fussy", "fuzzy", "gargantuan", "gaseous", "general", "generous", "gentle", "genuine", "giant", "giddy", "gigantic", "gifted", "giving", "glamorous", "glaring", "glass", "gleaming", "gleeful", "glistening", "glittering", "gloomy", "glorious", "glossy", "glum", "golden", "good", "good-natured", "gorgeous", "graceful", "gracious", "grand", "grandiose", "granular", "grateful", "grave", "gray", "great", "greedy", "green", "gregarious", "grim", "grimy", "gripping", "grizzled", "gross", "grotesque", "grouchy", "grounded", "growing", "growling", "grown", "grubby", "gruesome", "grumpy", "guilty", "gullible", "gummy", "hairy", "half", "handmade", "handsome", "handy", "happy", "happy-go-lucky", "hard", "hard-to-find", "harmful", "harmless", "harmonious", "harsh", "hasty", "hateful", "haunting", "healthy", "heartfelt", "hearty", "heavenly", "heavy", "hefty", "helpful", "helpless", "hidden", "hideous", "high", "high-level", "hilarious", "hoarse", "hollow", "homely", "honest", "honorable", "honored", "hopeful", "horrible", "hospitable", "hot", "huge", "humble", "humiliating", "humming", "humongous", "hungry", "hurtful", "husky", "icky", "icy", "ideal", "idealistic", "identical", "idle", "idiotic", "idolized", "ignorant", "ill", "illegal", "ill-fated", "ill-informed", "illiterate", "illustrious", "imaginary", "imaginative", "immaculate", "immaterial", "immediate", "immense", "impassioned", "impeccable", "impartial", "imperfect", "imperturbable", "impish", "impolite", "important", "impossible", "impractical", "impressionable", "impressive", "improbable", "impure", "inborn", "incomparable", "incompatible", "incomplete", "inconsequential", "incredible", "indelible", "inexperienced", "indolent", "infamous", "infantile", "infatuated", "inferior", "infinite", "informal", "innocent", "insecure", "insidious", "insignificant", "insistent", "instructive", "insubstantial", "intelligent", "intent", "intentional", "interesting", "internal", "international", "intrepid", "ironclad", "irresponsible", "irritating", "itchy", "jaded", "jagged", "jam-packed", "jaunty", "jealous", "jittery", "joint", "jolly", "jovial", "joyful", "joyous", "jubilant", "judicious", "juicy", "jumbo", "junior", "jumpy", "juvenile", "kaleidoscopic", "keen", "key", "kind", "kindhearted", "kindly", "klutzy", "knobby", "knotty", "knowledgeable", "knowing", "known", "kooky", "kosher", "lame", "lanky", "large", "last", "lasting", "late", "lavish", "lawful", "lazy", "leading", "lean", "leafy", "left", "legal", "legitimate", "light", "lighthearted", "likable", "likely", "limited", "limp", "limping", "linear", "lined", "liquid", "little", "live", "lively", "livid", "loathsome", "lone", "lonely", "long", "long-term", "loose", "lopsided", "lost", "loud", "lovable", "lovely", "loving", "low", "loyal", "lucky", "lumbering", "luminous", "lumpy", "lustrous", "luxurious", "mad", "made-up", "magnificent", "majestic", "major", "male", "mammoth", "married", "marvelous", "masculine", "massive", "mature", "meager", "mealy", "mean", "measly", "meaty", "medical", "mediocre", "medium", "meek", "mellow", "melodic", "memorable", "menacing", "merry", "messy", "metallic", "mild", "milky", "mindless", "miniature", "minor", "minty", "miserable", "miserly", "misguided", "misty", "mixed", "modern", "modest", "moist", "monstrous", "monthly", "monumental", "moral", "mortified", "motherly", "motionless", "mountainous", "muddy", "muffled", "multicolored", "mundane", "murky", "mushy", "musty", "muted", "mysterious", "naive", "narrow", "nasty", "natural", "naughty", "nautical", "near", "neat", "necessary", "needy", "negative", "neglected", "negligible", "neighboring", "nervous", "new", "next", "nice", "nifty", "nimble", "nippy", "nocturnal", "noisy", "nonstop", "normal", "notable", "noted", "noteworthy", "novel", "noxious", "numb", "nutritious", "nutty", "obedient", "obese", "oblong", "oily", "oblong", "obvious", "occasional", "odd", "oddball", "offbeat", "offensive", "official", "old", "old-fashioned", "only", "open", "optimal", "optimistic", "opulent", "orange", "orderly", "organic", "ornate", "ornery", "ordinary", "original", "other", "our", "outlying", "outgoing", "outlandish", "outrageous", "outstanding", "oval", "overcooked", "overdue", "overjoyed", "overlooked", "palatable", "pale", "paltry", "parallel", "parched", "partial", "passionate", "past", "pastel", "peaceful", "peppery", "perfect", "perfumed", "periodic", "perky", "personal", "pertinent", "pesky", "pessimistic", "petty", "phony", "physical", "piercing", "pink", "pitiful", "plain", "plaintive", "plastic", "playful", "pleasant", "pleased", "pleasing", "plump", "plush", "polished", "polite", "political", "pointed", "pointless", "poised", "poor", "popular", "portly", "posh", "positive", "possible", "potable", "powerful", "powerless", "practical", "precious", "present", "prestigious", "pretty", "precious", "previous", "pricey", "prickly", "primary", "prime", "pristine", "private", "prize", "probable", "productive", "profitable", "profuse", "proper", "proud", "prudent", "punctual", "pungent", "puny", "pure", "purple", "pushy", "putrid", "puzzled", "puzzling", "quaint", "qualified", "quarrelsome", "quarterly", "queasy", "querulous", "questionable", "quick", "quick-witted", "quiet", "quintessential", "quirky", "quixotic", "quizzical", "radiant", "ragged", "rapid", "rare", "rash", "raw", "recent", "reckless", "rectangular", "ready", "real", "realistic", "reasonable", "red", "reflecting", "regal", "regular", "reliable", "relieved", "remarkable", "remorseful", "remote", "repentant", "required", "respectful", "responsible", "repulsive", "revolving", "rewarding", "rich", "rigid", "right", "ringed", "ripe", "roasted", "robust", "rosy", "rotating", "rotten", "rough", "round", "rowdy", "royal", "rubbery", "rundown", "ruddy", "rude", "runny", "rural", "rusty", "sad", "safe", "salty", "same", "sandy", "sane", "sarcastic", "sardonic", "satisfied", "scaly", "scarce", "scared", "scary", "scented", "scholarly", "scientific", "scornful", "scratchy", "scrawny", "second", "secondary", "second-hand", "secret", "self-assured", "self-reliant", "selfish", "sentimental", "separate", "serene", "serious", "serpentine", "several", "severe", "shabby", "shadowy", "shady", "shallow", "shameful", "shameless", "sharp", "shimmering", "shiny", "shocked", "shocking", "shoddy", "short", "short-term", "showy", "shrill", "shy", "sick", "silent", "silky", "silly", "silver", "similar", "simple", "simplistic", "sinful", "single", "sizzling", "skeletal", "skinny", "sleepy", "slight", "slim", "slimy", "slippery", "slow", "slushy", "small", "smart", "smoggy", "smooth", "smug", "snappy", "snarling", "sneaky", "sniveling", "snoopy", "sociable", "soft", "soggy", "solid", "somber", "some", "spherical", "sophisticated", "sore", "sorrowful", "soulful", "soupy", "sour", "Spanish", "sparkling", "sparse", "specific", "spectacular", "speedy", "spicy", "spiffy", "spirited", "spiteful", "splendid", "spotless", "spotted", "spry", "square", "squeaky", "squiggly", "stable", "staid", "stained", "stale", "standard", "starchy", "stark", "starry", "steep", "sticky", "stiff", "stimulating", "stingy", "stormy", "straight", "strange", "steel", "strict", "strident", "striking", "striped", "strong", "studious", "stunning", "stupendous", "stupid", "sturdy", "stylish", "subdued", "submissive", "substantial", "subtle", "suburban", "sudden", "sugary", "sunny", "super", "superb", "superficial", "superior", "supportive", "sure-footed", "surprised", "suspicious", "svelte", "sweaty", "sweet", "sweltering", "swift", "sympathetic", "tall", "talkative", "tame", "tan", "tangible", "tart", "tasty", "tattered", "taut", "tedious", "teeming", "tempting", "tender", "tense", "tepid", "terrible", "terrific", "testy", "thankful", "that", "these", "thick", "thin", "third", "thirsty", "this", "thorough", "thorny", "those", "thoughtful", "threadbare", "thrifty", "thunderous", "tidy", "tight", "timely", "tinted", "tiny", "tired", "torn", "total", "tough", "traumatic", "treasured", "tremendous", "tragic", "trained", "tremendous", "triangular", "tricky", "trifling", "trim", "trivial", "troubled", "true", "trusting", "trustworthy", "trusty", "truthful", "tubby", "turbulent", "twin", "ugly", "ultimate", "unacceptable", "unaware", "uncomfortable", "uncommon", "unconscious", "understated", "unequaled", "uneven", "unfinished", "unfit", "unfolded", "unfortunate", "unhappy", "unhealthy", "uniform", "unimportant", "unique", "united", "unkempt", "unknown", "unlawful", "unlined", "unlucky", "unnatural", "unpleasant", "unrealistic", "unripe", "unruly", "unselfish", "unsightly", "unsteady", "unsung", "untidy", "untimely", "untried", "untrue", "unused", "unusual", "unwelcome", "unwieldy", "unwilling", "unwitting", "unwritten", "upbeat", "upright", "upset", "urban", "usable", "used", "useful", "useless", "utilized", "utter", "vacant", "vague", "vain", "valid", "valuable", "vapid", "variable", "vast", "velvety", "venerated", "vengeful", "verifiable", "vibrant", "vicious", "victorious", "vigilant", "vigorous", "villainous", "violet", "violent", "virtual", "virtuous", "visible", "vital", "vivacious", "vivid", "voluminous", "wan", "warlike", "warm", "warmhearted", "warped", "wary", "wasteful", "watchful", "waterlogged", "watery", "wavy", "wealthy", "weak", "weary", "webbed", "wee", "weekly", "weepy", "weighty", "weird", "welcome", "well-documented", "well-groomed", "well-informed", "well-lit", "well-made", "well-off", "well-to-do", "well-worn", "wet", "which", "whimsical", "whirlwind", "whispered", "white", "whole", "whopping", "wicked", "wide", "wide-eyed", "wiggly", "wild", "willing", "wilted", "winding", "windy", "winged", "wiry", "wise", "witty", "wobbly", "woeful", "wonderful", "wooden", "woozy", "wordy", "worldly", "worn", "worried", "worrisome", "worse", "worst", "worthless", "worthwhile", "worthy", "wrathful", "wretched", "writhing", "wrong", "wry", "yawning", "yearly", "yellow", "yellowish", "young", "youthful", "yummy", "zany", "zealous", "zesty", "zigzag"]

connection = sqlite3.connect("messages.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS messages (userid INTEGER, messageid INTEGER UNIQUE, chanid INTEGER, message TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS users (userid INTEGER UNIQUE, user TEXT);")
connection.commit()

async def getMemberName(personId):
    for guild in client.guilds:
        for memb in guild.members:
            if memb.id == personId:
                name = memb.nick
                if name is None:
                    name = memb.name
                return name

async def getChannelName(chanId):
    for guild in client.guilds:
        for chan in guild.text_channels:
            if chan.id == chanId:
                return chan.name


async def getMessages():
    count = 0
    cursor = connection.cursor()
    for guild in client.guilds:
        for chan in guild.text_channels:
            if chan.id in denychannels:
                continue
            print("Reading from", chan)
            async for message in chan.history(limit=None):
                count += 1
                if "markov" in message.content:
                    continue
                if "!spy" in message.content:
                    continue
                cursor.execute("INSERT OR IGNORE INTO messages (userid, messageid, chanid, message) VALUES (?, ?, ?, ?);", (message.author.id, message.id, message.channel.id, message.content))
            print("Currently at ", count)
            connection.commit()

async def totalCount(channel):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) from messages;")
    messageCount = cursor.fetchone()[0]
    await channel.send("There are a total of {} messages stored in my database".format(messageCount))

async def leaderboard(channel):
    cursor = connection.cursor()
    msg = "Most spammy chatters\n"
    num = 5
    for row in cursor.execute("SELECT userid, COUNT(*) as cnt from messages GROUP BY userid ORDER BY cnt DESC;"):
        name = await getMemberName(row[0])
        msg += "{}\t{}\n".format(name, row[1])
        num -= 1
        if num <= 0:
            break
    await channel.send(msg)

async def leaderboardChannels(channel):
    cursor = connection.cursor()
    msg = "Channel Stats\n"
    for row in cursor.execute("SELECT chanid, COUNT(*) as cnt from messages WHERE chanid IS NOT NULL GROUP BY chanid ORDER BY cnt DESC;"):
        name = await getChannelName(row[0])
        msg += "{}\t{}\n".format(name, row[1])
    await channel.send(msg)


async def countUser(message):
    data = message.content.split(' ')
    if len(data) < 2:
        return
    personId = int(data[1][3:data[1].find('>')])
    for guild in client.guilds:
        for memb in guild.members:
            if memb.id == personId:
                name = memb.nick
                if name is None:
                    name = memb.name
                cursor = connection.cursor()
                cursor.execute("SELECT COUNT(*) from messages WHERE userid = {};".format(personId))
                messageCount = cursor.fetchone()[0]
                await message.channel.send("I found {} messaages for {}".format(messageCount, name))

async def getMessageText(authorId):
    cursor = connection.cursor()
    m_text = ""
    for row in cursor.execute("SELECT * FROM messages WHERE userid = {};".format(authorId)):
        m_text += row[3] + "\n"
    return m_text

async def markovDance(author, author2, channel):

    msgText = await getMessageText(author.id)
    msgText2 = await getMessageText(author2.id)

    name1 = await getMemberName(author.id)
    name2 = await getMemberName(author2.id)

    text_model_author = markovify.NewlineText(msgText)
    text_model_author2 = markovify.NewlineText(msgText2)

    fusion_model = markovify.combine([text_model_author, text_model_author2], [1, 1.75])
    to_say = fusion_model.make_sentence(tries=1000)
    if to_say is None:
        await channel.send("I failed to create a hybrid message, maybe try again")
    elif "@" in to_say:
        await channel.send("There was an @ in the message I generated so I threw it away, try again")
    else:
        adj = random.choice(adjs)
        await channel.send("A {} combination of {} and {} said \"{}\"".format(adj, name1, name2, to_say))


async def markovEveryone(channel):
    start = time.time()
    cursor = connection.cursor()
    m_text = ""
    for row in cursor.execute("SELECT * FROM messages;"):
        m_text += row[3] + "\n"
    
    text_model = markovify.NewlineText(m_text)

    to_say = text_model.make_sentence(tries=1000)
    if to_say is None:
        await channel.send("I failed to create a hybrid message, maybe try again")
    elif "@" in to_say:
        await channel.send("There was an @ in the message I generated so I threw it away, try again")
    else:
        adj = random.choice(adjs)
        await channel.send("A {} combination of everyone who has said anything ever, said \"{}\"".format(adj, to_say))
    end = time.time()
    print("Time to do everyone", end - start)

async def doMarkov(author, channel, numSentences=1, stateSize=2):
    cursor = connection.cursor()
    m_text = ""

    name = author.nick
    if name is None:
        name = author.name

    print("markoving ", name)
    cursor.execute("SELECT COUNT(*) from messages WHERE userid = {};".format(author.id))
    messageCount = cursor.fetchone()[0]
    print(messageCount)

    for row in cursor.execute("SELECT * FROM messages WHERE userid = {};".format(author.id)):
        m_text += row[3] + "\n"

    text_model = markovify.NewlineText(m_text, state_size=stateSize)

    said = ""
    for i in range(numSentences):
        sent = text_model.make_sentence(tries=1000)
        if sent is None:
            continue
        else:
            if "@" in sent:
                continue
            if i == numSentences - 1:
                said += "{}.".format(sent)
            else:
                said += "{}. ".format(sent)
    if said == "":
        await channel.send("Couldn't markov for ya with those arguments.")
    else:
        await channel.send("'{}' said, \"{}\"".format(name, said))

intent = discord.Intents.all()
client = discord.Client(intents=intent)

@client.event
async def on_ready():
    print('We have logged in at {}'.format(time.time()))
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) from messages;")
    messageCount = cursor.fetchone()[0]
    print("We have a total message count of", messageCount)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.content.startswith('!markovme'):
        args = message.content.split(' ')
        numSentences = 1
        stateSize = 2
        if len(args) > 1:
            try:
                numSentences = int(args[1])
            except:
                return
        if len(args) > 2:
            try:
                stateSize = int(args[2])
            except:
                return
        await doMarkov(message.author, message.channel, numSentences, stateSize)

    elif message.content.startswith('!markovthem'):
        data = message.content.split(' ')
        if len(data) < 2:
            return
        personId = int(data[1][3:data[1].find('>')])
        for guild in client.guilds:
            for memb in guild.members:
                if memb.id == personId:
                    await doMarkov(memb, message.channel) 
                    return
    elif message.content.startswith('!markovdance'):
        data = message.content.split(' ')
        if len(data) < 2:
            return
        personId = int(data[1][3:data[1].find('>')])
        for guild in client.guilds:
            for memb in guild.members:
                if memb.id == personId:
                    await markovDance(message.author, memb, message.channel)
                    return
    elif message.content.startswith('!markovhelp'):
        await message.channel.send("Rob wrote this. Use !markovme to have a markov chain generated based on your chat.")        
    elif message.content.startswith('!count'):
        await countUser(message)
    elif message.content.startswith('!total'):
        await totalCount(message.channel)
    elif message.content.startswith('!chatty'):
        await leaderboard(message.channel)
    elif message.content.startswith('!channels'):
        await leaderboardChannels(message.channel)
    elif message.content.startswith('!markovforest'):
        await markovEveryone(message.channel)
    else:
        if message.channel.id in denychannels:
            return
        cursor = connection.cursor()
        cursor.execute("INSERT OR IGNORE INTO messages (userid, messageid, message) VALUES (?, ?, ?);", (message.author.id, message.id, message.content))
        connection.commit()
        

tok = ""
if os.path.exists('token'):
    tfile = open('token', 'r')
    tok = tfile.read()
else:
    tok = os.environ['DISCORD_TOKEN']

if tok == "":
    print("No token provided", file=sys.stderr)

client.run(tok)
