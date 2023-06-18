import os
import MeCab
from pykakasi import kakasi

kakasi = kakasi()
kakasi.setMode("J","H") # Hiragana to ascii, default: no conversio
# kakasi.setMode("K","H") # Hiragana to ascii, default: no conversio
conv = kakasi.getConverter()

tagger = MeCab.Tagger()

def list_files(directory):
    res = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            res.append(os.path.join(root, file))
    return res

def read_ass(filename):
    jps = []
    chs = []
    cur = jps
    with open(filename) as fo:
        for line in fo:
            line = line.strip()
            if '白熊警示广告' in line or '白熊中文OP' in line or '白熊制作成员' in line \
                or '中文ED' in line or '中文OP' in line:
                continue
            if line.startswith('Dialogue'):
                sentence = line.split(',,')[-1]
                if len(sentence) < 1:
                    continue
                if '日文' in line:
                    jps.append(sentence)
                if '中文' in line:
                    chs.append(sentence)
    # for s1, s2 in zip(jps, chs):
    #     print(s1, s2)
    return jps, chs

search_url = "https://www.weblio.jp/content/%s"
search_url2 = "https://dictionary.goo.ne.jp/word/%s"

def format_parse_result(res: str):
    rtn = ""
    lines = res.splitlines()[:-1]
    words = []
    words2 = []
    for line in lines:
        line = line.strip()
        word = line.split()[0]
        if word != '空白':
            words.append(word)
            # rtn += f'{line}  {search_url % word}  {search_url2 % word}\n'
    for i, word in enumerate(words):
        word2 = conv.do(word)
        if word2 == word:
            word2 = '　' * len(word2)
        words2.append(word2)
        if len(word2) > len(word):
            words[i] = word + "　" * (len(word2) - len(word))
    rtn = '　'.join(words2)
    rtn += '\n'
    rtn += '　'.join(words)
    return rtn

def parse_and_format(jps, chs):
    res = ''
    for i, sen in enumerate(jps):
        sen = format_parse_result(tagger.parse(sen))
        # tmp = conv.do(sen)
        # res += f'{tmp}\n'
        if '白熊咖啡厅\\N准备中' == chs:
            continue
        res += f'{sen}'
        if i < len(chs):
            res += f'        [{chs[i]}]\n'
        else:
            res += '\n'
        res += '\n'
    return res

def test():
    print(format_parse_result(tagger.parse('今年もよろしくお願いします')))

if __name__ == '__main__':
    # test()
    # directory_path = "./subs"
    directory_path = './special'
    for fname in list_files(directory_path):
        print(fname)
        jps, chs = read_ass(fname)
        # jps, chs = read_ass('./test.txt')
        res = parse_and_format(jps, chs)
        with open('./simple/' + fname.split('special/')[1] + '.txt', 'w') as fw:
            fw.write(res)