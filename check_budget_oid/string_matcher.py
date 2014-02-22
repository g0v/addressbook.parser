import difflib

# 3-party modules
try:
    import uniout
except ImportError, e:
    pass

# match status
MATCH = 'MATCH'
PARTIAL_MATCH = 'PARTIAL'
MISMATCH = 'MISS'


class IMatcher(object):
    def add(self, obj):
        raise NotImplementedError

    def match(self, obj):
        raise NotImplementedError


class ExactMatcher(IMatcher):
    def __init__(self):
        self._match_objs = set()

    def add(self, obj):
        self._match_objs.add(obj)

    def match(self, obj):
        if obj in self._match_objs:
            return {'match_status': MATCH}
        else:
            return {'match_status': MISMATCH}


class PartialMatcher(IMatcher):
    def __init__(self):
        self._match_objs = set()

    def add(self, obj):
        self._match_objs.add(obj)

    def match(self, obj):
        if obj in self._match_objs:
            # exact match
            return {'match_status': MATCH}

        # check partial match
        matcher = difflib.SequenceMatcher()
        matcher.set_seq1(obj)

        candidates = {}
        for o in self._match_objs:
            # use "offset" to control : MORE words (0) prior to LESS words (-1)
            if obj in o:
                offset = 0
            elif o in obj:
                offset = -1
            else:
                continue
            matcher.set_seq2(o)
            candidates[o] = offset + matcher.ratio()

        if candidates:
            return {
                'match_status': PARTIAL_MATCH,
                'match_candidates': candidates,
            }
        else:
            return {'match_status': MISMATCH}
