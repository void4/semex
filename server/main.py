from flask import Flask, render_template, request
from glob import glob
import os.path

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")#str(glob("../languages/en/*"))

@app.route("/generator")
def generator():
    from generator import concept
    definition = concept()
    return render_template("generator.html", definition=definition)

@app.route("/cultures")
def cultures():
	return render_template("cultures.html")

@app.route("/languages")
def languages():
    langs = [path.split("/")[-1] for path in glob("../languages/*")]
    return render_template("languages.html", languages=langs)

@app.route("/languages/<lang>")
def language(lang=None):
    words = [path.split("/")[-1] for path in glob("../languages/%s/*" % lang)]
    return render_template("language.html", lang=lang, words=words)

validwords = "i you someone people something thing body kind part this the same other else another one two some all much many little few good bad big small think know want don't want feel see hear say words true do happen move be somewhere there is be someone be something is mine live die when time now before after a long time a short time for some time moment where place here above below far near side inside touch contact not maybe can because if very more like as way"
validwords = validwords.split()

NSM = """Substantives
I, YOU, SOMEONE, PEOPLE, SOMETHING, THING, BODY
Relational Substantives
KIND, PART
Determiners
THIS, THE SAME, OTHER, ELSE, ANOTHER
Quantifiers
ONE, TWO, SOME, ALL, MUCH, MANY, LITTLE, FEW
Evaluators
GOOD, BAD
Descriptors
BIG, SMALL
Mental predicates
THINK, KNOW, WANT, DON'T WANT, FEEL, SEE, HEAR
Speech
SAY, WORDS, TRUE
Actions, Events, Movement
DO, HAPPEN, MOVE
Existence, Possession
BE SOMEWHERE, THERE IS, BE SOMEONE, BE SOMETHING ,IS, MINE
Life and Death
LIVE, DIE
Time
WHEN, TIME, NOW, BEFORE, AFTER, A LONG TIME, A SHORT TIME, FOR SOME TIME, MOMENT
Space
WHERE, PLACE, HERE, ABOVE, BELOW, FAR, NEAR, SIDE, INSIDE, TOUCH, CONTACT
Logical Concepts
NOT, MAYBE, CAN, BECAUSE, IF
Intensifier, Augmentor
VERY, MORE
Similarity
LIKE, AS, WAY"""

def define(lang, name, definition):
    definition = definition.strip()
    if len(definition) == 0:
        return False, "Empty definition."


    definition = definition.lower()
    words = definition.split()

    invalidwords = []
    for word in words:
        if word not in validwords:
            invalidwords.append(word)

    if invalidwords:
        return False, "Invalid words: " + ",".join(invalidwords)

    finaldef = " ".join(words)

    path = "../languages/%s/%s" % (lang, name)

    prefix = "\n\n"

    try:
        f = open(path, "r")
        defs = f.read().split("\n\n")
        f.close()

        if finaldef in defs:
            return False, "This definition already exists."
    except FileNotFoundError:
        prefix = ""
        pass

    f = open(path, "a")
    f.write(prefix + finaldef)
    f.close()
    return True, "Definition submitted. Thank you."

@app.route("/languages/<lang>/<word>", methods=['GET', 'POST'])
def word(lang=None, word=None):
    print(request.args)
    result = ""
    definition = ""
    if "definition" in request.form:
        result = define(lang, word, request.form["definition"])
        if not result[0]:
            definition = request.form["definition"]
        result = result[1]
    definitions = [open(path).read() for path in glob("../languages/%s/%s" % (lang, word))]
    #", ".join(validwords)
    return render_template("word.html", lang=lang, word=word, definitions=definitions, definition=definition, allowedwords=NSM, result=result)

app.run("0.0.0.0", 8080, debug=True)
