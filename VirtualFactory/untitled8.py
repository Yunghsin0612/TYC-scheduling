# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:04:24 2021

@author: DALab
"""

    def gen_product_data(self):
        self.pc_list = gen_pc_list(10, (3,5), (0,2), (0,2))
        self.pd_list = gen_pd_list(10, (3,6))
        self.pd_pc_map = gen_pd_pc_map(self.pd_list, self.pc_list, 4)
        
    def gen_order_data(self):
        row_list = []
        #隨機開始與結束時間
        start = datetime.datetime.strptime('2008/1/1 1:30 PM', '%Y/%m/%d %I:%M %p')
        end = datetime.datetime.strptime('2008/2/1 1:30 PM', '%Y/%m/%d %I:%M %p')
        for i in range(self.len):
            date = random_date(start,end)
            pd_cat = ra.randint(1,5)
            dict1 = {'data_fetch_time': date,
                     'data_create_time': date,
                     'order_id':'wo_'+"%03d" % i,
                     'pd_id':'pd_'+"%03d" % pd_cat,
                     'qty':ra.randint(2,15)*10,
                     'route_id':'route_'+"%03d" % pd_cat,
                     'ES': date+datetime.timedelta(hours=3),
                     'DD': date+datetime.timedelta(days=3)
                    }
            row_list.append(dict1)
        self.data = pd.DataFrame(row_list)
        self.data.to_excel(self.path+'/fake_order_data.xlsx', sheet_name='order', index=False)  
        return list(set(self.data['route_id'].tolist()))

    def gen_rs_table(self, process_count, mc_count, ft_count):
        pc_list = self.pc_list
        row_list= []
        for i in range(pc_list):
            mc_id = ra.randint(1, mc_count)
            dict1 = {'rs_id':'pc_'+"%03d" % i, 
                      'Mc_id':ra.randint(2, 3),
                      'Nft':ra.randint(2, 3),
                      }
            row_list.append(dict1)
        self.data = pd.DataFrame(pc_list)
        self.data.to_excel(self.path+'/fake_process_data.xlsx', sheet_name='order', index=False)  
        
        # return mc_list, ft_list
    
 
    def gen_ft_table(self, fixture_number):
        row_list = []
        for i in range(len(self.op_id_list)):
            dict1 = {'op_id':'op'+"%03d" % i}
            dict1 = {'ft_id':'ft'+"%03d" % i}
            dict1['usage_min'] = ra.choices(ra.choices(range(1,6), weights=(60, 10, 10, 10, 10), k=5))[0]
            dict1['qty'] = dict1['usage_min']*ra.randint(1, 3)
            dict1['usage_max'] = dict1['usage_min']+ra.randint(2, 4)
            row_list.append(dict1)
        df = pd.DataFrame(row_list)
        df.to_excel(self.path+'/fake_fixture_table.xlsx', sheet_name='order', index=False)
        
    def gen_route_table(self, route_id_list):
        row_list = []
        max_op = 6
        #亂數產生route的總站數
        route_op_number = {}
        for route_id in route_id_list:
            route_op_number[route_id] = ra.randint(3, max_op)
        #亂數產生製程對應的機台數
        def gen_op_mc_number():
            op_mc_number = {}
            rnd_sum = 0
            for i in range(max_op):
                total_machine = ra.randint(3, 5)
                op_id = 'op_'+"%01d" % i+"0"
                op_mc_number[op_id] = total_machine
            return op_mc_number
        
        def gen_op_mc_map(op_mc_number):
            op_mc_map = {}
            mc_idx_start = 0
            for i in range(max_op):
                op_id = 'op_'+"%01d" % i+"0"
                op_mc_map[op_id] = ['P%d' % (mc_idx_start+j) for j in range(op_mc_number[op_id])]
                mc_idx_start+=op_mc_number[op_id]
            return op_mc_map
        
        def append_route_infor(route_id, route_op_number):
            row_list = []
            final_op = False
            op_mc_number = gen_op_mc_number()
            op_mc_map = gen_op_mc_map(op_mc_number)
            for i in range(route_op_number[route_id]):
                if i == (route_op_number[route_id]-1):
                    final_op = True
                dict1 = {'route_id': route_id,
                         'op_id':'op_'+"%01d" % i+"0",
                         'su_t':str(ra.randint(0, 3)*10+20),
                         'op_t':str(ra.randint(5, 9)*10+30)
                         }
                dict1['next_op'] = "" if final_op else 'op_'+"%01d" % (i+1)+"0"
                row_list.append(dict1)
            return row_list
        
        #新增每個row_data
        for i, route_id in enumerate(route_id_list):
            row_list.extend(append_route_infor(route_id, route_op_number))
            
        #對每個Operation產生對應的資源ID
        for idx, row_dict in enumerate(row_list):
            row_dict['rs_id'] = 'rs_'+"%03d" % idx
        self.data = pd.DataFrame(row_list)
        self.data.to_excel(self.path+'/fake_route_table.xlsx', sheet_name='order',index=False)  
        return list(set(self.data['rs_id'].tolist()))