# import spacy
# from spacy.matcher import Matcher

# nlp = spacy.load("en_core_web_sm")
# matcher = Matcher(nlp.vocab)

# # Pattern for detecting "delay" in a risk context (simplified)
# pattern = [
#     {"DEP": "nsubj", "OP": "?"},  # Optional subject
#     {"LEMMA": "delay"},          # The word "delay"
#     {"DEP": {"IN": ["aux", "auxpass", "prep"]}, "OP": "?"}, # Optional auxiliary or preposition
#     {"DEP": {"IN": ["dobj", "pobj", "advmod"]}} # Object, prepositional object, or adverbial modifier
# ]
# matcher.add("DELAY_RISK", [pattern])

# text = "The project has been significantly delayed due to unforeseen circumstances."
# doc = nlp(text)
# matches = matcher(doc)

# for match_id, start, end in matches:
#     string_id = nlp.vocab.strings[match_id]  # Get string representation
#     span = doc[start:end]  # The matched span
#     print(f"Matched: {span.text} (Rule ID: {string_id})")
#     print(f"Root word: {span.root}") # print the root word, e.g. delay

# # Example of dependency parsing
# for token in doc:
#     print(token.text, token.dep_, token.head.text, token.head.pos_,
#           [child for child in token.children])
    



# def add_scope_creep_patterns(matcher):
#     # Basic phrases
#     patterns = [
#         [{"LOWER": "scope"}, {"LOWER": "creep"}],
#         [{"LOWER": "additional"}, {"LOWER": "requirement"}],
#         [{"LOWER": "change"}, {"LOWER": "request"}],
#         [{"LOWER": "new"}, {"LOWER": "feature"}],
#         [{"LOWER": "expanded"}, {"LOWER": "scope"}],
#         [{"LOWER": "out"}, {"LOWER": "of"}, {"LOWER": "scope"}],
#         [{"LOWER": "unplanned"}, {"LOWER": "work"}],
#         [{"LOWER": "feature"}, {"LOWER": "creep"}],
#         [{"LOWER": "requirement"}, {"LOWER": "change"}],
#         [{"LOWER": "added"}, {"LOWER": "feature"}],
#         [{"LOWER": "extra"}, {"LOWER": "work"}],
#         [{"LOWER": "deviation"}, {"LOWER": "from"}, {"LOWER": "plan"}],
#         [{"LOWER": "modified"}, {"LOWER": "requirement"}]
#     ]
#     matcher.add("SCOPE_CREEP_BASIC", patterns)

#     # More contextual patterns (using dependency parsing where helpful)
#     patterns_contextual = [
#         [{"LEMMA": "add"}, {"OP": "a|an|the|ADJ*"}, {"LEMMA": "feature"}], # adding a new feature, adding features
#         [{"LEMMA": "include"}, {"OP": "a|an|the|ADJ*"}, {"LEMMA": "feature"}], # including new features
#         [{"LEMMA": "change"}, {"POS": "ADP"}, {"OP":"DET?"}, {"LEMMA": "requirement"}], # change to requirement
#         [{"LEMMA": "modify"}, {"OP":"DET?"}, {"LEMMA": "requirement"}], # modify requirement
#         [{"LEMMA": "beyond"}, {"LOWER": "the"}, {"LOWER":"original"}, {"LOWER":"scope"}], # beyond the original scope
#         [{"LOWER":"outside"}, {"LOWER":"the"}, {"LOWER":"original"}, {"LOWER":"plan"}] # outside the original plan
#     ]
#     matcher.add("SCOPE_CREEP_CONTEXTUAL", patterns_contextual)
#     return matcher

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)


