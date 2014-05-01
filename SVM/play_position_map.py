import json

Position_list = ["Power Forward","Shooting Guard","Center","Point Guard","Small Forward"]


def main( ):

    ''' Fetch the original data'''
    SG_list = open('./Player_per/SG.json', "w")
    PF_list  = open('./Player_per/PF.json', "w")
    CT_list  = open('./Player_per/CT.json', "w")
    PG_list  = open('./Player_per/PG.json', "w")
    ST_list  = open('./Player_per/ST.json', "w")

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


    with open('player_raw_json.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    with open('player_raw_json.json') as orginal_player_infor:
        for i in range(position_map_line_number):
            line = orginal_player_infor.readline()
            if len(line) != 0:
                json_line = json.loads(line)
                print json_line['POSITION']
                if (json_line['POSITION'][0] == str('Shooting Guard') ):
                    string = ''.join(map(str,line))
                    print >> SG_list, string
                if (json_line['POSITION'][0] == str('Power Forward') ):
                    string = ''.join(map(str,line))
                    print >> PF_list, string
                if (json_line['POSITION'][0] == str('Center')):
                    string = ''.join(map(str,line))
                    print >> CT_list, string
                if (json_line['POSITION'][0] == str('Point Guard')):
                    string = ''.join(map(str,line))
                    print >> PG_list, string
                if (json_line['POSITION'][0] == str("Small Forward")):
                    string = ''.join(map(str,line))
                    print >> ST_list, string

    '''
    #Calculate the factor for uPer
    with open('player_raw_json.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    lgAST = 0
    lgFG = 0
    lgFT = 0
    lgPTS = 0
    lgFGA = 0
    lgORB = 0
    lgTO = 0
    lgFTA = 0
    lgTRB = 0

    with open('player_raw_json.json') as orginal_player_infor:
        for i in range(position_map_line_number):
            line = orginal_player_infor.readline()
            if len(line) != 0:
                json_line = json.loads(line)
                lgAST = lgAST + int(json_line['AST'][0])
                lgFG = lgFG + int(json_line['FGM'][0])
                lgFT = lgFT + int(json_line['FTM'][0])
                lgPTS = lgPTS + int(json_line['PTS'][0])
                lgFGA = lgFGA + int(json_line['FGA'][0])
                lgORB = lgORB + int(json_line['OREB'][0])
                lgTO = lgTO + int(json_line['TOV'][0])
                lgFTA = lgFTA + int(json_line['FTA'][0])
                lgTRB = lgTRB + int(json_line['REB'][0])

    print lgTRB
    print lgORB
    print (float(lgTRB-lgORB)/lgTRB)
    factor = float(2/3 - ((0.5*lgAST/lgFG)/(2*lgFG/lgFT)))
    VOP = lgPTS/(lgFGA - lgORB +lgTO +0.44*lgFTA)
    DRBP = (lgTRB -lgORB)/lgTRB
    print 'factor value  is'+str(factor)
    print 'VOP value is' +str(VOP)
    print 'DRBP value is ' +str(DRBP)
    '''

    '''Chomp the CT for mini_svm usage'''
    chomp_CT = open('./Player/chomCT.json', "w")

    with open('./Player/CT.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    with open('./Player/CT.json') as OriginCT:
        for i in range(position_map_line_number):
            line = OriginCT.readline().split()
            if len(line) != 0:
                print>> chomp_CT, ' '.join(map(str,line))


    '''Chomp SG'''
    chomp_SG = open('./Player/chomSG.json', "w")

    with open('./Player/SG.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    with open('./Player/SG.json') as OriginSG:
        for i in range(position_map_line_number):
            line = OriginSG.readline().split()
            if len(line) != 0:
                print>> chomp_SG, ''.join(map(str,line))

    '''Chomp PF'''
    chomp_PF = open('./Player/chomPF.json', "w")

    with open('./Player/PF.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    with open('./Player/PF.json') as OriginPF:
        for i in range(position_map_line_number):
            line = OriginPF.readline().split()
            if len(line) != 0:
                print>> chomp_PF, ''.join(map(str,line))

    '''Chomp PG'''
    chomp_PG = open('./Player/chomPG.json', "w")

    with open('./Player/PG.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    with open('./Player/PG.json') as OriginPG:
        for i in range(position_map_line_number):
            line = OriginPG.readline().split()
            if len(line) != 0:
                print>> chomp_PG, ''.join(map(str,line))

    '''Chomp ST'''
    chomp_ST = open('./Player/chomST.json', "w")

    with open('./Player/ST.json') as counte_line_circuit:
        position_map_line_number = sum(1 for line in counte_line_circuit)
        print position_map_line_number

    with open('./Player/ST.json') as OriginST:
        for i in range(position_map_line_number):
            line = OriginST.readline().split()
            if len(line) != 0:
                print>> chomp_ST, ''.join(map(str,line))


    with open('./Player/chomST.json') as testST:
        line = testST.readline()
        line_json = json.loads(line)


if __name__ == '__main__':
    main()

