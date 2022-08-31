import random
import re , math
import numpy as np
from pathlib import Path
from collections import Counter
from BahasBali.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import sent_tokenize
from sklearn.model_selection import KFold
from sklearn.metrics.pairwise import cosine_similarity
from array import *
from flask import Flask, render_template, flash, request
app = Flask(__name__)

@app.route("/index")
def main():
	return render_template('index.html')

@app.route("/testing" , methods=['GET' , 'POST'])
def testing():
    def stoplist():
        stoplist = open('stoplistbali.txt', 'r').readlines()
        lis = []
        for stop in stoplist:
            lis.append(stop.rstrip())
        #print(list)
        return(lis)
    if request.method == 'POST':
        entries = Path('d/COBA_asli')
        #print(entries)
        doctrain = []
        doc = []
        paragraf = []
        for entry in entries.iterdir():
            print(entry)
            doc.append(entry)
            document_text = open(entry, 'r' ,  encoding="utf8")
            text_string = document_text.readlines()
            documents = []
            #replace
            #print(entry)
            for test in text_string:
                sent = test.lower().rstrip()
                sent = re.sub('ã©','e' ,sent)
                sent = re.sub('é' , 'e',sent)
                documents.append(sent)
            #print(documents)
            # create stemmer
            factory = StemmerFactory()
            stemmer = factory.create_stemmer()
            
            kalimat = []
            judul = ''
            iddoc = []
            paragrafs = []
            #pisah judul dan kalimat
            for x,kal in enumerate(documents):
                #print(x,kal)
                if x == 0:
                    judul = documents[x]
                else:
                    test = sent_tokenize(documents[x])
                    for i in test:
                        paragrafs.append(x)
                        kalimat.append(i)
            
            paragraf.append(paragrafs)
            stop = stoplist()
            tmp = ''
            for j in judul.split():
                if(j not in stop):
                    tmp += j + ' '
            judul = tmp
            judul = stemmer.stem(judul)
            for x,i in enumerate(doc):
                dok = x
            iddoc.append(dok)
            #print(iddoc)
            #doctrain.append((iddoc, judul, kalimat))
            #print('KAL',kalimat)
            fix = []
            list = stoplist()
            #print(documents)
            for document in kalimat:
                temp = ""
                for word in document.split():
                    if word not in list:
                        word = stemmer.stem(word)
                        temp += word + ' '
                #print('TEMP',temp)
                fix.append(temp)
            #print('fisss', fix)
            doctrain.append((iddoc, judul, kalimat, fix))

        def keypos_f1(kal,fix):
            # fix = filtering_stemming(kalimat)
            for  doc in doctrain:
                words = re.findall(r'\w+', str(fix))
                keypos = Counter(words).most_common(1)
                fitur1 = []
                # for word in fix:
                #print(keypos[0][0])
                temp = sum(1 for c in kal.split() if c == keypos[0][0])
                f1 = temp/keypos[0][1]
                fitur1.append(f1)
            #print(f1)
            return fitur1 

        def keynef_f2(kal,fix):
            # fix = filtering_stemming(kalimat)
            for  doc in doctrain:
                words = re.findall(r'\w+', str(fix))
                keynef = Counter(words).most_common()[:-2:-1]
                #print(keynef)
                fitur2 = []
                # for word in fix:
                temp = sum(1 for c in kal.split() if c == keynef[0][0])
                f2 = temp/keynef[0][1]
                fitur2.append(f2)
                #print(f2)
            return fitur2
            
        def titlematch_f3(kal,fix):
            for  doc in doctrain:
                fitur3 = []
                # fix = filtering_stemming(kalimat)
                # for k in fix:
                i = 0
                for j in judul.split():
                    if j in kal:
                        i+= 1
                        #print(j)
                #print(i,len(k.split()),len(judul.split()))
                hasil = i/((len(kal.split())+len(judul.split()))-i)
                #print(hasil)
                fitur3.append(hasil)
            return fitur3

        def sentmatch_f4(colkal,fix):
            for  doc in doctrain:
                # fitur4 = []
                # fix = filtering_stemming(kalimat)
                jum = []
                # voc = []
                for k in fix:
                    word = len(k.split())
                    jum.append(word)
                total_words = sum(jum)
                #print(total_words)
                i=0
                uniquewords = []
                for x,kal in enumerate(fix):
                    if(colkal is not x):
                        uniquewords = set(uniquewords).union(set(kal.split()))
                #print(uniquewords)
                
                for w in fix[colkal].split():
                    if w in uniquewords:
                        i+=1
                hasil = i/total_words
                #print(i)
                #print(total_words)
                #print(hasil)
                # fitur4.append(hasil)
            return hasil 
        WORD = re.compile(r'\w+')
        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x]*vec2[x] for x in intersection])
            sum1 = sum([vec1[x]**2 for x in vec1.keys()])
            sum2 = sum([vec2[x]**2 for x in vec2.keys()])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)
            
            if not denominator:
                return 0.0
            else:
                return float(numerator)/denominator
            
        def text_to_vector(text):
            words = WORD.findall(text)
            #print('WORDS = ', words)
            return Counter(words)

        def computeTF(wordDict, bagOfWords):
            tfDict = {}
            #print("TF")
            bagOfWordsCount = len(bagOfWords)
            for word, count in wordDict.items():
                tfDict[word] = count
            #print(tfDict)
            return tfDict

        def computeIDF(documents):
            import math
            N = len(documents)

            idfDict = dict.fromkeys(documents[0].keys(), 0)
            for document in documents:
                for word, val in document.items():
                    if val > 0:
                        idfDict[word] += 1

            for word, val in idfDict.items():
                idfDict[word] = math.log(N / float(val))
            return idfDict

        def computeTFIDF(tfBagOfWords, idfs):
            tfidf = {}
            for word, val in tfBagOfWords.items():
                tfidf[word] = val * idfs[word]
            return tfidf

        def computeall(fix):
            uniqueWords = []
            #fix = filtering_stemming(kalimat)
            # print(fix)
            for x in fix:
                uniqueWords = set(uniqueWords).union(set(x.split()))
            uniqueWords = ' '.join(sorted(uniqueWords))
            uniqueWords = uniqueWords.split()
            # print(uniqueWords)
        # Bonus TF-IDF
            term_frequency = []
            num_for_idf = []
            for x in fix:
                numOfWords = dict.fromkeys(uniqueWords, 0)
                # print(numOfWords)
                for word in x.split():
                    numOfWords[word] += 1
                num_for_idf.append(numOfWords)
                TF = computeTF(numOfWords,x)
                term_frequency.append(TF)
            idfs = computeIDF(num_for_idf)
                
            tf_idf = []
            for tf in term_frequency:
                tf_idf.append(computeTFIDF(tf, idfs))
            #print(tf_idf)
            hasil = []
            for x in tf_idf:
                values = x.values()
                hasil.append([x for x in values])
            #print(hasil)
            return hasil
                   # print(y)

        def get_cosine(vec1,vec2,fix):
            computeall(fix)
            test_a = np.array(vec1)
            test_b = np.array(vec2)
            test_aa = test_a.reshape(1,len(vec1))
            test_bb = test_b.reshape(1,len(vec2))
            coslib = cosine_similarity(test_aa,test_bb)
            return coslib 
            
        def test(fix):
            #fix = filtering_stemming(kalimat)
            total = []
            temp = computeall(fix)
            for i in temp:
                jumlah = []
                for x in temp:
                    vector1 = i
                    vector2 = x
                    hasil = get_cosine(vector1,vector2,fix)
                    #print('vector1:',vector1)
                    #print('vector2:',vector2)
                    #print('Cosine Similiarity :',hasil)
                    jumlah.append(hasil)
                total.append(sum(jumlah))
            #print(total)
            totaa = sum(total)
            score = []
            for tot in total:
                score.append(tot/totaa)
            #print(score)
            return score

        def sortScore(val): 
            return val[2]

        def sortPar(val): 
            return val[1]

        def sortFit(val): 
            return val[2]

        def sortKrom(val): 
            return val[0]

        def sortHas(val): 
            return val[3]


        def openRM():
            manual = Path('d/COBA_manual')
            doc = []
            test2 = []
            for docm in manual.iterdir():
                doc.append(docm)
                document_manual = open(docm, 'r' ,  encoding="utf8")
                textmanual = document_manual.readlines()
                docRM = []
                for test in textmanual:
                    sent = test.lower().rstrip()
                    sent = re.sub('ã©','e' ,sent)
                    sent = re.sub('é' , 'e',sent)
                    docRM.append(sent)
                #print(docRM) 
                kalRM = []
                judul = ''
                
                for x,kal in enumerate(docRM):
                    #print(x,kal)
                    if x == 0:
                        judul = docRM[x]
                    else:
                        kalimatRM = sent_tokenize(docRM[x])
                        test = docRM[x].split()
                        for i in test:
                            kalRM.append(i)
                #print('kRM:', kalRM)
                #print('KalRM : ',kalimatRM)
                test2.append((kalRM,kalimatRM))
                #print('KALIMAT RM \n',kalimatRM)
           # print(test2)
            #print("DIR")
            #print(test)
            #print(kalrm)
                #print('panjang RM : ', len(kalimatRM))     
            return test2
            
        def sumarize():
            kompresi = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 , 0.9, 1]
            testt = []
            test2 = openRM()
            #print(doctrain)
            matrouge = []
            dokumen_no = 0
            w1 = 0.008471
            w2 = 0.373998
            w3 = 0.321812
            w4 = 0.234836
            w5 = 0.060883
            for  z , doc in enumerate(doctrain):
                jmlfix1 = len(test2[z][1])
                for i in kompresi:
                    print(i)
                    jmlfix = len(doc[2]) - (len(doc[2]) * i)
                    #print('jmlkalimat', z , round(jmlfix))
                    cosin = test(doc[3])
                    Rsistem = []
                    fitur = []
                    senscore = []
                    #print(doc[2])
                    for x,kal in enumerate(doc[3]):
                        #print(paragraf[dokumen_no])
                        #print('f1 :')
                        keypos = keypos_f1(kal,doc[3])
                        #print('f2 :')
                        keynef = keynef_f2(kal,doc[3])
                        #print('f3 :')
                        titlematch = titlematch_f3(kal,doc[3])
                        #print('f4 :')
                        sentmatch = sentmatch_f4(x,doc[3])
                        #print('f5 :')
                        fitur.append((paragraf[dokumen_no][x],x,keypos[0],keynef[0],titlematch[0],sentmatch,cosin[x][0][0]))
                        score = keypos[0]*w1 + keynef[0]*w2 + titlematch[0]*w3 + sentmatch*w4 + cosin[x][0][0]*w5
                        #print(x,score)
                        senscore.append((paragraf[dokumen_no][x], x, round(score, 4)))
                        #print(fitur)
                        #print('score kalimat', senscore)
                        senscore.sort(key = sortScore, reverse = True)
                        #print('sort score', senscore)  
                    tempcut = []
                    #print(jmlfix)
                    for x in range(round(jmlfix)):
                        tempcut.append(senscore[x])
                    tempcut.sort(key = sortPar)
                    #print('sort paragraf :',tempcut)
                    sortkal = []
                    #print('\nRINGKASAN')
                    for x in range(round(jmlfix)):
                        ringkas = doc[2][tempcut[x][1]]
                        #print(ringkas)
                        sortkal.append(ringkas)
                    hasil = ' '.join(sortkal)
                    #print(hasil, '\n')
                    kalimatRS = sent_tokenize(hasil)
                    #print('KALRS', kalimatRS)
                    #print('panjang RS', len(kalimatRS))
                    kalRS = (hasil.split())
                    katRS = ' '.join(kalRS)
                    katRSfix = katRS.split()
                    #print(len(kalimatRS))
                    #hitung match
                    match = 0
                    for j in katRSfix:
                        if j in test2[z][0]:
                            match +=1
                            if match > len(test2[z][0]):
                                match = len(test2[z][0])
                    Rouge = round(match/len(test2[z][0]) , 2)
                    matrouge.append(Rouge)
                    print(match)
                    print(len(test2[z][0]))
                    print('Rouge doc:', doc[0], Rouge)
                    Rsistem.append(hasil)   
                testt.append(matrouge)
                dokumen_no += 1
                #print(testt) 
            return matrouge , testt , kompresi
        sumarize , lenr , kompresi = sumarize()
        iddok = []
        judul_txt = []
        for i in doctrain:
            # print(i[0])
            # print(i[1])
            iddok.append(i[0])
            judul_txt.append(i[1])
        for n in sumarize:
            print('N',n)
        return render_template('hasil_testing.html' , doctrain = len(doctrain),  iddok = iddok , judul_txt = judul_txt, rouge = sumarize , lenkom = len(sumarize) , penrouge = len(lenr) , kompresi = kompresi )
    return render_template('testing.html')
    
