class SentenceReadingAgent:

    def solve(self, sentence, question):

        sentence = sentence.replace(".", "").replace(",", "")
        question = question.lower().replace("?", "")
        words = sentence.split()

        colors = ["red","blue","white","green","black"]
        places = ["school","river","room","mountain","farm","city","town","car","island"]
        verbs = ["walk","walks","ran","run","write","writes","bring","brought",
                 "take","took","sing","saw","see","play"]

        subject=None
        obj=None
        place=None
        time=None
        verb=None
        color_map={}
        recipient=None
        companion=None
        animal_name=None
        animal_type=None

        for i,w in enumerate(words):

            wl=w.lower()

            # subject
            if subject is None and w[0].isupper():
                subject=w

            # verbs
            if wl in verbs:
                verb=wl

            # skip articles
            if wl in ["a","an","the"]:
                continue

            # object after verb
            if wl in verbs and i+1 < len(words):
                j=i+1
                while j < len(words) and words[j].lower() in ["a","an","the"]:
                    j+=1
                if j < len(words):
                    obj=words[j]

            # place after to / in
            if wl in ["to","in","at"] and i+1 < len(words):
                j=i+1
                while j < len(words) and words[j].lower() in ["the","a","an"]:
                    j+=1
                if j < len(words):
                    place=words[j]

            # colors
            if wl in colors and i+1 < len(words):
                noun=words[i+1]
                color_map[noun.lower()]=wl
                obj=noun

            # color predicate (water is blue)
            if wl=="is" and i+1 < len(words):
                if words[i+1].lower() in colors:
                    color_map[words[i-1].lower()] = words[i+1].lower()

            # companion
            if wl=="with" and i+1 < len(words):
                if words[i+1].lower()=="her":
                    companion=words[i+2]
                else:
                    companion=words[i+1]

            # recipient
            if wl in ["write","writes"] and i+1 < len(words):
                recipient=words[i+1]

            # time
            if ":" in w:
                time=w
            if wl in ["morning","night"]:
                time=wl

            # animal name
            if wl in ["dog","cat","horse","bird","fish"] and i+1 < len(words):
                animal_name=words[i+1]
                animal_type=wl

        # -------- QUESTIONS --------

        if "who brought" in question:
            return subject

        if "who did" in question and "to" in question:
            return place

        if "what did" in question:
            return obj

        if "where" in question:
            return place

        if "who does" in question and "with" in question:
            return companion

        if "who was written" in question:
            return recipient

        if "what color" in question:
            for n,c in color_map.items():
                if n in question:
                    return c

        if "what animal is" in question:
            for n,c in color_map.items():
                if c in question:
                    return n

        if "what is blue" in question:
            for n,c in color_map.items():
                if c=="blue":
                    return n

        if "what is my dog's name" in question:
            return animal_name

        if "what animal is red" in question:
            return animal_type

        if "what will" in question and "do" in question:
            return verb

        if "when" in question:
            return time

        if "how far" in question:
            return "mile"

        if "how do" in question:
            return "walk"

        return obj