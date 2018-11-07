import pickle
from TokenHandler import TokenHandler


class EDBNormaliser:
    def __init__(self, tokens, kms, cpd_pickled):
        self.tokens = tokens
        self.kms = kms
        self.kms_keys_list = list(self.kms.keys())
        self.cpd_pickled = cpd_pickled

    def get_filtered_kata(self, n_prefix=0, n_postfix=0, token=''):
        if n_prefix > 0 and n_postfix > 0:
            filtered_kata = [kata.strip() for kata in self.kms_keys_list if
                             kata.strip()[:n_prefix] == token[:n_prefix] and
                             kata.strip()[-n_postfix:] == token[-n_postfix:]]
            return list(set(filtered_kata))
        elif n_prefix < 1 < n_postfix:
            filtered_kata = [kata.strip() for kata in self.kms_keys_list if
                             kata.strip()[-n_postfix:] == token[-n_postfix:]]
            return list(set(filtered_kata))
        elif n_prefix > 0 and n_postfix < 1:
            filtered_kata = [kata.strip() for kata in self.kms_keys_list if
                             kata.strip()[:n_prefix] == token[:n_prefix]]
            return list(set(filtered_kata))
        else:
            filtered_kata = [kata.strip() for kata in self.kms_keys_list if token in kata.strip()]
            return list(set(filtered_kata))

    def edit_distance(self, s1, s2):
        output = {}
        m = len(s1) + 1
        n = len(s2) + 1

        tbl = {}
        for i in range(m): tbl[i, 0] = i
        for j in range(n): tbl[0, j] = j
        for i in range(1, m):
            for j in range(1, n):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                tbl[i, j] = min(tbl[i, j - 1] + 1, tbl[i - 1, j] + 1, tbl[i - 1, j - 1] + cost)

        output[s2] = tbl[i, j]
        return output

    def normalise_token(self):
        prev_token = self.exaggerated_word_shortening_solver(self.tokens[0])
        next_token = self.exaggerated_word_shortening_solver(self.tokens[1])

        best = {}
        i, j = (0, 0) if len(next_token) < 3 else (1, 1)
        filtered_kata = self.get_filtered_kata(n_prefix=i, n_postfix=j, token=next_token)

        for kata in filtered_kata:
            distance_two_kata = self.edit_distance(next_token, kata)
            best[kata] = distance_two_kata[kata]

        if bool(best):
            best_candidate_tokens = sorted(best.items(), key=lambda kv: kv[1])
            return self.get_most_relevant_token(best_candidate_tokens, prev_token)


    def get_most_relevant_token(self, best_candidate_tokens, prev_token):
        dct = {}
        # cpd = pickle.loads(self.cpd_pickled)
        cpd = self.cpd_pickled
        for candidate in best_candidate_tokens[:10]:
            _prob = cpd[prev_token].prob(candidate[0])
            dct[candidate] = _prob
        sorted_by_prob = sorted(dct.items(), key=lambda kv: kv[1], reverse=True)
        if bool(sorted_by_prob):
            return "{}".format(sorted_by_prob[0][0][0])
            # if sorted_by_prob[0][1] == 0: return None #"{}/{}".format(sorted_by_prob[0][0][0], sorted_by_prob[0][1])
            # else: return "{}".format(sorted_by_prob[0][0][0])

    def exaggerated_word_shortening_solver(self, token):
        ctr = 0
        el_to_chars = list(token)
        prev_ch, word = '',''
        for i in (range(len(el_to_chars))):
            for j in (range(i, len(el_to_chars))):
                if el_to_chars[i] in el_to_chars[j] and el_to_chars[i] not in prev_ch and ctr > 1:
                    word += el_to_chars[i]
                    prev_ch = el_to_chars[i]
                    ctr += 1
                else:
                    break
        word = word if word else token
        return word