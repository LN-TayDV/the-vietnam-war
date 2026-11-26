import json

eng_fns = {
    64: 'Neither military, nor economic, nor political considerations were allowed to interfere with the costly and troublesome program of mass exterminations and deportations. If one considers these last',
    69: 'The "Germanic world empire," as Himmler said, or the "Aryan" world empire, as Hitler would have put it, was in any event still centuries off. For the "movement" it was more important to demonstrate',
    72: 'Thus Hitler could afford to use the favorite cliche "decent Jew" once he had begun to exterminate them, namely, in December, 1941, in the Tischgespräche, p. 346.',
    73: 'This leads to the paradox that "the secret society in broad daylight" is never more conspiratory in character and methods than after it has been recognized as a full-fledged member of the committee',
    74: 'This began with an order in July, 1944, by which the SS was elevated to the rank of an independent organization within the NSDAP. and completed by a top secret decree of August 1944, which de',
    76: 'Stalin has carried this art of balance, which demands more skill than the ordinary routine of diplomacy, to the point where a moderation in foreign policy or the political line of the Comintern is',
    77: 'How seriously the Nazis took their conspiratorial fiction, according to which they were the future rulers of the world, came to light in 1940 when, despite necessity, and in the face of all their',
    81: 'In this context also belongs the astonishing rarity of suicides in the camps. Suicide occurred far more often before arrest and deportation than in the camp itself, which is of course partly explained by',
    82: 'This is supported by the fact that the decree to murder all incurably sick was issued on the day the war broke out, but even more so by Hitler\'s statements during the war, quoted by Goebbels (The Goebbels Diaries, ed. Louis P. Lochner, 1948) with the effect that "war has made it possible for us to solve a whole series of problems which could never have been solved in peacetime," and that, no matter how the war ends, "the Jews will certainly be the losers." (p. 314).',
    83: 'Naturally, the Poles themselves soon began to worry about what would happen to them when the Nazis had finished the extermination of the Jews (Nazi Conspiracy, IV, 916). For Hitler\'s plans reg',
    84: 'Whatever connection power had in the minds of Western man with earthly possessions, with wealth, treasures, and riches, has been dissolved into a kind of dematerialized mechanism whose every move g',
    85: 'To a man who believed in organizational omnipotence against all mere material factors, military or economic, and who, moreover, calculated the eventual victory of his enterprise in centuries, defeat',
    86: 'The problem of seizing the state. Hitler frequently commented on the relationship between state and party, and always emphasized that not the state, but the race, or the "united folk community,"',
    92: 'Totalitarianism for facts, its strict adherence to the rules of a fictitious world, becomes steadily more difficult to maintain, yet remains as essential as it was before. Power means a direct co',
    93: 'Many of the errors of the nontotalitarian world in its diplomatic dealings with totalitarian governments (the most conspicuous ones being confidence in the Munich pact with Hitler and the Yalta',
    94: 'Totalitarianism cially the Weimar constitution; they even left the civil services more or less intact-a fact which induced many native and foreign observers to hope for restraint of the party and f',
    96: 'All levels of the administrative machine in the Third Reich were subject to a curious duplication of offices. With a fantastic thoroughness, the Nazis made sure that every function',
    98: 'Totalitarianism in Russia; he introduced the Soviet constitution as the symbol of the existence as well as the powerlessness of the Soviets. (None of its paragraphs ever had the slightest practical',
    99: 'As a matter of fact, duplication of offices, seemingly the result of the party-state problem in all one-party dictatorships, is only the most conspicuous sign of a more complicated phenomenon tha',
    101: 'Typical of the concept of the suspect is the following story related by C. Pobyedonostzev in L\'Autocratie Russe: Mémoires politiques, correspondance officielle et documents divers... 188',
    102: 'Against these "objective," though entirely improbable, possibilities stood only "subjective" factors, such as the trustworthiness of the accused, their fatigue, their inability to understand what',
    103: 'These illegal methods of financing itself, ranging from friendly acceptance of bribes to outright blackmail, were a',
    110: 'The elite formations of the Nazi movement and the "cadres" of the Bolshevik movement serve the goal of total domination rather than the security of the regime in power. Just as the totalitarian',
    115: 'He is never an individual whose dangerous thoughts must be "" Interesting in this respect are the attempts made by Nazi civil servants in Germany to reduce the competence and the personnel of the G',
    116: 'Obviously the limitations of this method are set only by the size of the filing cards, and, theoretically, a gigantic single sheet could show the relations and cross-relationships of the entire',
    117: 'As early as 1941, during a staff meeting in Hitler\'s headquarters, it was proposed to impose upon the Polish population those regulations by which the Jews had been prepared for the extermination',
    118: 'The concept of the "objective opponent," whose identity changes according to the prevailing circumstances-so that, as soon as one category is liquidated, war may be declared on another-corresponds',
    120: 'Of course the population at large and the party members specifically know all the general facts-that concentration camps exist, that people disappear, that innocent persons are arrested; at the same time',
    124: 'The reason why the totalitarian regimes can get so far toward realizing a fictitious, topsy-turvy world is that the outside nontotalitarian world, which always comprises a great part of the population',
    129: 'We attempt to understand elements in present or recollected experience that simply surpass our powers of understanding. We attempt to classify as criminal a thing which, as we all feel, no such',
    131: 'If it is true that the concentration camps are the most consequential institution of totalitarian rule, "dwelling on horrors" would seem to be indispensable for the understanding of totalitarian',
    134: 'David Rousset called his report on the period in a German concentration camp "Les Jours de Notre Mort," and it is indeed as if there were a possibility to give permanence to the process of dying',
    137: 'The films which the Allies circulated in Germany and elsewhere after the war showed clearly that this atmosphere of insanity and unreality is not dispelled by pure reportage. To the unprejudiced observer',
    145: 'To the amalgam of politicals and criminals with which concentration camps in Russia and Germany started out, was added at an early date a third element which was soon to constitute the majority of the camp population',
    146: 'It is this third group of the totally innocent who in every case fare the worst in the camps. Criminals and politicals are assimilated to this category; thus deprived of the protective distinction',
    154: 'Through the creation of conditions under which conscience ceases to be adequate and to do good becomes utterly impossible, the consciously organized complicity of all men in the crimes of totalitarian',
    158: 'The real horror began, however, when the SS took over the administration of the camps. The old spontaneous bestiality gave way to an absolutely cold and systematic destruction of human bodies, calculated with',
}

with open('eng_fns_ch12.json', 'w', encoding='utf-8') as f:
    json.dump(eng_fns, f, ensure_ascii=False, indent=2)

print(f'Saved {len(eng_fns)} English footnotes')