@app.route("/data_testing")
def data_testing():
    def stoplist():
        stoplist = open('stoplistbali.txt', 'r').readlines()
        lis = []
        for stop in stoplist:
            lis.append(stop.rstrip())
            #print(list)
        return lis
    #print(jml_populasi)
    #print(inputcrossover)
    #print(inputmutasi)
    entries = Path('d/testing')
    #print(entries)
    doctrain = []
    doc = []
    paragraf = []
    for entry in entries.iterdir():
        print(entry)
        doc.append(entry)
        document_text = open(entry, 'r' ,  encoding="utf8")
        text_string = document_text.readlines()
        documents = []
        #replace
        #print(entry)
        for test in text_string:
            sent = test.lower().rstrip()
            sent = re.sub('ã©','e' ,sent)
            sent = re.sub('é' , 'e',sent)
            documents.append(sent)
        #print(documents)
        # create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        
        kalimat = []
        judul = ''
        iddoc = []
        paragrafs = []
        #pisah judul dan kalimat
        for x,kal in enumerate(documents):
            #print(x,kal)
            if x == 0:
                judul = documents[x]
            else:
                test = sent_tokenize(documents[x])
                for i in test:
                    paragrafs.append(x)
                    kalimat.append(i)
        
        paragraf.append(paragrafs)
        stop = stoplist()
        tmp = ''
        for j in judul.split():
            if(j not in stop):
                tmp += j + ' '
        judul = tmp
        judul = stemmer.stem(judul)
        for x,i in enumerate(doc):
            dok = x
        iddoc.append(dok)
        #print(iddoc)
        #doctrain.append((iddoc, judul, kalimat))
        #print('KAL',kalimat)
        fix = []
        list = stoplist()
        #print(documents)
        for document in kalimat:
            temp = ""
            for word in document.split():
                if word not in list:
                    word = stemmer.stem(word)
                    temp += word + ' '
            #print('TEMP',temp)
            fix.append(temp)
        #print('fisss', fix)
        doctrain.append((iddoc, judul, kalimat, fix))
        iddok = []
        judul_txt = []
        for i in doctrain:
            # print(i[0])
            # print(i[1])
            iddok.append(i[0])
            judul_txt.append(i[1])
    return render_template('data_testing.html',doctrain = len(doctrain),  iddok = iddok , judul_txt = judul_txt, path = doc)

