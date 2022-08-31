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