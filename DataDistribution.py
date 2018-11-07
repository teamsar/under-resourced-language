import ast

if __name__ == '__main__':
    fileName = input('File name: ')
    f = open(fileName, 'r')
    data = ast.literal_eval(str(f.read()))

    for comment_key in data.keys():
        ctr_positive, ctr_negative, ctr_netral = 0, 0, 0
        for comment in data[comment_key]:
            tokens = comment.strip().split(' ')
            result = 0
            for token in tokens:
                t = token.split('/')
                if t[0] and len(t) > 1:
                    if 'UNK' not in t[1].strip() and t[1].strip():
                        result += int(t[1].strip())
            if result == 0: ctr_netral += 1
            elif result > 0: ctr_positive += 1
            else: ctr_negative += 1

        g = open('normalised_data_dist.txt', 'a')
        g.write("{}: {},{},{}\n".format(comment_key, ctr_positive, ctr_negative, ctr_netral))
        g.flush()
        g.close()