@app.route("/data_training")
def data_training():
    def stoplist():
        stoplist = open('stoplistbali.txt', 'r').readlines()
        lis = []
        for stop in stoplist:
            lis.append(stop.rstrip())
            #print(list)
        return lis
    #print(jml_populasi)
    #print(inputcrossover)
    #print(inputmutasi)
    entries = Path('d/training')
    #print(entries)
    doctrain = []
    doc = []
    paragraf = []
    for entry in entries.iterdir():
        print(entry)
        doc.append(entry)
        document_text = open(entry, 'r' ,  encoding="utf8")
        text_string = document_text.readlines()
        documents = []
        #replace
        #print(entry)
        for test in text_string:
            sent = test.lower().rstrip()
            sent = re.sub('ã©','e' ,sent)
            sent = re.sub('é' , 'e',sent)
            documents.append(sent)
        #print(documents)
        # create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        
        kalimat = []
        judul = ''
        iddoc = []
        paragrafs = []
        #pisah judul dan kalimat
        for x,kal in enumerate(documents):
            #print(x,kal)
            if x == 0:
                judul = documents[x]
            else:
                test = sent_tokenize(documents[x])
                for i in test:
                    paragrafs.append(x)
                    kalimat.append(i)
        
        paragraf.append(paragrafs)
        stop = stoplist()
        tmp = ''
        for j in judul.split():
            if(j not in stop):
                tmp += j + ' '
        judul = tmp
        judul = stemmer.stem(judul)
        for x,i in enumerate(doc):
            dok = x
        iddoc.append(dok)
        #print(iddoc)
        #doctrain.append((iddoc, judul, kalimat))
        #print('KAL',kalimat)
        fix = []
        list = stoplist()
        #print(documents)
        for document in kalimat:
            temp = ""
            for word in document.split():
                if word not in list:
                    word = stemmer.stem(word)
                    temp += word + ' '
            #print('TEMP',temp)
            fix.append(temp)
        #print('fisss', fix)
        doctrain.append((iddoc, judul, kalimat, fix))
        iddok = []
        judul_txt = []
        for i in doctrain:
            # print(i[0])
            # print(i[1])
            iddok.append(i[0])
            judul_txt.append(i[1])
    return render_template('data_training.html',doctrain = len(doctrain),  iddok = iddok , judul_txt = judul_txt, path = doc)

