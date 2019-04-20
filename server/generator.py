from random import choice, random, randint

p = """Substantives
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
LIKE, AS, WAY""".split("\n")

grammar = """
substantives = subst word*
similarity = word* sim word*
"""

d = {}

for i, line in enumerate(p):
	if i%2 == 0:
		d[line] = [w.strip() for w in p[i+1].split(",")]


words = sum(d.values(), [])
words = [w.lower() for w in words]

#print(sum([len(v) for v in d.values()]))
#print(words)
#print(" ".join(list(d.keys())))

def concept(l=10,p=0.1):
	"""p is probability of nested concept"""
	text = ""
	for i in range(randint(1,l)):
		# Increase length of nested concepts?
		text += (choice(words) if random()>p else "(" + concept(l//2) + ")") + " "

	text = text.strip()
	#print("RETURNING", text)
	return text

# Construct random tree
if __name__ == "__main__":
	print(concept())