def add_risk_patterns(matcher):
    # Basic scope creep phrases
    patterns = [
        [{"LOWER": "scope"}, {"LOWER": "creep"}],
        [{"LOWER": "additional"}, {"LOWER": "requirement"}],
        [{"LOWER": "change"}, {"LOWER": "request"}],
        [{"LOWER": "new"}, {"LOWER": "feature"}],
        [{"LOWER": "expanded"}, {"LOWER": "scope"}],
        [{"LOWER": "out"}, {"LOWER": "of"}, {"LOWER": "scope"}],
        [{"LOWER": "unplanned"}, {"LOWER": "work"}],
        [{"LOWER": "feature"}, {"LOWER": "creep"}],
        [{"LOWER": "requirement"}, {"LOWER": "change"}],
        [{"LOWER": "added"}, {"LOWER": "feature"}],
        [{"LOWER": "extra"}, {"LOWER": "work"}],
        [{"LOWER": "deviation"}, {"LOWER": "from"}, {"LOWER": "plan"}],
        [{"LOWER": "modified"}, {"LOWER": "requirement"}]
    ]
    matcher.add("SCOPE_CREEP_BASIC", patterns)

    # More contextual patterns (using dependency parsing where helpful)
    patterns_contextual = [
        # Optionals on individual tokens are fine
        [{"LEMMA": "add"}, {"LOWER": "a", "OP":"?"}, {"LOWER":"new", "OP":"?"}, {"LEMMA": "feature"}],
        [{"LEMMA": "include"}, {"LOWER": "a", "OP":"?"}, {"LOWER":"new", "OP":"?"}, {"LEMMA": "feature"}],

        # Handling "change to/of the requirement" CORRECTLY: Create separate patterns
        [{"LEMMA": "change"}, {"LOWER": "to"}, {"LOWER": "the", "OP":"?"}, {"LEMMA": "requirement"}], # change to (the) requirement
        [{"LEMMA": "change"}, {"LOWER": "of"}, {"LOWER": "the", "OP":"?"}, {"LEMMA": "requirement"}], # change of (the) requirement

        [{"LEMMA": "modify"}, {"LOWER":"the", "OP":"?"}, {"LEMMA": "requirement"}], # modify (the) requirement
        [{"LEMMA": "beyond"}, {"LOWER": "the"}, {"LOWER":"original"}, {"LOWER":"scope"}],
        [{"LOWER":"outside"}, {"LOWER":"the"}, {"LOWER":"original"}, {"LOWER":"plan"}],
        [{"LEMMA":"add"}, {"LOWER":"on"}, {"LOWER":"to"}],
        [{"LOWER":"build"}, {"LOWER":"on"}, {"LOWER":"to"}]
    ]
    matcher.add("SCOPE_CREEP_CONTEXTUAL", patterns_contextual)

    # Schedule Delays
    patterns_schedule = [
        [{"LEMMA": "delay"}],
        [{"LOWER": "behind"}, {"LOWER": "schedule"}],
        [{"LOWER": "missed"}, {"LOWER": "deadline"}],
        [{"LOWER": "postponed"}],
        [{"LOWER": "slippage"}],
        [{"LOWER": "overdue"}],
        [{"LOWER": "time"}, {"LOWER": "overrun"}],
        [{"LOWER": "late"}, {"LOWER": "delivery"}],
        [{"LOWER": "schedule"}, {"LOWER": "variance"}],
        [{"LOWER": "bottleneck"}],
        [{"LOWER": "time"}, {"LOWER": "constraint"}],
        [{"LOWER": "pushed"}, {"LOWER": "back"}],
        [{"LOWER": "put"}, {"LOWER": "off"}],
        [{"LOWER": "rescheduled"}],
        [{"LOWER": "extended"}, {"LOWER": "deadline"}],
        [{"LOWER": "not"}, {"LOWER": "on"}, {"LOWER": "track"}],
        [{"LOWER": "falling"}, {"LOWER": "behind"}]
    ]
    matcher.add("SCHEDULE_DELAY", patterns_schedule)

    # Budget Overruns
    patterns_budget = [
        [{"LOWER": "cost"}, {"LOWER": "increase"}],
        [{"LOWER": "budget"}, {"LOWER": "exceeded"}],
        [{"LOWER": "over"}, {"LOWER": "budget"}],
        [{"LOWER": "cost"}, {"LOWER": "overrun"}],
        [{"LOWER": "funding"}, {"LOWER": "shortfall"}],
        [{"LOWER": "cost"}, {"LOWER": "escalation"}],
        [{"LOWER": "expense"}, {"LOWER": "increase"}],
        [{"LOWER": "unforeseen"}, {"LOWER": "expenses"}],
        [{"LOWER": "higher"}, {"LOWER": "than"}, {"LOWER": "expected"}],
        [{"LOWER": "exceeding"}, {"LOWER": "the"}, {"LOWER": "budget"}],
        [{"LOWER": "budget"}, {"LOWER": "deficit"}],
        [{"LOWER": "financial"}, {"LOWER": "constraints"}]
    ]
    matcher.add("BUDGET_OVERRUN", patterns_budget)

    # Resource Shortages/Constraints
    patterns_resource = [
        [{"LOWER": "lack"}, {"LOWER": "of"}, {"LOWER": "resources"}],
        [{"LOWER": "resource"}, {"LOWER": "constraints"}],
        [{"LOWER": "staff"}, {"LOWER": "shortage"}],
        [{"LOWER": "equipment"}, {"LOWER": "unavailability"}],
        [{"LOWER": "material"}, {"LOWER": "delays"}],
        [{"LOWER": "resource"}, {"LOWER": "allocation"}, {"LOWER": "issues"}],
        [{"LOWER": "limited"}, {"LOWER": "resources"}],
        [{"LOWER": "not"}, {"LOWER": "enough"}, {"LOWER": "manpower"}],
        [{"LOWER": "insufficient"}, {"LOWER": "staff"}],
        [{"LOWER": "lack"}, {"LOWER": "of"}, {"LOWER": "personnel"}],
        [{"LOWER": "equipment"}, {"LOWER": "breakdown"}],
        [{"LOWER": "supply"}, {"LOWER": "chain"}, {"LOWER": "issues"}]
    ]
    matcher.add("RESOURCE_SHORTAGE", patterns_resource)

    # Technical Difficulties/Challenges
    patterns_technical = [
        [{"LOWER": "technical"}, {"LOWER": "difficulties"}],
        [{"LOWER": "integration"}, {"LOWER": "problems"}],
        [{"LOWER": "software"}, {"LOWER": "bugs"}],
        [{"LOWER": "hardware"}, {"LOWER": "failures"}],
        [{"LOWER": "compatibility"}, {"LOWER": "issues"}],
        [{"LOWER": "system"}, {"LOWER": "errors"}],
        [{"LOWER": "technical"}, {"LOWER": "challenges"}],
        [{"LOWER": "implementation"}, {"LOWER": "issues"}],
        [{"LOWER": "debugging"}],
        [{"LOWER": "testing"}, {"LOWER": "issues"}],
        [{"LOWER": "system"}, {"LOWER": "downtime"}],
        [{"LOWER": "performance"}, {"LOWER": "issues"}],
        [{"LOWER": "software"}, {"LOWER": "defects"}],
        [{"LOWER": "hardware"}, {"LOWER": "malfunction"}]
    ]
    matcher.add("TECHNICAL_DIFFICULTY", patterns_technical)
    return matcher