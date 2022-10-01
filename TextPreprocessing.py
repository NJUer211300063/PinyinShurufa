"""
预处理文本
"""
import re

standard = re.compile(r'[\u4E00-\u9FA5`~!@#$%^&*()_\-+=<>?:"{}|,.;·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘，。、|\n]{1,}')

fr1 = open('corpus/renminribao_corpus.txt', 'r', encoding='utf-8', errors='ignore')
f2 = open('corpus/corpus_processed.txt', 'w', encoding='utf-8')
txt1 = fr1.read()
for w in standard.findall(txt1):
    f2.write(w)

fr1.close()
f2.close()
print("语料库预处理完成！")