@app.route("/algoritma" , methods=['GET' , 'POST'])
def algoritma():
    def stoplist():
        stoplist = open('stoplistbali.txt', 'r').readlines()
        lis = []
        for stop in stoplist:
            lis.append(stop.rstrip())
            #print(list)
        return lis
    if request.method == 'POST':
        jml_populasi=request.form['jumlah_populasi']
        inputcrossover = request.form.getlist('crossover_rate')
        inputmutasi = request.form.getlist('mutation_rate')
        #print(jml_populasi)
        #print(inputcrossover)
        #print(inputmutasi)
        entries = Path('d/COBA_asli')
        #print(entries)
        doctrain = []
        doc = []
        paragraf = []
        for entry in entries.iterdir():
            print(entry)
            doc.append(entry)
            document_text = open(entry, 'r' ,  encoding="utf8")
            text_string = document_text.readlines()
            documents = []
            #replace
            #print(entry)
            for test in text_string:
                sent = test.lower().rstrip()
                sent = re.sub('ã©','e' ,sent)
                sent = re.sub('é' , 'e',sent)
                documents.append(sent)
            #print(documents)
            # create stemmer
            factory = StemmerFactory()
            stemmer = factory.create_stemmer()
            
            kalimat = []
            judul = ''
            iddoc = []
            paragrafs = []
            #pisah judul dan kalimat
            for x,kal in enumerate(documents):
                #print(x,kal)
                if x == 0:
                    judul = documents[x]
                else:
                    test = sent_tokenize(documents[x])
                    for i in test:
                        paragrafs.append(x)
                        kalimat.append(i)
            
            paragraf.append(paragrafs)
            stop = stoplist()
            tmp = ''
            for j in judul.split():
                if(j not in stop):
                    tmp += j + ' '
            judul = tmp
            judul = stemmer.stem(judul)
            for x,i in enumerate(doc):
                dok = x
            iddoc.append(dok)
            #print(iddoc)
            #doctrain.append((iddoc, judul, kalimat))
            #print('KAL',kalimat)
            fix = []
            list = stoplist()
            #print(documents)
            for document in kalimat:
                temp = ""
                for word in document.split():
                    if word not in list:
                        word = stemmer.stem(word)
                        temp += word + ' '
                #print('TEMP',temp)
                fix.append(temp)
            #print('fisss', fix)
            doctrain.append((iddoc, judul, kalimat, fix))
        def keypos_f1(kal,fix):
            # fix = filtering_stemming(kalimat)
            for  doc in train:
                words = re.findall(r'\w+', str(fix))
                keypos = Counter(words).most_common(1)
                fitur1 = []
                # for word in fix:
                #print(keypos[0][0])
                temp = sum(1 for c in kal.split() if c == keypos[0][0])
                f1 = temp/keypos[0][1]
                fitur1.append(f1)
            #print(f1)
            return fitur1

        def keynef_f2(kal,fix):
            # fix = filtering_stemming(kalimat)
            for  doc in train:
                words = re.findall(r'\w+', str(fix))
                keynef = Counter(words).most_common()[:-2:-1]
                #print(keynef)
                fitur2 = []
                # for word in fix:
                temp = sum(1 for c in kal.split() if c == keynef[0][0])
                f2 = temp/keynef[0][1]
                fitur2.append(f2)
                #print(f2)
            return fitur2
        
        def titlematch_f3(kal,fix):
            for  doc in train:
                fitur3 = []
                # fix = filtering_stemming(kalimat)
                # for k in fix:
                i = 0
                for j in judul.split():
                    if j in kal:
                        i+= 1
                        #print(j)
                #print(i,len(k.split()),len(judul.split()))
                hasil = i/((len(kal.split())+len(judul.split()))-i)
                #print(hasil)
                fitur3.append(hasil)
            return fitur3

        def sentmatch_f4(colkal,fix):
            for  doc in train:
                # fitur4 = []
                # fix = filtering_stemming(kalimat)
                jum = []
                # voc = []
                for k in fix:
                    word = len(k.split())
                    jum.append(word)
                total_words = sum(jum)
                #print(total_words)
                i=0
                uniquewords = []
                for x,kal in enumerate(fix):
                    if(colkal is not x):
                        uniquewords = set(uniquewords).union(set(kal.split()))
                #print(uniquewords)
                
                for w in fix[colkal].split():
                    if w in uniquewords:
                        i+=1
                hasil = i/total_words
                #print(i)
                #print(total_words)
                #print(hasil)
                # fitur4.append(hasil)
            return hasil
        WORD = re.compile(r'\w+')
        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x]*vec2[x] for x in intersection])
            sum1 = sum([vec1[x]**2 for x in vec1.keys()])
            sum2 = sum([vec2[x]**2 for x in vec2.keys()])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)
            
            if not denominator:
                return 0.0
            else:
                return float(numerator)/denominator
            
        def text_to_vector(text):
            words = WORD.findall(text)
            #print('WORDS = ', words)
            return Counter(words)

        def computeTF(wordDict, bagOfWords):
            tfDict = {}
            #print("TF")
            bagOfWordsCount = len(bagOfWords)
            for word, count in wordDict.items():
                tfDict[word] = count
            #print(tfDict)
            return tfDict

        def computeIDF(documents):
            import math
            N = len(documents)

            idfDict = dict.fromkeys(documents[0].keys(), 0)
            for document in documents:
                for word, val in document.items():
                    if val > 0:
                        idfDict[word] += 1

            for word, val in idfDict.items():
                idfDict[word] = math.log(N / float(val))
            return idfDict

        def computeTFIDF(tfBagOfWords, idfs):
            tfidf = {}
            for word, val in tfBagOfWords.items():
                tfidf[word] = val * idfs[word]
            return tfidf

        def computeall(fix):
            uniqueWords = []
            #fix = filtering_stemming(kalimat)
            # print(fix)
            for x in fix:
                uniqueWords = set(uniqueWords).union(set(x.split()))
            uniqueWords = ' '.join(sorted(uniqueWords))
            uniqueWords = uniqueWords.split()
            # print(uniqueWords)
        # Bonus TF-IDF
            term_frequency = []
            num_for_idf = []
            for x in fix:
                numOfWords = dict.fromkeys(uniqueWords, 0)
                # print(numOfWords)
                for word in x.split():
                    numOfWords[word] += 1
                num_for_idf.append(numOfWords)
                TF = computeTF(numOfWords,x)
                term_frequency.append(TF)
            idfs = computeIDF(num_for_idf)
            
            tf_idf = []
            for tf in term_frequency:
                tf_idf.append(computeTFIDF(tf, idfs))
            #print(tf_idf)
            hasil = []
            for x in tf_idf:
                values = x.values()
                hasil.append([x for x in values])
            #print(hasil)
            return hasil

        def get_cosine(vec1,vec2,fix):
            computeall(fix)
            test_a = np.array(vec1)
            test_b = np.array(vec2)
            test_aa = test_a.reshape(1,len(vec1))
            test_bb = test_b.reshape(1,len(vec2))
            coslib = cosine_similarity(test_aa,test_bb)
            return coslib 
            
        def test(fix):
            #fix = filtering_stemming(kalimat)
            total = []
            temp = computeall(fix)
            for i in temp:
                jumlah = []
                for x in temp:
                    vector1 = i
                    vector2 = x
                    hasil = get_cosine(vector1,vector2,fix)
                    #print('vector1:',vector1)
                    #print('vector2:',vector2)
                    #print('Cosine Similiarity :',hasil)
                    jumlah.append(hasil)
                total.append(sum(jumlah))
            #print(total)
            totaa = sum(total)
            score = []
            for tot in total:
                score.append(tot/totaa)
            #print(score)
            return score 

        def populasi():
            kromosom = []
            for k in range(int(jml_populasi)):
                temp = []
                for i in range(5):
                    randoms = random.uniform(0, 100)
                    test = round(randoms)
                    #print(test)
                    temp.append(test)
                #print(temp)
                tot = sum(temp)
                #print(tot)
                cek = []
                for i in temp:
                    hasil = i/tot
                    #print(hasil)
                    cek.append(round(hasil, 6))
                kromosom.append(cek)
            #print(kromosom)
            print('KROMOSOM')
            for i in kromosom:
                print(i)
            return kromosom


        def sortScore(val): 
            return val[2]

        def sortPar(val): 
            return val[1]

        def sortFit(val): 
            return val[2]

        def sortKrom(val): 
            return val[0]

        def sortHas(val): 
            return val[3]


        def openRM():
            manual = Path('d/COBA_manual')
            doc = []
            test2 = []
            for docm in manual.iterdir():
                doc.append(docm)
                document_manual = open(docm, 'r' ,  encoding="utf8")
                textmanual = document_manual.readlines()
                docRM = []
                for test in textmanual:
                    sent = test.lower().rstrip()
                    sent = re.sub('ã©','e' ,sent)
                    sent = re.sub('é' , 'e',sent)
                    docRM.append(sent)
                #print(docRM) 
                kalRM = []
                judul = ''
                
                for x,kal in enumerate(docRM):
                    #print(x,kal)
                    if x == 0:
                        judul = docRM[x]
                    else:
                        kalimatRM = sent_tokenize(docRM[x])
                        test = docRM[x].split()
                        for i in test:
                            kalRM.append(i)
                #print('kRM:', kalRM)
                #print('KalRM : ',kalimatRM)
                test2.append((kalRM,kalimatRM))
                #print('KALIMAT RM \n',kalimatRM)
           # print(test2)
            #print("DIR")
            #print(test)
            #print(kalrm)
                #print('panjang RM : ', len(kalimatRM))     
            return test2 
            
        def sumarize(status):
            kromosom = status
            testt = []
            dokumen_no = 0
            for  z,doc in enumerate(train):
                 jmlfix = len(test2[z][1])
                 cosin = test(doc[3])
                 Rsistem = []
                 matrouge = [] 
                 for i in kromosom:
                    w1 = i[0]
                    w2 = i[1]
                    w3 = i[2]
                    w4 = i[3]
                    w5 = i[4]
                    fitur = []
                    senscore = []
                    #perhitungan skor kalimat
                    for x,kal in enumerate(doc[3]):
                        keypos = keypos_f1(kal,doc[3])
                        keynef = keynef_f2(kal,doc[3])
                        titlematch = titlematch_f3(kal,doc[3])
                        sentmatch = sentmatch_f4(x,doc[3])
                        fitur.append((paragraph[dokumen_no][x],x,keypos[0],keynef[0],titlematch[0],sentmatch,cosin[x][0][0]))
                        score = keypos[0]*w1 + keynef[0]*w2 + titlematch[0]*w3 + sentmatch*w4 + cosin[x][0][0]*w5
                        senscore.append((paragraph[dokumen_no][x], x, round(score, 4)))
                    #urut skor kalimat
                    senscore.sort(key = sortScore, reverse = True)
                    tempcut = []
                    #potong jumlah kalimat
                    for x in range(round(jmlfix)):
                        tempcut.append(senscore[x])
                    #urut kalimat berdasarkan indeks paragraf
                    tempcut.sort(key = sortPar)
                    sortkal = []
                    #membuat ringkasan
                    for x in range(round(jmlfix)):
                        ringkas = doc[2][tempcut[x][1]]
                        sortkal.append(ringkas)
                    hasil = ' '.join(sortkal)
                    kalimatRS = sent_tokenize(hasil)
                    kalRS = (hasil.split())
                    katRS = ' '.join(kalRS)
                    katRSfix = katRS.split()
                    match = 0
                    #perhitungan Rouge
                    for j in katRSfix:
                        if j in test2[z][0]:
                            match +=1
                            if match > len(test2[z][0]):
                                match = len(test2[z][0])
                    Rouge = match/len(test2[z][0])
                    matrouge.append(Rouge)
                    Rsistem.append(hasil)
                 dokumen_no += 1    
                 testt.append(matrouge)
            #simpan masing2 rouge kromosom ke dalam matriks
            arr = np.array(testt)
            arr_t = arr.transpose()
            totalrouge = np.sum(arr_t, axis=1)
            fobjektif = []
            #fungsi fitness 
            for x,i in enumerate(totalrouge):
                fobjektif.append((x , round(i/len(train), 8)))
            kromob = []
            totmod = []
            for f in fobjektif:
                totmod.append(f[1])
                kromob.append((f[0], kromosom[f[0]] , f[1]))
            print('\nPOPULASI')
            for i in kromob:
                print(i)
            totalobjektif = sum(totmod)
            #print(totalfitness)
            avgobjektif = totalobjektif / len(kromosom)
            print('Rata2 fitness : ', avgobjektif)
            #print('\nSort Fitness')
            kromob.sort(key = sortFit, reverse = True)
            print('\nKROMOSOM TERBAIK :')
            print(kromob[0])
            return avgobjektif ,kromob[0],kromob 

        def seleksi(generasi):
            kromosom = generasi
            fitness = []
            crom = []
            kromosom.sort(key = sortKrom)
            for i in kromosom:
                fitness.append(i[2])
                crom.append(i[1])
            totalfitness = sum(fitness)
            #Hitung Probabilitas Fitness
            pfitness = []
            for fit in fitness:
                probfit = fit/totalfitness
                pfitness.append(probfit)
            probfit = []
            #ROTWEEL
            #hitung probabilitas komulatif kromosom
            for i in range(len(kromosom)):
                probfit.append(sum(pfitness[0:(i + 1)]))
            randr = []
            #Randomgenerator
            for r in range(len(kromosom)):
                rd = random.uniform(0,1)
                randr.append(rd)
            baru = []
            #KROMOSOM TERPILIH
            for x,ran in enumerate(randr):
                stts = 0
                for i in range(len(kromosom)):
                    if ran < probfit[i] and stts == 0:
                        baru.append(crom[i])
                        stts +=1
            return baru 
            
        def crossover(generasi):
            kromosom = generasi
            #crossover_rate
            pcrossover = float(inputcrossover[0])
            rand = []
            for r in range(len(kromosom)):
                rd = random.uniform(0,0.5)
                rand.append(rd)
            induk = []
            indeks = []
            #INDUK TERPILIH
            for x,ran in enumerate(rand):
                if ran < pcrossover:   
                    induk.append(kromosom[x])
                    indeks.append(x)
            temp = []
            rdom = []
            for i in induk:
                temp.append(i)
            #CUT POINT CROSSOVER
            for r in range(len(induk)):
                rc = random.randint(1,4)
                rdom.append(rc)
            #CROSSOVER
            temp.append(induk[0])
            new = []
            for n,val in enumerate(induk):
                x = []
                temphas = []
                if rdom[n] == 1:
                     x.append(temp[n][0])
                     y = temp[n+1][1:5]
                     #crossover
                     s = x + y
                     tot = sum(s)
                     #kromosom di normalisasi
                     for i in s:
                         hasil = i/tot
                         temphas.append(round(hasil , 6) )
                     new.append( (indeks[n],temphas))
                elif rdom[n] == 2:
                    x = temp[n][0:2]
                    y = temp[n+1][2:5]
                    #crossover
                    s = x + y
                    #kromosom di normalisasi
                    tot = sum(s)
                    for i in s:
                        hasil = i/tot
                        temphas.append(round(hasil , 6) )
                    new.append( (indeks[n],temphas))
                elif rdom[n] == 3:
                    x = temp[n][0:3]
                    y = temp[n+1][3:5]
                    #crossover
                    s = x + y 
                    #kromosom di normalisasi
                    tot = sum(s)
                    for i in s:
                        hasil = i/tot
                        temphas.append(round(hasil , 6) )
                    new.append( (indeks[n],temphas))
                elif rdom[n] == 4:
                    x = temp[n][0:4]
                    y = temp[n+1][4:5]
                    #crossover
                    s = x + y 
                    #kromosom di normalisasi
                    tot = sum(s)
                    for i in s:
                        hasil = i/tot
                        temphas.append(round(hasil , 6) )
                    new.append( (indeks[n],temphas))
            print('Populasi BARU Hasil CrossOver')
            kromosombaru =[]
            for i, k  in enumerate(kromosom):
                for n in new :
                    if i == n[0]:
                        k = n[1]
                print(k)
                kromosombaru.append(k)
            return kromosombaru 

        def randomgen():
            randoms = random.randint(0, 4)
            #print(randoms)
            return randoms
            
        def mutasi(generasi):
            #mutation_rate
            pmutasi = float(inputmutasi[0])
            kromosom = generasi
            pop = []
            for k in kromosom:
                pop.append(k)
            g1 = randomgen()
            g2 = randomgen()
            #RANDOM GEN
            if g1 == g2:
                if g1 == 0:
                    g1 = random.randint(1, 4)
                else: 
                    g2 = random.randrange(0, g1)
            #POPULASI BARU
            popbaru = []
            mut = len(kromosom) * pmutasi
            tempran =[]
            for r in range(int(mut)):
                ran = random.randint(0,9)
                tempran.append(ran)
            for n,x in enumerate(pop):
                if n in tempran:
                    temp = x[g1]
                    x[g1] = x[g2]
                    x[g2] = temp
                popbaru.append(x)
            print('\nPopulasi Hasil Mutasi')
            for p in popbaru:
                print(p)
            #print('\nHitung Ulang Fitness')
            #rata,terbaik,fitbaru = sumarize(popbaru)
            #print(fitbaru)
            return popbaru 

        def algen(pop,iter):
            if (iter < maxgen):
                if(iter == 0):    
                    rata,terbaik,summarize2 = sumarize(pop)
                    print('iterasi awal')
                else:
                    summarize2 = pop
                seleksi2 = seleksi(summarize2)
                #print('TETS')
                #print(summarize2)
                crossover2 = crossover(seleksi2)
                mutasi2 = mutasi(crossover2)
                rata,terbaik,fitbaru = sumarize(mutasi2)
                print('iterasi = ',iter )
                rata_rata.append(rata)
                kromosom_terbaik.append(terbaik)
                iter += 1
                algen(fitbaru,iter)
            else:
                return 0

        global train
        global kromosom_terbaik
        global rata_rata
        global maxgen
        global paragraph
        global test2
        manual = openRM()
        #print(manual) 
        hasilakhir = []
        cv = KFold(n_splits=5, random_state=42, shuffle=False)
        for train_index, test_index in cv.split(doctrain):
            
            print(train_index)
            print(test_index)
            
            train = [doctrain[a] for a in train_index]
            paragraph = [ paragraf[a] for a in train_index]
            test2 = [manual[a] for a in train_index]
            #print(train)
            
            kromosom_terbaik = []
            
            rata_rata = []
            
            maxgen = 5
            pop = populasi()
            iter = 0
            algen2 = algen(pop,iter)
            print('\n')
            #print(kromosom_terbaik)
            hasil = []
            print('HASIL ALGORITMA GENETIKA')
            print('untuk', maxgen ,'generasi', 'dengan jumlah kromosom : ', len(pop), 'kromosom') 
            for i , k  in enumerate(kromosom_terbaik):
                print(i ,rata_rata[i], k[1], k[2])
                hasil.append((i , rata_rata[i] , k[1] , k[2]))
            hasil.sort(key = sortPar, reverse = True)
            #for i in hasil:
                #print(i)
            print('\nFitness terbaik dilihat dari GENERASI TERBAIK')
            print(hasil[0])
            print('KROMOSOM TERPILIH')
            print(hasil[0][2])
            # hasil.sort(key = sortHas, reverse = True)
            # print('\nFitness terbaik hasil iterasi')
            # print(hasil[0])
            rata = 0
            for i in test_index:
                #print(doctrain[i])
                train = [doctrain[i]]
                paragraph = [ paragraf[i]]
                test2 = [manual[i]]
                print([hasil[0][2]])
                #print(train)
                #print(paragraph)
                #print(test2)
                has = sumarize([hasil[0][2]])
                print("Hasil pengujian : ", has[0])
                rata += has[0]
            hasilakhir.append((hasil[0][2],rata/len(test_index)))
        for hasil in hasilakhir:
            print(hasil)
        hasilakhir.sort(key = sortPar, reverse = True)
        print('KROMOSOM TERBAIK')
        print(hasilakhir[0])
        hasilakhir1 = hasilakhir[0]
        for i in hasilakhir1:
            #print(i)
            bobot = hasilakhir1[0]
            fitness = hasilakhir1[1]
        for i in bobot:
            print(i)
        return render_template('hasil_training.html' , hasil = hasilakhir1 , bobot = bobot , fitness = fitness , jumlah_populasi = jml_populasi , crossover_rate = float(inputcrossover[0]) , mutation_rate = float(inputmutasi[0]))
    return render_template('algoritma.html')

