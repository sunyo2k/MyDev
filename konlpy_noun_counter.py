from konlpy.tag import Twitter
twitter = Twitter()
file = open("/sample/data/loadofthering.txt", 'r')
lines = file.readlines()
word_dic = {}
count = 0
for line in lines:
    malist = twitter.pos(line)
    #print(count, malist)
    for taeso, pumsa in malist:
        if pumsa == "Noun":
            if not (taeso in word_dic):
                word_dic[taeso] = 0
            word_dic[taeso] += 1
            
    if count > 1000:
        break
    count += 1
keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
for word, count in keys[:50]:
    print("{0}({1})".format(word, count), end="\n")
print()
