#Laban Efforts
name = input("Character name? ")

weight = input("Light or Strong? (L/S): ")
direction = input("Direct or Indirect? (D/I): ")
timing = input("Sudden or Sustained? (S/U): ")

laban = ""
if(weight == "L"):
    if(direction == "D"):
        if(timing == "S"):
            laban = "Dabbing (Light Direct Sudden)"
        elif(timing == "U"):
            laban = "Gliding (Light Direct Sustained)"
    elif(direction == "I"):
        if(timing == "S"):
            laban = "Flicking (Light Indirect Sudden)"
        elif(timing == "U"):
            laban = "Floating (Light Indirect Sustained)"
elif(weight == "S"):
    if(direction == "D"):
        if(timing == "S"):
            laban = "Thrusting (Strong Direct Sudden)"
        elif(timing == "U"):
            laban = "Pressing (Strong Direct Sustained)"
    elif(direction == "I"):
        if(timing == "S"):
            laban = "Slashing (Strong Indirect Sudden)"
        elif(timing == "U"):
            laban = "Wringing (Strong Indirect Sustained)"


age = ["How old is your character?"," Young", " Teenage", " Adult", "n Elderly"]
air = ["Is their voice nasally, throaty, or clear?","Nasally", "Breathy", "Clear"]
moisture = ["Is their voice breathy, dry, or hoarse?","Breathy", "Dry", "Hoarse"]
gender = ["Is this character Male, Female, or Neither", "Male", "Female", "Nonbinary"]
size = ["Is this character small, medium, or large", "Small", "Medium", "Large"]
tempo = ["Does this character speak slow, medium, or fast", "Slow", "Medium", "Fast"]
attitude = ["Is this character friendly, neutral, or aggressive", "Friendly", "Neutral", "Aggressive"]


def getModifier(mods: list):
    mod = int(input(mods[0]))
    return mods[mod]

age = getModifier(age)
air = getModifier(air)
moisture = getModifier(moisture)
gender = getModifier(gender)
size = getModifier(size)
tempo = getModifier(tempo)
attitude = getModifier(attitude)

notes = input("Any other notes? \n")

voice = f"{name} is a{age} {gender}. He is {size} and speaks {tempo}. His voice is {air} and {moisture}. He is {attitude} and {laban}. {notes}"
print(voice)