@app.route("/ringkas-file")
def ringkasfile():
	return render_template('ringkas.html')

@app.route("/ringkas-manual", methods=['GET' , 'POST'])
def ringkasmanual():
     def stoplist():
        stoplist = open('stoplistbali.txt', 'r').readlines()
        lis = []
        for stop in stoplist:
            lis.append(stop.rstrip())
        #print(lis)
        return lis
     if request.method == 'POST':
        text_string = []
        judul=request.form['judul']
        judul1 = judul
        isi=request.form['isi']
        inputkompresi = request.form.getlist('kompresi')
        documents=[]
        kalimat = []
        paragraf = []
        kalm = []
        print('ISI',isi)
        par = isi.split('\n')
        #print(par)
        for x,p in enumerate(par):
            #print(x, p)
            kalimat1 = sent_tokenize(p)
            print(x, kalimat1)
            kalm.append(kalimat1)
            for kal in kalimat1:
                sent = kal.lower().rstrip()
                sent = re.sub('ã©','e' ,sent)
                sent = re.sub('é' , 'e',sent)
                #print(x,sent)
                kalimat.append(sent)
                paragraf.append(x)
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stop = stoplist()
        tmp = ''
        for j in judul.split():
            if(j not in stop):
                tmp += j + ' '
            judul = tmp
            judul = stemmer.stem(judul)
        def filtering_stemming(kalimat):
            fix = []
            list = stoplist()
            #print(documents)
            for document in kalimat:
                temp = ""
                for word in document.split():
                    if word not in list:
                        word = stemmer.stem(word)
                        temp += word + ' '
                    #print(temp)
                fix.append(temp)
            return fix

        def keypos_f1(kal,fix):
            # fix = filtering_stemming(kalimat)
            words = re.findall(r'\w+', str(fix))
            keypos = Counter(words).most_common(1)
            fitur1 = []
            # for word in fix:
            #print(keypos[0][0])
            temp = sum(1 for c in kal.split() if c == keypos[0][0])
            print('temp1' , temp)
            #print('KALSPLIT',kal.split())
            f1 = temp/keypos[0][1]
            fitur1.append(f1)
            #print('F1',f1)
            return f1 , keypos[0][0]
        def keynef_f2(kal,fix):
            # fix = filtering_stemming(kalimat)
            words = re.findall(r'\w+', str(fix))
            keynef = Counter(words).most_common()[:-2:-1]
            #print(keynef)
            fitur2 = []
            # for word in fix:
            temp = sum(1 for c in kal.split() if c == keynef[0][0])
            f2 = temp/len(kal.split())
            fitur2.append(f2)
            #print(f2)
            return f2 , keynef[0][0]
        def titlematch_f3(kal,fix):
            fitur3 = []
            # fix = filtering_stemming(kalimat)
            # for k in fix:
            i = 0
            for j in judul.split():
                if j in kal:
                    i+= 1
                    #print(j)
            #print(i,len(k.split()),len(judul.split()))
            hasil = i/((len(kal.split())+len(judul.split()))-i)
            #print(hasil)
            fitur3.append(hasil)
            return hasil
        def sentmatch_f4(colkal,fix):
            # fitur4 = []
            # fix = filtering_stemming(kalimat)
            jum = []
            # voc = []
            for k in fix:
                word = len(k.split())
                jum.append(word)
            total_words = sum(jum)
            #print(total_words)
            i=0
            uniquewords = []
            for x,kal in enumerate(fix):
                if(colkal is not x):
                    uniquewords = set(uniquewords).union(set(kal.split()))
            #print(uniquewords)
            
            for w in fix[colkal].split():
                if w in uniquewords:
                    i+=1
            hasil = i/total_words
            #print(i)
            #print(total_words)
            #print(hasil)
            # fitur4.append(hasil)
            return hasil
        WORD = re.compile(r'\w+')
        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x]*vec2[x] for x in intersection])
            sum1 = sum([vec1[x]**2 for x in vec1.keys()])
            sum2 = sum([vec2[x]**2 for x in vec2.keys()])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)
            
            if not denominator:
                return 0.0
            else:
                return float(numerator)/denominator
        
        def text_to_vector(text):
            words = WORD.findall(text)
            #print('WORDS = ', words)
            return Counter(words)

        def computeTF(wordDict, bagOfWords):
            tfDict = {}
            #print("TF")
            bagOfWordsCount = len(bagOfWords)
            for word, count in wordDict.items():
                tfDict[word] = count
            #print(tfDict)
            return tfDict

        def computeIDF(documents):
            import math
            N = len(documents)

            idfDict = dict.fromkeys(documents[0].keys(), 0)
            for document in documents:
                for word, val in document.items():
                    if val > 0:
                        idfDict[word] += 1

            for word, val in idfDict.items():
                idfDict[word] = math.log(N / float(val))
            return idfDict
        def computeTFIDF(tfBagOfWords, idfs):
            tfidf = {}
            for word, val in tfBagOfWords.items():
                tfidf[word] = val * idfs[word]
            return tfidf

        def computeall():
            uniqueWords = []
            fix = filtering_stemming(kalimat)
            # print(fix)
            for x in fix:
                uniqueWords = set(uniqueWords).union(set(x.split()))
            uniqueWords = ' '.join(sorted(uniqueWords))
            uniqueWords = uniqueWords.split()
            # print(uniqueWords)
        # Bonus TF-IDF
            term_frequency = []
            num_for_idf = []
            for x in fix:
                numOfWords = dict.fromkeys(uniqueWords, 0)
                # print(numOfWords)
                for word in x.split():
                    numOfWords[word] += 1
                num_for_idf.append(numOfWords)
                TF = computeTF(numOfWords,x)
                term_frequency.append(TF)
            idfs = computeIDF(num_for_idf)
                
            tf_idf = []
            for tf in term_frequency:
                tf_idf.append(computeTFIDF(tf, idfs))
            #print(tf_idf)
            hasil = []
            for x in tf_idf:
                values = x.values()
                hasil.append([x for x in values])
            #print(hasil)
            return hasil
           # print(y)

        def get_cosine(vec1,vec2):
            computeall()
            test_a = np.array(vec1)
            test_b = np.array(vec2)
            test_aa = test_a.reshape(1,len(vec1))
            test_bb = test_b.reshape(1,len(vec2))
            coslib = cosine_similarity(test_aa,test_bb)
            return coslib
    
        def test():
            #fix = filtering_stemming(kalimat)
            total = []
            temp = computeall()
            for i in temp:
                jumlah = []
                for x in temp:
                    vector1 = i
                    vector2 = x
                    hasil = get_cosine(vector1,vector2)
                    #print('vector1:',vector1)
                    #print('vector2:',vector2)
                    #print('Cosine Similiarity :',hasil)
                    jumlah.append(hasil)
                total.append(sum(jumlah))
            #print(total)
            totaa = sum(total)
            score = []
            for tot in total:
                score.append(tot/totaa)
            #print(score)
            
            return score

        def cosimiliarity_f5(kal):
            #fix = filtering_stemming(kalimat)
            jumlah = []
            total = []
            temp = computeall()
            for x in temp:
                vector1 = temp[kal]
                vector2 = x
                hasil = get_cosine(vector1,vector2)
                #print('vector1:',vector1)
                #print('vector2:',vector2)
                #print('Cosine Similiarity :',hasil)
                jumlah.append(hasil)
                jml = sum(jumlah)
                for i in jml:
                    total.append(i)
            #print(jml)
            #print(total)
            #kata = []
            #for w in fix:
                #kata.append(w)
            #print(kata)
            # vector1 = text_to_vector(fix1)
            # vector2 = text_to_vector(fix1)
            # hasil = get_cosine(vector1,vector2)
            # print(hasil)
            return jml
    
        def sortScore(val): 
            return val[2]

        def sortPar(val): 
            return val[1]

        def sumarize():
            fix = filtering_stemming(kalimat)
            fitur = []
            fit = []
            senscore = []
            cosin = test()
            kompresi = float(inputkompresi[0])
            ringkasfix = []
            kalim = []
            jmlfix = len(kalimat) -(len(kalimat) * kompresi)
            w1 = 0.43010752688172044
            w2 = 0.021505376344086023
            w3 = 0.3655913978494624
            w4 = 0.12903225806451613
            w5 = 0.053763440860215055
            print('FIX',fix)
            #doc = sent_tokenize(fix)
            f1 = []
            f2 = []
            f3 = []
            f4 = []
            f5 = []
            sscore = []
            for x,kal in enumerate(fix):
                print(x,kal)
                keypos , kp = keypos_f1(kal,fix)
                keypos = float(keypos)
                print('f1 :' , keypos)
                f1.append( round(keypos , 6))
                keynef , kn = keynef_f2(kal,fix)
                keynef = float(keynef)
                print('f2 :' , keynef)
                f2.append( round(keynef , 6))
                titlematch = titlematch_f3(kal,fix)
                print('f3 :', titlematch)
                f3.append(round(titlematch , 6))
                sentmatch = sentmatch_f4(x,fix)
                print('f4 :' , sentmatch)
                f4.append( round(sentmatch , 6))
                #print(cosin[x][0][0])
                cosimiliarity = cosimiliarity_f5(x)
                print('f5 :' , cosimiliarity)
                f5.append( round(cosin[x][0][0] , 6))
                # fit.append([keypos,keynef,titlematch])
                fitur.append([paragraf[x],x,keypos,keynef,titlematch,sentmatch,cosin[x][0][0]])
                score = keypos*w1 + keynef*w2 + titlematch*w3 + sentmatch*w4 + cosin[x][0][0]*w5
                print(x,score)
                senscore.append([paragraf[x], x, round(score, 4)])
                sscore.append( round(score , 6))
                kalim.append(kal)

            # print(fitur)
            # print('score kalimat', senscore)
            senscore.sort(key = sortScore, reverse = True)
            print('sort score \n', senscore)
            tempcut = []
            for x in range(round(jmlfix)):
                tempcut.append(senscore[x])
            print(tempcut)
            tempcut.sort(key = sortPar)
            print('sort paragraf :',tempcut)
            sortkal = []
            #print('\nRINGKASAN\n')
            for x in range(round(jmlfix)):
                ringkas = kalimat[tempcut[x][1]]
                #print(ringkas)
                sortkal.append(ringkas)
            hasil = ' '.join(sortkal)
            print(hasil)
            return hasil , fitur , fix , f1 , f2 , f3 , f4 , f5 , sscore , round(w1 , 6) , round(w2 ,6) , round(w3 , 6) , round( w4 ,6), round( w5 , 6) ,  enumerate(senscore) , enumerate(tempcut) , sortkal , kp , kn
        hasil , fitur , fix , f1 , f2 , f3 , f4 ,f5 , sscore , w1 , w2 , w3 , w4 ,  w5 , senscore , tempcut , sortkal , kp , kn = sumarize()
        outkom = float(inputkompresi[0])*100
        kalim = enumerate(kalimat)
        return render_template('hasil.html', judul=judul1 , isi1 = isi , isi = hasil , kompresi = outkom , fitur = fitur , fix = fix , kalim = kalim , f1 = f1 , f2 = f2 , f3 = f3 , f4 = f4 , f5 = f5 , sscore = sscore , w1 =  w1 , w2 = w2 , w3 = w3 , w4 = w4 , w5 = w5 , senscore = senscore ,  tempcut = tempcut , sortkal = sortkal , kp=kp , kn=kn , kalimat = kalimat)
     return render_template('manual.html')

