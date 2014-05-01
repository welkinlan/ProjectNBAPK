import json

from  sklearn import svm
import numpy
from  scipy import sparse


Position_list = ["Power Forward","Shooting Guard","Center","Point Guard","Small Forward"]
#selected out the uncorreclected feature. Need to be divided by 'GP'
#Cared_parameter = ['TOV','OREB','DREB','FG3M','FG3A','FTA','FTM','PF','AST','AST_TOV','PTS','STL','BLK','STL_TOV']

#OREB_PCT = OREB/GP
#DREB_PCT = DREB/GP
#AST_PCT = AST/GP
#STL_PCT = STL/GP
#PF_PCT = PF/GP

Cared_feature= ['EFG_PCT','TS_PCT','FT_PCT','FG3_PCT','AST_TOV','STL_TOV','OREB_PCT','DREB_PCT','AST_PCT','STL_PCT','PF_PCT' ]

def construct_X_Y_matrix( original_txt, doc_number,factor,VOP,DRBP, lgFTA,lgPF,lgFT,Cared_feature,per_player_hash):

    X_Matrix = []
    Y_vector = []

    '''original_matrix'''
    #need to figure out the dimision need by the new matrix, 1Score + 1PseduoQID +11features
    original_matrix = sparse.lil_matrix((doc_number, 13))
    counter = 0

    for num_counter in range(doc_number):
        original_line = original_txt.readline()
        if original_line  != '':
            line_json = json.loads(original_line)
            curr_player = line_json['PLAYER_NAME'][0]
            print curr_player
            if(  str(curr_player) in per_player_hash.keys()):
                per_value = per_player_hash[curr_player]
                print curr_player+str(per_value)

            else:
                per_value = 1/float(line_json['MIN'][0])* ( float(line_json['FG3M'][0])+2/3*float(line_json['AST'][0]) \
                +(2-factor*float(line_json['AST'][0])/float(line_json['FGM'][0]))*float(line_json['FGM'][0]) + 0.5*float(line_json['FTM'][0])*(2-1/3*float(line_json['AST'][0])/float(line_json['FGM'][0]) ) \
                -(VOP*DRBP*float(line_json['FGA'][0])-float(line_json['FGM'][0])) -(VOP*0.44*(0.44+(0.56*DRBP))*(float(line_json['FTA'][0])-float(line_json['FTM'][0])) ) +(VOP*(1-DRBP)*(float(line_json['REB'][0]) - float(line_json['OREB'][0])) ) +(VOP*DRBP*float(line_json['OREB'][0])) +(VOP*float(line_json['STL'][0])) +(VOP*DRBP*float(line_json['BLK'][0])) - (float(line_json['PF'][0])*(lgFT/lgPF -0.44*lgFTA/lgPF*VOP)) )
            #print per_value
            original_matrix[num_counter,0] = per_value
            original_matrix[num_counter,1] = 1
            for i  in range(2,13):
                if(Cared_feature[i-2]=='OREB_PCT'):
                    original_matrix[num_counter, i] = float(line_json['OREB'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='DREB_PCT'):
                    original_matrix[num_counter, i] = float(line_json['DREB'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='AST_PCT'):
                    original_matrix[num_counter, i] = float(line_json['AST'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='STL_PCT'):
                    original_matrix[num_counter, i] = float(line_json['STL'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='PF_PCT'):
                    original_matrix[num_counter, i] = float(line_json['PF'][0])/float(line_json['GP'][0])
                else:
                    original_matrix[num_counter, i] = float(line_json[Cared_feature[i-2]][0])
    '''By now I have finished the original_matrix construction, then feed into the previous established steps to get the real X matrix and Y vector'''

    ''' Addressing the original_matrix based on the quary doc'''
    base_addr_list = [0]
    for addr in range(doc_number-1):
        if (original_matrix[addr+1, 1] - original_matrix[addr,1] != 0):
            base_addr_list.append(addr+1)
    #print base_addr_list

    ''' Processing the pairs page by page '''
    for k_0 in range(len(base_addr_list)):
        if k_0 == len(base_addr_list)-1:
            current_base_addr =base_addr_list[k_0]
            next_base_addr = doc_number
        else:
            current_base_addr = base_addr_list[k_0]
            next_base_addr = base_addr_list[k_0+1]

        current_page_volume = (next_base_addr - current_base_addr)

        ''' By now we get all the possible pair_list in the same query page'''
        ''' Store the difference value of each vectors'''

        for k_1 in range(current_page_volume):
            for i_1 in range(current_page_volume):
                if(k_1 - i_1 !=0):

                    ''' Judge by there relevance value'''
                    ''' If the difference of relavance is positive, then vector Y add 1,
                        Matrix add the vector of features difference'''
                    feature_diff_vector = []
                    if(original_matrix[current_base_addr + k_1,0] - original_matrix[current_base_addr+i_1,0] >0):
                        Y_vector.append(1)
                        for q_0 in range(2,13):
                            temp_feature_diff = original_matrix[current_base_addr+k_1,q_0] - original_matrix[current_base_addr+i_1,q_0]
                            feature_diff_vector.append(temp_feature_diff)
                        X_Matrix.append(feature_diff_vector)

                    elif (original_matrix[current_base_addr+k_1,0] - original_matrix[current_base_addr+i_1,0] <0 ):
                        Y_vector.append(-1)
                        for q_0 in range(2,13):
                            temp_feature_diff = original_matrix[current_base_addr+k_1,q_0] - original_matrix[current_base_addr+i_1,q_0]
                            feature_diff_vector.append(temp_feature_diff)
                        X_Matrix.append(feature_diff_vector)

    return X_Matrix , Y_vector





def test_construct_X_Y_matrix( original_txt, doc_number,factor,VOP,DRBP, lgFTA,lgPF,lgFT,Cared_feature):

    X_Matrix = []
    Y_vector = []

    '''original_matrix'''
    #need to figure out the dimision need by the new matrix, 1Score + 1PseduoQID +11features
    original_matrix = sparse.lil_matrix((doc_number, 13))
    counter = 0

    for num_counter in range(doc_number):
        original_line = original_txt.readline()
        if original_line  != '':
            line_json = json.loads(original_line)

            original_matrix[num_counter,0] = (15-num_counter)
            original_matrix[num_counter,1] = 1
            for i  in range(2,13):
                if(Cared_feature[i-2]=='OREB_PCT'):
                    original_matrix[num_counter, i] = float(line_json['OREB'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='DREB_PCT'):
                    original_matrix[num_counter, i] = float(line_json['DREB'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='AST_PCT'):
                    original_matrix[num_counter, i] = float(line_json['AST'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='STL_PCT'):
                    original_matrix[num_counter, i] = float(line_json['STL'][0])/float(line_json['GP'][0])
                elif(Cared_feature[i-2]=='PF_PCT'):
                    original_matrix[num_counter, i] = float(line_json['PF'][0])/float(line_json['GP'][0])
                else:
                    original_matrix[num_counter, i] = float(line_json[Cared_feature[i-2]][0])
    '''By now I have finished the original_matrix construction, then feed into the previous established steps to get the real X matrix and Y vector'''

    ''' Addressing the original_matrix based on the quary doc'''
    base_addr_list = [0]
    for addr in range(doc_number-1):
        if (original_matrix[addr+1, 1] - original_matrix[addr,1] != 0):
            base_addr_list.append(addr+1)
    #print base_addr_list

    ''' Processing the pairs page by page '''
    for k_0 in range(len(base_addr_list)):
        if k_0 == len(base_addr_list)-1:
            current_base_addr =base_addr_list[k_0]
            next_base_addr = doc_number
        else:
            current_base_addr = base_addr_list[k_0]
            next_base_addr = base_addr_list[k_0+1]

        current_page_volume = (next_base_addr - current_base_addr)

        ''' By now we get all the possible pair_list in the same query page'''
        ''' Store the difference value of each vectors'''

        for k_1 in range(current_page_volume):
            for i_1 in range(current_page_volume):
                if(k_1 - i_1 !=0):

                    ''' Judge by there relevance value'''
                    ''' If the difference of relavance is positive, then vector Y add 1,
                        Matrix add the vector of features difference'''
                    feature_diff_vector = []
                    if(original_matrix[current_base_addr + k_1,0] - original_matrix[current_base_addr+i_1,0] >0):
                        Y_vector.append(1)
                        for q_0 in range(2,13):
                            temp_feature_diff = original_matrix[current_base_addr+k_1,q_0] - original_matrix[current_base_addr+i_1,q_0]
                            feature_diff_vector.append(temp_feature_diff)
                        X_Matrix.append(feature_diff_vector)

                    elif (original_matrix[current_base_addr+k_1,0] - original_matrix[current_base_addr+i_1,0] <0 ):
                        Y_vector.append(-1)
                        for q_0 in range(2,13):
                            temp_feature_diff = original_matrix[current_base_addr+k_1,q_0] - original_matrix[current_base_addr+i_1,q_0]
                            feature_diff_vector.append(temp_feature_diff)
                        X_Matrix.append(feature_diff_vector)

    return X_Matrix , Y_vector






def main( ):

    lgAST = 0
    lgFG = 0
    lgFT = 0
    lgPTS = 0
    lgFGA = 0
    lgORB = 0
    lgTO = 0
    lgFTA = 0
    lgTRB = 0
    factor = 0
    VOP = 0
    DRBP = 0
    lgPF = 0


    C_para = float(raw_input( "Please input the C: "))
    print C_para

    with open('player_raw_json.json') as counte_line_json:
        position_map_line_number = sum(1 for line in counte_line_json)
        print position_map_line_number

    with open('player_raw_json.json') as orginal_player_infor:
        for i in range(position_map_line_number):
            line = orginal_player_infor.readline()
            if len(line) != 0:
                json_line = json.loads(line)
                lgAST = lgAST + float(json_line['AST'][0])
                lgFG = lgFG + float(json_line['FGM'][0])
                lgFT = lgFT + float(json_line['FTM'][0])
                lgPTS = lgPTS + float(json_line['PTS'][0])
                lgFGA = lgFGA + float(json_line['FGA'][0])
                lgORB = lgORB + float(json_line['OREB'][0])
                lgTO = lgTO + float(json_line['TOV'][0])
                lgFTA = lgFTA + float(json_line['FTA'][0])
                lgTRB = lgTRB + float(json_line['REB'][0])
                lgPF = lgPF + float(json_line['PF'][0])

        factor = float(2/3 - ((0.5*lgAST/lgFG)/(2*lgFG/lgFT)))
        VOP = float(lgPTS)/float(lgFGA - lgORB +lgTO +0.44*lgFTA)
        DRBP = float(lgTRB -lgORB)/lgTRB


    with open('per.json') as per_stat_counte:
        per_line_number = sum(1 for line in per_stat_counte)
        print per_line_number

    per_player_hash = {}

    with open('per.json') as per_map_construct:
        for i in range(per_line_number):
            line = per_map_construct.readline()
            if len(line) != 0:
                json_line = json.loads(line)
                player_name = json_line['player'][0]
                player_value = float(json_line['per'][0])
                per_player_hash.update({player_name : player_value})
    print len(per_player_hash.keys())


    #filename = './Player/chomCT.json'
    #filename = './Player/chomPF.json'
    filename = './Player/chomPG.json'
    #filename = './Player/chomSG.json'
    #filename = './Player/chomST.json'

    #testfilename = './Player/golden_CT.json'
    #testfilename = './Player/golden_PF.json'
    testfilename = './Player/golden_PG.json'
    #testfilename = './Player/golden_SG.json'
    #testfilename = './Player/golden_SF.json'


    ''' Construct the Matrix and Vector for  each position'''
    with open (filename) as original_txt :
        doc_number = sum(1 for line in original_txt)
    #print doc_number

    with open (filename) as original_doc:
        X_list, Y_vector = construct_X_Y_matrix(original_doc,doc_number,factor,VOP,DRBP, lgFTA,lgPF,lgFT,Cared_feature,per_player_hash)

    X_Matrix = numpy.array(X_list)
    Y_Matrix = numpy.array(Y_vector)
    print '''Sucessfully finished X_list and Y_vector and Now fitting the svc'''

    with open (testfilename) as original_txt :
        doc_number1 = sum(1 for line in original_txt)
    #print doc_number

    with open (testfilename) as original_doc:
        X_list1, Y_vector1 = test_construct_X_Y_matrix(original_doc,doc_number1,factor,VOP,DRBP, lgFTA,lgPF,lgFT,Cared_feature)

    X_Matrix_1 = numpy.array(X_list1)
    Y_Matrix_1 = numpy.array(Y_vector1)
    print '''Sucessfully finished test's X_list and Y_vector and Now fitting the svc'''

    svc = svm.SVC(C=C_para, kernel = 'linear')
    svc.fit(X_Matrix, Y_Matrix)
    print "Model fit sucessfully"
    accurancy = svc.score(X_Matrix_1, Y_Matrix_1)*100
    print "The accuracy is" +str(accurancy)


    feature_dict = {svc.coef_[0][i] :i for i in range(11)}
    ranked_coef = feature_dict.keys()
    ranked_coef.sort( lambda x, y: cmp(abs(x), abs(y)), reverse = True)

    print"-----------------"
    print "Top 10 Features Statistic\n"

    for i in range(11):
        temp= feature_dict[ranked_coef[i]]
        print "Feature"+ str(temp)+"::  " + Cared_feature[temp-1]+" with coefficient" + str(ranked_coef[i])+'\n'

if __name__ == '__main__':
    main()
