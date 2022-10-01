import json
smList = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,z,c,s,r,zh,ch,sh,y,w'.split(',')
ymList = 'a,o,e,i,u,v,ai,ei,ui,ao,ou,iu,ie,ve,ue,er,an,en,in,un,ang,eng,ing,ong,uai,ia,uan,uang,iang,uo,ua,ian, \
                 iao,iong'.split(',')
ztrdList = 'a,o,e,ai,ei,ao,ou,er,an,en,ang,zi,ci,si,zhi,chi,shi,ri,yi,wu,yu,yin,ying,yun,ye,yue,yuan'.split(',')
PinYin = []
for s in smList:
    for y in ymList:
        PinYin.append(s + y)
for z in ztrdList:
    PinYin.append(z)

# 获取语料库中的所有拼音
with open('TrainingData/STATE' + '.json', 'r') as f:
    state = json.load(f)
allpy = state.keys()


def getSplit(str):
    res = str.split(" ")
    for s in res:
        # 如果输入的拼音不合法或者语料库中没有相应的字，则返回空列表
        if (s not in PinYin) or (s not in allpy):
            return []
    return res


if __name__ == '__main__':
    print(getSplit("da xue"))
