import numpy as np
import pandas as pd
import datetime
import random
import time

def isNaN(num): return num != num

def trans(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if (not isNaN(data.iloc[i, j])) & (type(data.iloc[i, j]) != str):
                data.iloc[i, j] = str(int(data.iloc[i, j]))
    return data

def pretty(d, indent=1):
    print('{')
    for key, value in d.items():
        print('    ' * indent + "'" + str(key) + "': ", end='')
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print(str(value))
    print('    ' * (indent-1) + '}')

def Data_format_conversion(Inputorder, Processing_Qty, RemainBatch, FinishBatchQty, CURRENTTIME, mac_only_list,
                           InputMachine1, InputMachine1QTY, InputMachine2, InputMachine2QTY, 
                           InputFixture1, MCFixture1, InputFixture2, MCFixture2, InputProcessTime, 
                           InputMachine1_2, InputMachine1QTY_2, InputMachine2_2, InputMachine2QTY_2, 
                           InputFixture1_2, MCFixture1_2, InputProcessTime2, MANPOWER_DAY, MANPOWER_NIGHT, 
                           Machineall, Fixtureall):
    
    def add_item(name, num, MC = {}):
        def check_value(value):
            return (not isNaN(value)) & (value != 0)

        if check_value(name) & check_value(num):
            MC[str(name)] = int(num)
        return MC
    
    def add_dict(name, dt, MC = {}):
        def check_dict(dictionary):
            return (len(dictionary) > 0)

        if check_dict(dt):
            MC[str(name)] = dt
        return MC

    Job_information = {}
    for row in range(Inputorder.shape[0]):
        item = Inputorder['WIP_ENTITY_NAME'].iloc[row]
        job_info = {}
        
        for j in range(Inputorder['Oper_num'].iloc[row]):
            ope = 'O'+str(j+1)

            QTY = [int(Inputorder['BatchSize'].iloc[row])] * int(RemainBatch.loc[item, ope])
            if len(QTY) > 0:
                QTY[-1] = int(Inputorder['BatchSizeLast'].iloc[row]) if int(Inputorder['BatchSizeLast'].iloc[row]) != 0 else QTY[-1]
                QTY[0] = int(Processing_Qty.loc[item, ope]) if int(Processing_Qty.loc[item, ope]) != 0 else QTY[0]
                QTY = [0] * (int(RemainBatch.loc[item].max()) - int(RemainBatch.loc[item, ope])) + QTY

            MAP = {}

            # Pri = 1
            para_num1 = InputMachine1QTY.loc[item, ope]
            WF1 = {}
            if not isNaN(InputMachine1.loc[item, ope]):
                if InputMachine1.loc[item, ope] not in mac_only_list:
                    WF1 = add_item('general', 1)
                else:
                    WF1 = add_item('AutoATE', 0, WF1) # 實際不排

            MC1 = {}
            MC1 = add_item(InputMachine1.loc[item, ope], InputMachine1QTY.loc[item, ope], MC1)
            MC1 = add_item(InputMachine2.loc[item, ope], InputMachine2QTY.loc[item, ope], MC1)

            FT1 = {}
            ft_name = InputFixture1.loc[item, ope]
            if not isNaN(ft_name):
                if Fixtureall['FIX_CAPA_QTY'][ft_name] > 0:
                    FT1 = add_item(ft_name, MCFixture1.loc[item, ope], FT1)
            ft_name = InputFixture2.loc[item, ope]
            if not isNaN(ft_name):
                if Fixtureall['FIX_CAPA_QTY'][ft_name] > 0:
                    FT1 = add_item(ft_name, MCFixture2.loc[item, ope], FT1)

            t1 = InputProcessTime.loc[item, ope]

            RC1 = {}
            RC1 = add_dict('WF', WF1, RC1)
            RC1 = add_dict('MC', MC1, RC1)
            RC1 = add_dict('FT', FT1, RC1)

            if len(RC1) > 0:
                MAP.update({
                    1: {
                        'Resource': RC1, 
                        'Time': t1,
                        'Unit': {
                            'Parallel_num': int(para_num1), 
                            'Max_Parallel_num': 1
                        }
                    }
                })

            # Pri = 2
            para_num2 = InputMachine1QTY_2.loc[item, ope]
            WF2 = {}
            if not isNaN(InputMachine1_2.loc[item, ope]):
                if InputMachine1_2.loc[item, ope] not in mac_only_list:
                    WF2 = add_item('general', 1, WF2)
                else:
                    WF2 = add_item('AutoATE', 0, WF2) # 實際不排

            MC2 = {}
            MC2 = add_item(InputMachine1_2.loc[item, ope], InputMachine1QTY_2.loc[item, ope], MC2)
            MC2 = add_item(InputMachine2_2.loc[item, ope], InputMachine2QTY_2.loc[item, ope], MC2)

            FT2 = {}
            ft_name = InputFixture1_2.loc[item, ope]
            if not isNaN(ft_name):
                if Fixtureall['FIX_CAPA_QTY'][ft_name] > 0:
                    FT2 = add_item(ft_name, MCFixture1_2.loc[item, ope], FT2)

            t2 = InputProcessTime2.loc[item, ope]

            RC2 = {}
            RC2 = add_dict('WF', WF2, RC2)
            RC2 = add_dict('MC', MC2, RC2)
            RC2 = add_dict('FT', FT2, RC2)

            if len(RC2) > 0:
                MAP.update({
                    2: {
                        'Resource': RC2, 
                        'Time': t2,
                        'Unit': {
                            'Parallel_num': int(para_num2), 
                            'Max_Parallel_num': 1
                        }
                    }
                })


            job_info.update({
                ope: {
                    'QTY': QTY,
                    'Map': MAP
                }
            })
    
        Job_information.update({item: job_info})
    
    Job_available_init = {}
    for row in range(Inputorder.shape[0]):
        item = Inputorder['WIP_ENTITY_NAME'].iloc[row]
        
        st = max(CURRENTTIME, Inputorder['OPR_END_DATE'].iloc[row])
        st = (st - CURRENTTIME).total_seconds() / 60
        available = [st] * int(RemainBatch.loc[item].max())
        Job_available_init.update({item: available})
    
    Job_shipment_info = {}
    for row in range(Inputorder.shape[0]):
        item = Inputorder['WIP_ENTITY_NAME'].iloc[row]
        
        shipment_info = {}
        shipment_info['REQUEST_JOB'] = Inputorder['REQUEST_JOB'].iloc[row]
        shipment_info['OPR_END_DATE'] = (Inputorder['OPR_END_DATE'].iloc[row] - CURRENTTIME).total_seconds() / 60
        shipment_info['SHIP_DATE'] = (Inputorder['SHIP_DATE'].iloc[row] - CURRENTTIME).total_seconds() / 60
        shipment_info['MTQ_batch'] = Inputorder['MTQ_batch'].iloc[row]
        ope_last = 'O'+ str(Inputorder['Oper_num'].iloc[row])
        shipment_info['Job_QTY'] = Job_information[item][ope_last]['QTY']
        shipment_info['FinishBatchQty'] = int(FinishBatchQty.loc[item][ope_last])

        Job_shipment_info.update({item: shipment_info})
    
    WF_dict = {'AutoATE': [0], 'general': list(range(1, max(MANPOWER_DAY, MANPOWER_NIGHT)))}
    WF_st = [0] * max(MANPOWER_DAY, MANPOWER_NIGHT)

    MC_dict = [0] + Machineall['WC'].cumsum().to_list()
    MC_dict = {Machineall.index[i]: list(range(MC_dict[i], MC_dict[i+1])) for i in range(Machineall.shape[0])}
    MC_st = [0]*(Machineall['WC'].sum())

    FT_dict = [0] + Fixtureall['FIX_CAPA_QTY'].cumsum().to_list()
    FT_dict = {Fixtureall.index[i]: list(range(FT_dict[i], FT_dict[i+1])) for i in range(Fixtureall.shape[0])}
    FT_st = [0]*(Fixtureall['FIX_CAPA_QTY'].sum())

    Resource = {
        'WF': {
            'index': WF_dict, 
        },
        'MC': {
            'index': MC_dict, 
        },
        'FT': {
            'index': FT_dict, 
        }
    }
    
    Resource_available_init = {
        'WF': WF_st,
        'MC': MC_st,
        'FT': FT_st
    }
    
    return Job_information, Job_available_init, Job_shipment_info, Resource, Resource_available_init

def Reset_available(Job_available_init, Resource_available_init):
    Job_available = {key: Job_available_init[key].copy() for key in Job_available_init}
    Resource_available = {key: Resource_available_init[key].copy() for key in Resource_available_init}
    return Job_available, Resource_available

def Dispatch(item, ope, job_info, Job_available, Resource, Resource_available):
    def rsrc_sel(rsrc, value, num):
        # 選用策略：資源較早釋放者取靠後者，資源較晚釋放者取靠前者
        pos = sorted(range(len(rsrc)), key=rsrc.__getitem__)
        rsrc_sorted = [rsrc[i] for i in pos]
        for i, v in enumerate(rsrc_sorted[num:]):
            if v > value:
                return pos[i:(num+i)]
            if rsrc_sorted[i] == value:
                return pos[i:(num+i)]
        return pos[-num:]

    qty = job_info['QTY']
    job_avl = Job_available[item]
    
    if len(qty) == 0:
        return {'job_avl': {}, 'rsrc_avl': {}, 
                'result': [], 'last_time': 0}
    
    # 對所有的資源優先度進行試派並儲存試派結果
    EachPriority_Result = {}
    for pri, map_info in job_info['Map'].items():
        # 儲存試派結果
        result = []

        # 複製當前時間資訊(避免直接改值)
        job_avl_copy = job_avl.copy()
        rsrc_avl_copy = {key: Resource_available[key].copy() for key in Resource_available}
        
        para_num = map_info['Unit']['Parallel_num']
        max_para_num = map_info['Unit']['Max_Parallel_num']
        
        batch_collect = []
        for q in range(len(qty)):
            # 湊齊滿足平行開啟數量的批次數量
            if (len(batch_collect) < para_num) & (qty[q] > 0):
                batch_collect.append(q)
                
            # 當批次集合符合平行開啟數量或達到最後一個批次 : 開始派工
            if (len(batch_collect) == para_num) or (q == (len(qty)-1)):
                start = max([job_avl_copy[q] for q in batch_collect])
                t = map_info['Time'] * max([qty[q] for q in batch_collect])
                
                if t == 0:
                    batch_collect = []
                    continue
                
                # 搜尋最佳資源組合，直到開始時間不會因資源占用而被向後推遲 (重複至多2次)
                st = start
                while True:
                    selected_list = {RC: [] for RC in map_info['Resource']}
                    for RC, rsrc_request in map_info['Resource'].items(): #(WF, MC, FT)
                        for rsrc_name, rsrc_num in rsrc_request.items():
                            rsrc_idx = Resource[RC]['index'][rsrc_name]
                            rsrc_st = [rsrc_avl_copy[RC][idx] for idx in rsrc_idx]

                            selected = rsrc_sel(rsrc_st, st, rsrc_num)
                            selected_list[RC].extend([rsrc_idx[sel] for sel in selected])
                            st = max(st, max([rsrc_st[sel] for sel in selected]))
                
                    if st > start:
                        start = st
                    else:
                        break

                # 更新執行本批次組合後的工單、資源開始時間
                end = start + t
                for RC, selected in selected_list.items():
                    for sel in selected:
                        rsrc_avl_copy[RC][sel] = end
                for q in batch_collect:
                    job_avl_copy[q] = end

                result.append([item, ope, [(q+1) for q in batch_collect], start, end, selected_list])
                batch_collect = []
                
        EachPriority_Result[pri] = {'job_avl': {item: job_avl_copy}, 'rsrc_avl': rsrc_avl_copy, 
                                    'result': result, 'last_time': max(job_avl_copy)}

    pri = min(EachPriority_Result.keys(), key = lambda x: EachPriority_Result[x]['last_time']) # argsort
    return EachPriority_Result[pri]

def Update_Dispatch_Result(Dispatch_result, Job_available, Resource_available, Schedule):
    Job_available.update(Dispatch_result['job_avl'])
    Resource_available.update(Dispatch_result['rsrc_avl'])
    Schedule.extend(Dispatch_result['result'])
    
    return Job_available, Resource_available, Schedule

def Scheduling(Job_list, chr1, Job_information, Job_available, Resource, Resource_available):
    dispatch_order = dict(zip(chr1, Job_list))
    
    Schedule = []
    for i in range(1, len(Job_list)+1):
        # 依據派工順序進行派工
        item, ope = dispatch_order[i]

        # 派工
        Dispatch_result = Dispatch(item, ope, Job_information[item][ope], Job_available, Resource, Resource_available)

        # 上傳本次派工結果並更新資源狀態
        Job_available, Resource_available, Schedule = Update_Dispatch_Result(Dispatch_result, 
                                                                             Job_available, 
                                                                             Resource_available, 
                                                                             Schedule)
    
    return Schedule, Job_available

def Fitness_calculate(Job_available, Job_shipment_info):
    Makespan = max([max(endtime, default=0) for endtime in Job_available.values()])# - CURRENTTIME (=0)
    SumOVERDUE = 0
    SumOVERDUE_WIP = 0
    DelayLength = 0

    for item, last_ope_endtime in Job_available.items():
        shipment_info = Job_shipment_info[item]

        if shipment_info['REQUEST_JOB'] == 'OSP':
            continue

        if shipment_info['REQUEST_JOB'] == 'WIP':
            last_ope_endtime = [0] * shipment_info['FinishBatchQty'] + last_ope_endtime
            nodelay = sum([(et > 0) & (et <= shipment_info['SHIP_DATE']) for et in last_ope_endtime])
            if nodelay < shipment_info['MTQ_batch']:
                SumOVERDUE_WIP += 1

        if shipment_info['REQUEST_JOB'] not in ['OSP', 'WIP']:
            last_ope_endtime = [0] * shipment_info['FinishBatchQty'] + last_ope_endtime
            nodelay = sum([et <= shipment_info['SHIP_DATE'] for et in last_ope_endtime])
            if nodelay < shipment_info['MTQ_batch']:
                if (shipment_info['SHIP_DATE'] > 0) & (shipment_info['SHIP_DATE'] > shipment_info['OPR_END_DATE']):
                    SumOVERDUE += 1

        order_end_time = max(last_ope_endtime, default=0)
        if order_end_time > shipment_info['SHIP_DATE']:
            DelayLength += (order_end_time - shipment_info['SHIP_DATE'])

    Fitness = Makespan + 10000*SumOVERDUE + 10*DelayLength
    
    return Makespan, Fitness, SumOVERDUE, SumOVERDUE_WIP


# ---------------------------------------------------------------------------------------------------- #
# 讀取資料
fixed_current = '20200902090006'
CURRENTTIME = pd.to_datetime(fixed_current)

vers = 'GA_data'
Inputorder = pd.read_csv(vers + '/Inputorder.csv', index_col=0)
Inputorder['OPR_END_DATE'] = pd.to_datetime(Inputorder['OPR_END_DATE'])
Inputorder['SHIP_DATE'] = pd.to_datetime(Inputorder['SHIP_DATE'])

InputMachine1 = pd.read_csv(vers + '/InputMachine1.csv', index_col=0)
InputMachine1_2 = pd.read_csv(vers + '/InputMachine1_2.csv', index_col=0)
InputMachine2 = pd.read_csv(vers + '/InputMachine2.csv', index_col=0)
InputMachine2_2 = pd.read_csv(vers + '/InputMachine2_2.csv', index_col=0)

InputProcessTime = pd.read_csv(vers + '/InputProcessTime.csv', index_col=0)
InputProcessTime2 = pd.read_csv(vers + '/InputProcessTime2.csv', index_col=0)

InputMachine1QTY = pd.read_csv(vers + '/InputMachine1QTY.csv', index_col=0)
InputMachine1QTY_2 = pd.read_csv(vers + '/InputMachine1QTY_2.csv', index_col=0)
InputMachine2QTY = pd.read_csv(vers + '/InputMachine2QTY.csv', index_col=0)
InputMachine2QTY_2 = pd.read_csv(vers + '/InputMachine2QTY_2.csv', index_col=0)

RemainBatch = pd.read_csv(vers + '/RemainBatch.csv', index_col=0)

Machineall = pd.read_csv(vers + '/Machineall.csv', index_col=0)
L = []
for i in Machineall.columns:
    try:
        L.append(int(i))
    except:
        L.append(i)
Machineall.columns = L
#Machineall.columns = Machineall.columns[0:91].astype(int).to_list() + Machineall.columns[91:].to_list()

Processing_Qty = pd.read_csv(vers + '/Processing_Qty.csv', index_col=0)

FinishBatchQty = pd.read_csv(vers + '/FinishBatchQty.csv', index_col=0)

MANPOWER_DAY = 12
MANPOWER_NIGHT = 12

calendar_rest = pd.read_csv(vers + '/calendar_rest.csv', index_col=0)
calendar_rest['REST_START'] = pd.to_datetime(calendar_rest['REST_START'])
calendar_rest['REST_END'] = pd.to_datetime(calendar_rest['REST_END'])

InputOperation = pd.read_csv(vers + '/InputOperation.csv', index_col=0)
InputOperationSequence = pd.read_csv(vers + '/InputOperationSequence.csv', index_col=0)

productionMapSMD = pd.read_csv(vers + '/productionMapSMD.csv', index_col=0)

PMS = pd.read_csv(vers + '/PMS.csv', index_col=0)
PMS['SERIAL_NO'] = PMS['SERIAL_NO'].astype(str)

FixtureGPN = pd.read_csv(vers + '/FixtureGPN.csv', index_col=0)

InputFixture1 = pd.read_csv(vers + '/InputFixture1.csv', index_col=0)
InputFixture2 = pd.read_csv(vers + '/InputFixture2.csv', index_col=0)
InputFixture1_2 = pd.read_csv(vers + '/InputFixture1_2.csv', index_col=0)
MCFixture1 = pd.read_csv(vers + '/MCFixture1.csv', index_col=0)
MCFixture2 = pd.read_csv(vers + '/MCFixture2.csv', index_col=0)
MCFixture1_2 = pd.read_csv(vers + '/MCFixture1_2.csv', index_col=0)

Fixtureall = pd.read_csv(vers + '/Fixtureall.csv', index_col=0)

InputMachine1 = trans(InputMachine1)
InputMachine2 = trans(InputMachine2)
InputMachine1_2 = trans(InputMachine1_2)
InputMachine2_2 = trans(InputMachine2_2)
Fixtureall.iloc[:,:-1] = trans(Fixtureall.iloc[:,:-1])

# ---------------------------------------------------------------------------------------------------- #
mac_only_list = ['120', '125', '130', '131', '132', '135', '140', '150', '151', '161', '162', '165', 'MAN-CONFORMAL_COATING', 'MAN-PACK', 'MAN-PCB_ROUTING', 'MAN-POST_OPERATION', '1SAAALE', '1SPTOV0', '1SPTATE', '2SPTATE', '3SPTATE']

# 任務列
Job_list = [(Inputorder['WIP_ENTITY_NAME'].iloc[i], 'O'+str(j+1)) for i in range(Inputorder.shape[0]) for j in range(Inputorder['Oper_num'].iloc[i])]

# 資料格式轉換
Job_information, Job_available_init, Job_shipment_info, Resource, Resource_available_init = Data_format_conversion(
    Inputorder, Processing_Qty, RemainBatch, FinishBatchQty, CURRENTTIME, mac_only_list, InputMachine1, InputMachine1QTY, 
    InputMachine2, InputMachine2QTY, InputFixture1, MCFixture1, InputFixture2, MCFixture2, InputProcessTime, 
    InputMachine1_2, InputMachine1QTY_2, InputMachine2_2, InputMachine2QTY_2, InputFixture1_2, MCFixture1_2, 
    InputProcessTime2, MANPOWER_DAY, MANPOWER_NIGHT, Machineall, Fixtureall)

def time_axis_transform(baseline, flag, calendar_rest, tt):
    tt = max(baseline, tt)
    
    rest = pd.Timedelta(0, 'm')
    for f in range(flag+1, len(calendar_rest)):
        if tt > calendar_rest['REST_START'][f]:
            if tt > calendar_rest['REST_END'][f]:
                rest += (calendar_rest['REST_END'][f] - calendar_rest['REST_START'][f])
            else:
                rest += (tt - calendar_rest['REST_START'][f])
        else:
            break
    
    return ((tt - baseline) - rest).total_seconds() / 60

baseline = CURRENTTIME

flag = 0
for f in range(calendar_rest.shape[0]-1):
    if (calendar_rest['REST_START'].iloc[f] <= baseline < calendar_rest['REST_START'].iloc[f+1]):
        flag = f
        break
if baseline < calendar_rest['REST_END'].iloc[flag]:
    baseline = calendar_rest['REST_END'].iloc[flag]
    
for row, item in enumerate(Inputorder['WIP_ENTITY_NAME']):
    tt1 = Inputorder['OPR_END_DATE'].iloc[row]
    r1 = time_axis_transform(baseline, flag, calendar_rest, tt1)
    
    tt2 = Inputorder['SHIP_DATE'].iloc[row]
    r2 = time_axis_transform(baseline, flag, calendar_rest, tt2)
    
    Job_available_init[item] = [r1] * int(RemainBatch.loc[item].max())
    Job_shipment_info[item]['OPR_END_DATE'] = r1
    Job_shipment_info[item]['SHIP_DATE'] = r2
    
##### vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv #####
# 取得染色體
chr1 = list(range(1, len(Job_list)+1))

st = time.time()
# 初始化可開始時間, 開始排程 
Job_available, Resource_available = Reset_available(Job_available_init, Resource_available_init)
Schedule, Job_available = Scheduling(Job_list, chr1, Job_information, Job_available, Resource, Resource_available)

# 計算適合度
min_makespan, min_fitness, delayjobcount, delayjobcount_wip = Fitness_calculate(Job_available, Job_shipment_info)
print(min_makespan, min_fitness, delayjobcount, delayjobcount_wip)
print('Time cost: ', round(time.time()-st, 3), 's')
##### ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #####

# 看排程大表
Schedule = pd.DataFrame(Schedule, columns = ['Job', 'Operation', 'Batch', 'StartTime', 'EndTime', 'Resource'])
print(Schedule)