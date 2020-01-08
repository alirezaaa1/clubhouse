from eosclubhouse.libquest import QuestSet, Registry


class ArtPathWay(QuestSet):

    __pathway_order__ = 1
    __pathway_name__ = 'Art'
    __character_id__ = 'estelle'


Registry.register_quest_set(ArtPathWay)
