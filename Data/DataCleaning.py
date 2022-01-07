# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:06:50 2021

@author: RoyTseng
"""


def wip_cleaning(raw_wip):
    wip_dict = {}
    for idx,row in raw_wip.iterrows():
        wip_data = {}
        wip_data['order_id'] = row['工單號']
        wip_data['pd_id'] = row['產品號碼']
        wip_data['is_hold'] = row['保留']
        wip_data['op_name'] = row['加工站點類型代號']
        wip_data['op_id'] = row['加工站點代號']
        wip_data['CLM_time'] = row['資料擷取時間']
        wip_data['data_date'] = row['資料所屬日期']
        #Special
        wip_data['virtual_pd_id'] = row['虛擬產品號']
        wip_data['layer'] = row['add層別']
        #TODO
        wip_data['sheet'] = row['addwip']
        wip_data['pcs'] = row['addpcs']
        wip_data['on_machine'] = row['機台歸屬(2D)']
        wip_data['pd_type'] = row['add產品類型']
        wip_data['entry_time'] = row['進站時間']
        #TODO
        wip_data['lot_id'] = row['add Lot']
        wip_dict[wip_data['order_id']] = wip_data
        
    return wip_dict

def route_bom_cleaning(route_bom):
    route_bom.columns = ['idx', 'pd_id', 'board_id', 'layer_code', 'layer',
                         'op_id', 'op_name', 'op_t_type', 'sq_idx', 'pd_type',
                         'op_t', 'q_time', 'unit_qty']
    
    return route_bom