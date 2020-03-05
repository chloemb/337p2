def make_all_verbs(steps):
    new_steps = {}
    for large_step, sentence_dict in steps.items():
        for sentence, sentence_things in sentence_dict.items():
            for verb, verb_things in sentence_things.items():
                # print("adding verb key:", verb)
                # print("with related dict:", verb_things)
                # print("new steps for", verb, "currently has", new_steps.get(verb))
                # print("combining into", verb_things)
                # new_steps.setdefault(verb, {}).update(verb_things)
                if new_steps.get(verb):
                    new_steps[verb] = combine_dict(new_steps.get(verb), verb_things)
                else:
                    new_steps[verb] = verb_things
                # print("new steps is now", new_steps.get(verb))
                # new_steps[verb] = verb_things
    return new_steps


def combine_dict(dict1, dict2):
    # print("combining", dict1, dict2)
    new_dict = {}
    for d1key in dict1.keys():
        # if dict2.get(d1key):
            if type(dict1[d1key]) is dict:
                dict1[d1key].update(dict2[d1key])
                new_dict[d1key] = dict1[d1key]
            elif type(dict1[d1key]) is list:
                dict1[d1key].extend(dict2[d1key])
                new_dict[d1key] = dict1[d1key]
            else:
                new_dict[d1key] = [dict1[d1key], dict2[d1key]]
    return new_dict
