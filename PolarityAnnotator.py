import string
from TokenHandler import TokenHandler
from KBBIOfflineHandler import KBBIOfflineHandler
from EDBNormiliser import EDBNormaliser

class PolarityAnnotator:
    def __init__(self, comments, kbbi_offline, cpd_pickled, normalised=True):
        self.comments = comments
        self.kms = KBBIOfflineHandler(kbbi_offline)\
            .get_all_datakata()
        self.cpd_pickled = cpd_pickled
        self.normalised = normalised

    def get_annotated_comments(self):
        dct = {}
        for comment_key in self.comments.keys():
            comments_val = self.comments[comment_key]
            tokens_comments = [TokenHandler().word_tokenizer(comment[1]) for comment in comments_val]
            if comment_key not in dct.keys():
                dct[comment_key] = []
            for tokens_comment in tokens_comments:
                result = ''
                ctr_token = 0
                for token in tokens_comment:
                    if token in self.kms.keys():
                        result += "{}/{} ".format(token, self.kms[token])
                    else:
                        if self.normalised:
                            prev_token = tokens_comment[ctr_token-1] if ctr_token > 0 else "<s>"
                            next_token = token
                            normalised_token = EDBNormaliser((prev_token, next_token), self.kms, self.cpd_pickled)\
                                .normalise_token()
                            if normalised_token is None:
                                result += "{}/{} ".format(next_token, 'UNK')
                            else:
                                result += self.get_token_polarity(normalised_token)
                        else:
                            result += "{}/{} ".format(token, 'UNK')
                    ctr_token += 1
                dct[comment_key].append(result)
                print(result)
            # result = [["{}/{}".format(w, (self.kms[w] if w in self.kms.keys() else 'UNK')) for w
            #            in tokens_comment] for tokens_comment in tokens_comments]
        return self.comments, dct

    def get_token_polarity(self, token):
        if token in self.kms.keys():
            return "{}/{} ".format(token, self.kms[token])
        else:
            return "{}/{} ".format(token, 'UNK')