@app.route("/ringkas-babad", methods=['GET' , 'POST'])
def ringkasbabad():
     def stoplist():
        stoplist = open('stoplistbali.txt', 'r').readlines()
        lis = []
        for stop in stoplist:
            lis.append(stop.rstrip())
        #print(lis)
        return lis
     if request.method == 'POST':
        text_string = []
        judul=request.form['judul']
        judul1 = judul
        isi=request.form['isi']
        inputkompresi = request.form.getlist('kompresi')
        documents=[]
        kalimat = []
        paragraf = []
        kalm = []
        print('ISI',isi)
        par = isi.split('\n')
        #print(par)
        for x,p in enumerate(par):
            #print(x, p)
            kalimat1 = sent_tokenize(p)
            print(x, kalimat1)
            kalm.append(kalimat1)
            for kal in kalimat1:
                sent = kal.lower().rstrip()
                sent = re.sub('ã©','e' ,sent)
                sent = re.sub('é' , 'e',sent)
                #print(x,sent)
                kalimat.append(sent)
                paragraf.append(x)
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stop = stoplist()
        tmp = ''
        for j in judul.split():
            if(j not in stop):
                tmp += j + ' '
            judul = tmp
            judul = stemmer.stem(judul)
        def filtering_stemming(kalimat):
            fix = []
            list = stoplist()
            #print(documents)
            for document in kalimat:
                temp = ""
                for word in document.split():
                    if word not in list:
                        word = stemmer.stem(word)
                        temp += word + ' '
                    #print(temp)
                fix.append(temp)
            return fix

        def keypos_f1(kal,fix):
            # fix = filtering_stemming(kalimat)
            words = re.findall(r'\w+', str(fix))
            keypos = Counter(words).most_common(1)
            fitur1 = []
            # for word in fix:
            #print(keypos[0][0])
            temp = sum(1 for c in kal.split() if c == keypos[0][0])
            print('temp1' , temp)
            #print('KALSPLIT',kal.split())
            f1 = temp/keypos[0][1]
            fitur1.append(f1)
            #print('F1',f1)
            return f1 , keypos[0][0]
        def keynef_f2(kal,fix):
            # fix = filtering_stemming(kalimat)
            words = re.findall(r'\w+', str(fix))
            keynef = Counter(words).most_common()[:-2:-1]
            #print(keynef)
            fitur2 = []
            # for word in fix:
            temp = sum(1 for c in kal.split() if c == keynef[0][0])
            f2 = temp/len(kal.split())
            fitur2.append(f2)
            #print(f2)
            return f2 , keynef[0][0]
        def titlematch_f3(kal,fix):
            fitur3 = []
            # fix = filtering_stemming(kalimat)
            # for k in fix:
            i = 0
            for j in judul.split():
                if j in kal:
                    i+= 1
                    #print(j)
            #print(i,len(k.split()),len(judul.split()))
            hasil = i/((len(kal.split())+len(judul.split()))-i)
            #print(hasil)
            fitur3.append(hasil)
            return hasil
        def sentmatch_f4(colkal,fix):
            # fitur4 = []
            # fix = filtering_stemming(kalimat)
            jum = []
            # voc = []
            for k in fix:
                word = len(k.split())
                jum.append(word)
            total_words = sum(jum)
            #print(total_words)
            i=0
            uniquewords = []
            for x,kal in enumerate(fix):
                if(colkal is not x):
                    uniquewords = set(uniquewords).union(set(kal.split()))
            #print(uniquewords)
            
            for w in fix[colkal].split():
                if w in uniquewords:
                    i+=1
            hasil = i/total_words
            #print(i)
            #print(total_words)
            #print(hasil)
            # fitur4.append(hasil)
            return hasil
        WORD = re.compile(r'\w+')
        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x]*vec2[x] for x in intersection])
            sum1 = sum([vec1[x]**2 for x in vec1.keys()])
            sum2 = sum([vec2[x]**2 for x in vec2.keys()])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)
            
            if not denominator:
                return 0.0
            else:
                return float(numerator)/denominator
        
        def text_to_vector(text):
            words = WORD.findall(text)
            #print('WORDS = ', words)
            return Counter(words)

        def computeTF(wordDict, bagOfWords):
            tfDict = {}
            #print("TF")
            bagOfWordsCount = len(bagOfWords)
            for word, count in wordDict.items():
                tfDict[word] = count
            #print(tfDict)
            return tfDict

        def computeIDF(documents):
            import math
            N = len(documents)

            idfDict = dict.fromkeys(documents[0].keys(), 0)
            for document in documents:
                for word, val in document.items():
                    if val > 0:
                        idfDict[word] += 1

            for word, val in idfDict.items():
                idfDict[word] = math.log(N / float(val))
            return idfDict
        def computeTFIDF(tfBagOfWords, idfs):
            tfidf = {}
            for word, val in tfBagOfWords.items():
                tfidf[word] = val * idfs[word]
            return tfidf

        def computeall():
            uniqueWords = []
            fix = filtering_stemming(kalimat)
            # print(fix)
            for x in fix:
                uniqueWords = set(uniqueWords).union(set(x.split()))
            uniqueWords = ' '.join(sorted(uniqueWords))
            uniqueWords = uniqueWords.split()
            # print(uniqueWords)
        # Bonus TF-IDF
            term_frequency = []
            num_for_idf = []
            for x in fix:
                numOfWords = dict.fromkeys(uniqueWords, 0)
                # print(numOfWords)
                for word in x.split():
                    numOfWords[word] += 1
                num_for_idf.append(numOfWords)
                TF = computeTF(numOfWords,x)
                term_frequency.append(TF)
            idfs = computeIDF(num_for_idf)
                
            tf_idf = []
            for tf in term_frequency:
                tf_idf.append(computeTFIDF(tf, idfs))
            #print(tf_idf)
            hasil = []
            for x in tf_idf:
                values = x.values()
                hasil.append([x for x in values])
            #print(hasil)
            return hasil
           # print(y)

        def get_cosine(vec1,vec2):
            computeall()
            test_a = np.array(vec1)
            test_b = np.array(vec2)
            test_aa = test_a.reshape(1,len(vec1))
            test_bb = test_b.reshape(1,len(vec2))
            coslib = cosine_similarity(test_aa,test_bb)
            return coslib
    
        def test():
            #fix = filtering_stemming(kalimat)
            total = []
            temp = computeall()
            for i in temp:
                jumlah = []
                for x in temp:
                    vector1 = i
                    vector2 = x
                    hasil = get_cosine(vector1,vector2)
                    #print('vector1:',vector1)
                    #print('vector2:',vector2)
                    #print('Cosine Similiarity :',hasil)
                    jumlah.append(hasil)
                total.append(sum(jumlah))
            #print(total)
            totaa = sum(total)
            score = []
            for tot in total:
                score.append(tot/totaa)
            #print(score)
            
            return score

        def cosimiliarity_f5(kal):
            #fix = filtering_stemming(kalimat)
            jumlah = []
            total = []
            temp = computeall()
            for x in temp:
                vector1 = temp[kal]
                vector2 = x
                hasil = get_cosine(vector1,vector2)
                #print('vector1:',vector1)
                #print('vector2:',vector2)
                #print('Cosine Similiarity :',hasil)
                jumlah.append(hasil)
                jml = sum(jumlah)
                for i in jml:
                    total.append(i)
            #print(jml)
            #print(total)
            #kata = []
            #for w in fix:
                #kata.append(w)
            #print(kata)
            # vector1 = text_to_vector(fix1)
            # vector2 = text_to_vector(fix1)
            # hasil = get_cosine(vector1,vector2)
            # print(hasil)
            return jml
    
        def sortScore(val): 
            return val[2]

        def sortPar(val): 
            return val[1]

        def sumarize():
            fix = filtering_stemming(kalimat)
            fitur = []
            fit = []
            senscore = []
            cosin = test()
            kompresi = float(inputkompresi[0])
            ringkasfix = []
            kalim = []
            jmlfix = len(kalimat) -(len(kalimat) * kompresi)
            w1 = 0.43010752688172044
            w2 = 0.021505376344086023
            w3 = 0.3655913978494624
            w4 = 0.12903225806451613
            w5 = 0.053763440860215055
            print('FIX',fix)
            #doc = sent_tokenize(fix)
            f1 = []
            f2 = []
            f3 = []
            f4 = []
            f5 = []
            sscore = []
            for x,kal in enumerate(fix):
                print(x,kal)
                keypos , kp = keypos_f1(kal,fix)
                keypos = float(keypos)
                print('f1 :' , keypos)
                f1.append( round(keypos , 6))
                keynef , kn = keynef_f2(kal,fix)
                keynef = float(keynef)
                print('f2 :' , keynef)
                f2.append( round(keynef , 6))
                titlematch = titlematch_f3(kal,fix)
                print('f3 :', titlematch)
                f3.append(round(titlematch , 6))
                sentmatch = sentmatch_f4(x,fix)
                print('f4 :' , sentmatch)
                f4.append( round(sentmatch , 6))
                #print(cosin[x][0][0])
                cosimiliarity = cosimiliarity_f5(x)
                print('f5 :' , cosimiliarity)
                f5.append( round(cosin[x][0][0] , 6))
                # fit.append([keypos,keynef,titlematch])
                fitur.append([paragraf[x],x,keypos,keynef,titlematch,sentmatch,cosin[x][0][0]])
                score = keypos*w1 + keynef*w2 + titlematch*w3 + sentmatch*w4 + cosin[x][0][0]*w5
                print(x,score)
                senscore.append([paragraf[x], x, round(score, 4)])
                sscore.append( round(score , 6))
                kalim.append(kal)

            # print(fitur)
            # print('score kalimat', senscore)
            senscore.sort(key = sortScore, reverse = True)
            print('sort score \n', senscore)
            tempcut = []
            for x in range(round(jmlfix)):
                tempcut.append(senscore[x])
            print(tempcut)
            tempcut.sort(key = sortPar)
            print('sort paragraf :',tempcut)
            sortkal = []
            #print('\nRINGKASAN\n')
            for x in range(round(jmlfix)):
                ringkas = kalimat[tempcut[x][1]]
                #print(ringkas)
                sortkal.append(ringkas)
            hasil = ' '.join(sortkal)
            print(hasil)
            return hasil , fitur , fix , f1 , f2 , f3 , f4 , f5 , sscore , round(w1 , 6) , round(w2 ,6) , round(w3 , 6) , round( w4 ,6), round( w5 , 6) ,  enumerate(senscore) , enumerate(tempcut) , sortkal , kp , kn
        hasil , fitur , fix , f1 , f2 , f3 , f4 ,f5 , sscore , w1 , w2 , w3 , w4 ,  w5 , senscore , tempcut , sortkal , kp , kn = sumarize()
        outkom = float(inputkompresi[0])*100
        kalim = enumerate(kalimat)
        return render_template('hasilbabad.html', judul=judul1 , isi1 = isi , isi = hasil , kompresi = outkom , fitur = fitur , fix = fix , kalim = kalim , f1 = f1 , f2 = f2 , f3 = f3 , f4 = f4 , f5 = f5 , sscore = sscore , w1 =  w1 , w2 = w2 , w3 = w3 , w4 = w4 , w5 = w5 , senscore = senscore ,  tempcut = tempcut , sortkal = sortkal , kp=kp , kn=kn , kalimat = kalimat)
     return render_template('ringkas_babad.html')


if __name__ == "__main__":
    app.run()

