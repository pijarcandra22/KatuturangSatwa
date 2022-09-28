import re
from static.py.library.BahasBali.Stemmer.StemmerFactory import StemmerFactory
from collections import Counter
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from sklearn.model_selection import KFold
from sklearn.metrics.pairwise import cosine_similarity
import math
import numpy as np
import nltk
nltk.download('punkt')

class Sumarize_Bahasa_Bali:
  def __init__(self,judul, isi, inputkompresi = 0.8):
    self.judul         = judul 
    self.judul1        = judul
    self.kalimat       = []
    self.paragraf      = []
    self.kalm          = []
    self.inputkompresi = inputkompresi
    for x,p in enumerate(isi.split('\n')):
      #print(x, p)
      kalimat1 = sent_tokenize(p)
      print(x, kalimat1)
      self.kalm.append(kalimat1)
      for kal in kalimat1:
        sent = kal.lower().rstrip()
        sent = re.sub('ã©','e' ,sent)
        sent = re.sub('é' , 'e',sent)
        #print(x,sent)
        self.kalimat.append(sent)
        self.paragraf.append(x)
    self.factory = StemmerFactory()
    self.stemmer = self.factory.create_stemmer()
    self.stop = self.stoplist()
    tmp = ''
    for j in judul.split():
      if(j not in self.stop):
        tmp += j + ' '
      judul = tmp
      judul = self.stemmer.stem(judul)
    self.WORD = re.compile(r'\w+')

  def stoplist(self):
    stoplist = open('static/py/stoplistbali.txt', 'r').readlines()
    lis = []
    for stop in stoplist:
      lis.append(stop.rstrip())
    return lis
  
  def filtering_stemming(self):
    fix = []
    list = self.stoplist()
    for document in self.kalimat:
      temp = ""
      for word in document.split():
        if word not in list:
          word = self.stemmer.stem(word)
          temp += word + ' '
      fix.append(temp)
    return fix
  
  def computeall(self):
    uniqueWords = []
    fix = self.filtering_stemming()
    for x in fix:
      uniqueWords = set(uniqueWords).union(set(x.split()))
    uniqueWords = ' '.join(sorted(uniqueWords))
    uniqueWords = uniqueWords.split()
    term_frequency = []
    num_for_idf = []
    for x in fix:
      numOfWords = dict.fromkeys(uniqueWords, 0)
      for word in x.split():
        numOfWords[word] += 1
      num_for_idf.append(numOfWords)
      TF = self.computeTF(numOfWords,x)
      term_frequency.append(TF)
    idfs = self.computeIDF(num_for_idf)

    tf_idf = []
    for tf in term_frequency:
      tf_idf.append(self.computeTFIDF(tf, idfs))

    hasil = []
    for x in tf_idf:
      values = x.values()
      hasil.append([x for x in values])
    return hasil
        
  def computeTF(self,wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
      tfDict[word] = count
    return tfDict

  def computeIDF(self,documents):
    N = len(documents)
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
      for word, val in document.items():
        if val > 0:
          idfDict[word] += 1
    for word, val in idfDict.items():
      idfDict[word] = math.log(N / float(val))
    return idfDict

  def computeTFIDF(self,tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
      tfidf[word] = val * idfs[word]
    return tfidf

  def test(self):
    total = []
    temp = self.computeall()
    for i in temp:
      jumlah = []
      for x in temp:
        vector1 = i
        vector2 = x
        hasil = self.get_cosine(vector1,vector2)
        jumlah.append(hasil)
      total.append(sum(jumlah))
    totaa = sum(total)
    score = []
    for tot in total:
      score.append(tot/totaa)
    return score

  def get_cosine(self,vec1,vec2):
    test_a = np.array(vec1)
    test_b = np.array(vec2)
    test_aa = test_a.reshape(1,len(vec1))
    test_bb = test_b.reshape(1,len(vec2))
    coslib = cosine_similarity(test_aa,test_bb)
    return coslib

  def keypos_f1(self,kal,fix):
    words = re.findall(r'\w+', str(fix))
    keypos = Counter(words).most_common(1)
    fitur1 = []
    temp = sum(1 for c in kal.split() if c == keypos[0][0])
    print('temp1' , temp)
    f1 = temp/keypos[0][1]
    fitur1.append(f1)
    return f1 , keypos[0][0]

  def keynef_f2(self,kal,fix):
    words = re.findall(r'\w+', str(fix))
    keynef = Counter(words).most_common()[:-2:-1]
    fitur2 = []
    temp = sum(1 for c in kal.split() if c == keynef[0][0])
    try:
      f2 = temp/len(kal.split())
    except:
      f2 =1
    fitur2.append(f2)
    return f2 , keynef[0][0]

  def titlematch_f3(self,kal,fix):
    fitur3 = []
    i = 0
    for j in self.judul.split():
      if j in kal:
        i+= 1
    hasil = i/((len(kal.split())+len(self.judul.split()))-i)
    fitur3.append(hasil)
    return hasil

  def sentmatch_f4(self,colkal,fix):
    jum = []
    for k in fix:
      word = len(k.split())
      jum.append(word)
    total_words = sum(jum)
    i=0
    uniquewords = []
    for x,kal in enumerate(fix):
      if(colkal is not x):
        uniquewords = set(uniquewords).union(set(kal.split()))
    for w in fix[colkal].split():
      if w in uniquewords:
        i+=1
    hasil = i/total_words
    return hasil

  def cosimiliarity_f5(self,kal):
    jumlah = []
    total = []
    temp = self.computeall()
    for x in temp:
      vector1 = temp[kal]
      vector2 = x
      hasil = self.get_cosine(vector1,vector2)
      jumlah.append(hasil)
      jml = sum(jumlah)
      for i in jml:
        total.append(i)
      return jml

  def sortScore(self,val): 
    return val[2]

  def sortPar(self,val): 
    return val[1]

  def sumarize(self):
    fix = self.filtering_stemming()
    fitur = []
    fit = []
    senscore = []
    cosin = self.test()
    kompresi = float(self.inputkompresi)
    ringkasfix = []
    kalim = []
    jmlfix = len(self.kalimat) -(len(self.kalimat) * kompresi)
    w1 = 0.43010752688172044
    w2 = 0.021505376344086023
    w3 = 0.3655913978494624
    w4 = 0.12903225806451613
    w5 = 0.053763440860215055
    print('FIX',fix)
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    f5 = []
    sscore = []
    for x,kal in enumerate(fix):
      print(x,kal)
      keypos , kp = self.keypos_f1(kal,fix)
      keypos = float(keypos)
      print('f1 :' , keypos)
      f1.append( round(keypos , 6))
      keynef , kn = self.keynef_f2(kal,fix)
      keynef = float(keynef)
      print('f2 :' , keynef)
      f2.append( round(keynef , 6))
      titlematch = self.titlematch_f3(kal,fix)
      print('f3 :', titlematch)
      f3.append(round(titlematch , 6))
      sentmatch = self.sentmatch_f4(x,fix)
      print('f4 :' , sentmatch)
      f4.append( round(sentmatch , 6))
      #print(cosin[x][0][0])
      cosimiliarity = self.cosimiliarity_f5(x)
      print('f5 :' , cosimiliarity)
      f5.append( round(cosin[x][0][0] , 6))
      # fit.append([keypos,keynef,titlematch])
      fitur.append([self.paragraf[x],x,keypos,keynef,titlematch,sentmatch,cosin[x][0][0]])
      score = keypos*w1 + keynef*w2 + titlematch*w3 + sentmatch*w4 + cosin[x][0][0]*w5
      print(x,score)
      senscore.append([self.paragraf[x], x, round(score, 4)])
      sscore.append( round(score , 6))
      kalim.append(kal)

    senscore.sort(key = self.sortScore, reverse = True)
    print('sort score \n', senscore)

    tempcut = []
    for x in range(round(jmlfix)):
      tempcut.append(senscore[x])
    print(tempcut)
    tempcut.sort(key = self.sortPar)
    print('sort paragraf :',tempcut)
            
    sortkal = []
    for x in range(round(jmlfix)):
      ringkas = self.kalimat[tempcut[x][1]]
      sortkal.append(ringkas)
    hasil = ' '.join(sortkal)
    print(hasil)
    return hasil

class CaracterDetection_Bahasa_Bali:
  def __init__(self):  
    self.kalimat = ''
    self.listStop = []
    self.namadepan = []
    self.sanskerta = []
    self.punc = '''!()-[]{};:.'"”\<>/?@#$%^&*_~'''

    self.gender = ['I', 'Ni', 'Bagus', 'Ayu']
    self.urutankelahiran = ['Putu', 'Gede', 'Wayan', 'Luh', 'Made', 'Madé', 'Kadek', 'Nengah', 'Nyoman', 'Komang', 'Ketut']
    self.wangsa = ['Ida', 'Anak', 'Cokorda', 'Tjokorda', 'Gusti', 'Dewa', 'Sang', 'Ngakan', 'Bagus', 'Desak', 'Jero', 'Anake', 'Ratu']
    self.singkatan = ['IB', 'IA', 'Gde', 'Gd', 'Cok', 'AA', 'Gst', 'Dw', 'Ngkn', 'Dsk.', 'W', 'Wy', 'Wyn', 'Pt', 'Ngh', 'Md', 'N', 'Nymn', 'Ny', 'Kt', 'Dayu', 'Pan', 'Men', 'Nang', 'Bapa']
    self.pengenalan = ['madan', 'mawasta', 'mewasta','maparab', 'mapesengan', 'kaparabin']

    self.namadepan.append(self.gender)
    self.namadepan.append(self.urutankelahiran)
    self.namadepan.append(self.wangsa)
    self.namadepan.append(self.singkatan)

    with open('static/py/BaliVocab.txt', 'r') as s_file:
        for line in s_file:
            stripped_line = line.strip('\n')
            self.listStop.append(stripped_line)

    with open('static/py/sansekertavocab.txt', 'r', encoding="utf8") as s_file:
        for line in s_file:
            stripped_line = line.strip('\n')
            self.sanskerta.append(stripped_line)


  def ner_name(self,sentences):
    # global output
    names = []
    output = []
    kalimat = sentences
    kalimat = nltk.tokenize.sent_tokenize(kalimat)

    for sindex, i in enumerate(kalimat):
      for j in i:
        if(j in self.punc):
          kalimat[sindex] = kalimat[sindex].replace(j, "")
      kalimat[sindex] = nltk.tokenize.word_tokenize(i)

    for sindex, a in enumerate(kalimat):
      for gindex, b in enumerate(a):
        kalimat[sindex][gindex] = re.sub('ne$', '', b)
            
    for sindex, sentence in enumerate(kalimat):
      rule = 0
      for gindex, a in enumerate(sentence):
        if(a in(item for sublist in self.namadepan for item in sublist)):
          names.append([a])
          temp = names.index([a])
          for c in range((gindex+1), (len(kalimat[sindex]))):
            try:
              if(kalimat[sindex][c][0].isupper()):
                names[temp].append(kalimat[sindex][c])
              else:
                break
            except:
              continue
          continue
        elif ([b for b in self.listStop if a == b] or [b for b in self.listStop if a.lower() == b] and rule == 0):
          continue
        if (a in self.pengenalan):
          temp = []
          for c in range((gindex+1), (len(kalimat[sindex]))):
            try:
              if(kalimat[sindex][c][0].isupper()):
                temp.append(kalimat[sindex][c])
              else:
                break
            except:
              continue
          names.append(temp)
          continue
        try:
          if(a[0].isupper()):
            if([b for b in self.sanskerta if a == b] or [b for b in self.sanskerta if a.lower() == b]):
              names.append([a])
              temp = names.index([a])
              for c in range((gindex+1), (len(kalimat[sindex]))):
                try:
                  if(kalimat[sindex][c][0].isupper()):
                    names[temp].append(kalimat[sindex][c])
                  else:
                    break
                except:
                  continue
              continue
        except:
          continue
        else:
          continue

    for i in names:
      if(len(i) > 1):
        i = ' '.join(i)
        output.append(i)

    same_name = []
    output = list(dict.fromkeys(output))
    copy = output
    for i in range(0, len(output)):
      for j in range(0, len(output)):
        if((copy[i] in output[j]) and i != j):
          same_name.append(copy[i])

    output = ';'.join(map(str, [e for e in output if e not in same_name]))

    name = ', '.join(map(str, output))
    name = "Nama : " + name
    return output