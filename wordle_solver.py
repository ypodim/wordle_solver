import tornado
import tornado.ioloop
import tornado.web
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, w):
        self.w = w
    def get(self):
        self.render("index.html")
    def post(self):

        for k,v in self.request.arguments.items():
            val = v[0].decode("utf-8")
            if k == "blacklist":
                w.blacklist = val
            if k in ["w1","w2","w3","w4","w5","b1","b2","b3","b4","b5"]:
                pos = int(k[1])-1
                if k[0] == "w":
                    w.position_whitelist[pos] = val
                if k[0] == "b":
                    w.position_blacklist[pos] = val

        result = w.evaluate()
        self.write("%s" % result)

    def test(self):
        words = w.evaluate()
        self.write("%s %s" % (len(words), ",".join(words)))

class Wordle(object):
    def __init__(self):
        self.words = []
        self.blacklist = ""
        self.position_whitelist = ["","","","",""]
        self.position_blacklist = ["","","","",""]
        with open("%s/all5" % __location__) as f:
            whitelist = ""
            for line in f.readlines():
                word = line[:5].lower()
                self.words.append(word)
        self.load_frequencies()

    def load_frequencies(self):
        self.freq = {}
        with open("%s/unigram_freq.csv" % __location__) as f:
            for line in f.readlines():
                word, f = line.strip().split(',')
                if len(word) == 5:
                    self.freq[word] = int(f)

    def evaluate(self):
        result = []
        for word in self.words:
            prune = False

            whitelist = "".join(self.position_blacklist)
            whitelist += "".join(self.position_whitelist)

            for c in self.blacklist:
                if c in word:
                    prune = True
                    # print("skipping %s because it should not contain %s" % (word, c))
                    break

            for c in whitelist:
                if c not in word:
                    # print("skipping %s because it does not contain %s" % (word, c))
                    prune = True

            for i, c in enumerate(word):
                if len(self.position_whitelist[i]) and c not in self.position_whitelist[i]:
                    # print("skipping %s because it should have letter %s in position %d" % (word, c, i))
                    prune = True
                if c in self.position_blacklist[i]:
                    # print("skipping %s because it should have NOT letter %s in position %d" % (word, c, i))
                    prune = True

            if word not in self.freq:
                prune = True

            if not prune:
                result.append(word)

        temp = sorted(map(lambda x: [x, self.freq[x]], result), key=lambda x: x[1], reverse=True)
        
        return temp


if __name__ == "__main__":
    w = Wordle()
    settings = {
        "template_path": "",
        "static_path": "",
    }
    app = tornado.web.Application([
        (r"/wordle_solver", MainHandler, dict(w=w)),
    ], **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


