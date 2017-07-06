# encoding=utf-8
'''
回复结果
'''
def showResult(result,types):
    if types[0]=="查询 全部 工单":
        return get_order_relations(result)

    if types[0]=="查询 全部 设备 类型":
        return get_device_type(result)

    if types[0]=="查询 全部 设备":
        return monitoring_manage_get_devices(result)

    if types[0]=="查询 全部 采集点":
        return get_point_types(result)

    if types[0]=="查询 全部 应急 演练 预案":
        return get_drill_plan(result)

    if types[0]=="查询 局站 名称":
        return get_stations_name(result)

    if types[0]=="查询 全部 操作 日志":
        return get_operation_logs(result)

    if types[0]=="查询 position 报警 数量":
        return get_children_with_warning_count(result)

    if types[0]=="查询 position 员工":
        return get_staff_from_district(result)

    if types[0]=="查询 people 操作 日志 历史"or types[0]=="查询 people time 操作 日志 历史":
        return get_user_operation_log(result)

    if types[0]=="查询 people 历史 工单" or types[0]=="查询 people time 历史 工单":
        return get_work_orders(result)
    if types[0]=="查询 position 报警" or types[0]=="查询 position time 报警":
        return get_warning(result)
    if types[0]=="查询 position 设备":
        return get_devices_by_parents_name(result)
    if types[0]=="查询 people 通知":
        return get_received_messages(result)

def get_order_relations(result):
    print result
    rstr=""
    for x in result['message']:
        rstr+="设备编号:"
        rstr+=x['Device']
        rstr+='\n'
        rstr+="局站名称:"
        rstr+=x['Station']
        rstr+='\n'
        rstr+='工作人员:'
        rstr+='\n'
        for worker in x['Worker_Id']:
            rstr+=worker['name']
            rstr+='\n工号:'
            rstr+=worker['id']
            rstr+='\n'
        rstr+='\n\n'
    return rstr

def get_device_type(result):
    rstr=""
    for x in result['response'].values():
        rstr+=x
        rstr+='\n'
    return rstr

def monitoring_manage_get_devices(result):
    rstr=""
    for x in result['response']:
        rstr+="设备ID:"
        rstr+=x['ID']
        rstr+='\n'
        rstr+="设备类型:"
        rstr+=x['device_type']
        rstr+='\n'
        rstr+="设备名称:"
        rstr+=x['name']
        rstr+='\n'
        rstr+="设备位置:"
        for y in x['parents'].values():
            rstr+=y
            rstr+=" "
        rstr+='\n\n'
    return rstr

def get_point_types(result):
    rstr=""
    for x in result['response']:
        rstr+="采集点名称:"
        rstr+=x['name']
        rstr+='\n'
    return rstr

def get_drill_plan(result):
    rstr=""
    for x in result['message']:
        for y in x['plans']:
            url="/preplans/get_plan_by_id?plan_id="+y
            plan=getResult(url)
            plan=json.loads(plan)
            # print plan['message']
            insidex=plan['message']
            # print insidex
            rstr+="演练名称:"
            rstr+=insidex['name']
            rstr+="\n演练时间:"
            rstr+=insidex['time']
            rstr+="\n演练地点:"
            rstr+=insidex['location']
            rstr+="\n实施人员:"
            rstr+=insidex['operator']
            rstr+="\n联系电话:"
            rstr+=insidex['phone']
            rstr+="\n参演人员:"
            rstr+=insidex['operator']
            rstr+="\n演练步骤:"
            for step in range(len(insidex['description'])):
                rstr+="\n步骤"+str(step+1)+':'
                rstr+=insidex['description'][step]
    return rstr

def get_stations_name(result):
    rstr=""
    for x in result['response']:
        rstr+=x
        rstr+='\n'
    return rstr

def get_operation_logs(result):
    rstr=""
    for x in result['response']:
        rstr+="日期:"
        rstr+=x['timestamp']
        rstr+='\n'
        rstr+="处理人:"
        rstr+=x['operator']
        rstr+='\n'
        rstr+="操作信息:"
        if x['operations']!=[]:
            rstr+=x['operations'][0]['from'][0]['area']+'-'+x['operations'][0]['from'][0]['station']+'-'+x['operations'][0]['from'][0]['device_name']+'-'+x['operations'][0]['from'][0]['title']
        rstr+='\n'
        rstr+="操作结果:"
        rstr+=x['is_all_success']
        rstr+='\n\n'
    return rstr

def get_devices_by_parents_name(result):
    rstr="设备名称:\n"
    for x in result['response']:
        rstr+=x['name']
        rstr+='\n'
    return rstr


def get_children_with_warning_count(result):
    rstr=""
    for x in result['response']:
        rstr+='名字:'
        rstr+=x['name']
        rstr+='\n一般报警:'
        rstr+=str(x['warning_counts'][2])
        rstr+='\n紧急报警:'
        rstr+=str(x['warning_counts'][1])
        rstr+='\n严重报警:'
        rstr+=str(x['warning_counts'][0])
        rstr+="\n\n"

    return rstr


def get_staff_from_district(result):
    rstr=""
    for x in result["response"]:
        rstr+="姓名:"
        rstr+=x['name']
        rstr+="\n性别:"
        rstr+=x['gender']
        rstr+="\n电话:"
        rstr+=x['cellphone']
        rstr+="\n电邮:"
        rstr+=x['email']
        rstr+="\n公司:"
        rstr+=x['company']
        rstr+="\n类型:"
        rstr+=x['type']
        rstr+="\n区域:"
        rstr+=x['district']['name']
        rstr+="\n资格认证:"
        for y in x['qualification']:
            rstr+=y['name']
    return rstr

def get_received_messages(result):
    rstr=""
    for x in result['response']:
        rstr+="发件人:"
        rstr+=x['sender']
        rstr+='\n'
        rstr+="时间:"
        rstr+=x['timestamp']
        rstr+='\n'
        rstr+="标题:"
        rstr+=x['title']
        rstr+='\n'
        rstr+="内容:"
        rstr+=x['content']
        rstr+='\n\n'
    return rstr

def get_user_operation_log(result):
    rstr=""
    for x in result['response']:
        rstr+="操作人员:"
        for y in x['foreign1']:
            rstr+=y['name']
            rstr+=" "
        rstr+="\n权限:"
        for y in x['foreign2']:
            rstr+=y['name']
            rstr+=" "
        rstr+='\n操作内容:'
        rstr+=x['operation']
        rstr+='\n操作时间:'
        rstr+=x['timestamp']
        rstr+='\n\n'
    return rstr

def get_work_orders(result):
    status={'0':'已发送','1':'已确认','2':'已处理','3':'已完成'}
    rstr=""
    for x in result['response']:
        rstr+="工单编号:"
        rstr+=str(x['ID'])
        rstr+="\n处理人:"
        rstr+=x['worker_name']
        rstr+="\n地点:"
        rstr=rstr+x['event_detail']['Local_Network']+"-"+x['event_detail']['Area']+'-'+x['event_detail']['Local_Network']+x['event_detail']['Station']
        rstr+="\n产生时间:"
        rstr+=x['event_detail']['Start_Time']
        rstr+="\n工单内容:"
        rstr=rstr+x['event_detail']['Device']+'-'+x['event_detail']['Point']+'-'+x['event_detail']['Warning_Type']
        rstr+="\n当前状态:"
        rstr+=status[str(x['status']['current_status'])]
        rstr+='\n\n'
    return rstr

def get_point_info_with_real_time(result):
    rstr=""
    x=result['response']
    rstr+="区域:"
    rstr+=x['point']['area']
    rstr+="\n"
    rstr+="设备:"
    rstr+=x['point']['device_name']
    rstr+="\n"
    rstr+="监测点:"
    rstr+=x['point']['name']
    rstr+="\n"
    rstr+="时间:"
    rstr+=x['point_real_time']['time']
    rstr+="\n"
    rstr+="数值:"
    rstr=rstr+str(x['point_real_time']['value'])+x['point']['units']
    rstr+="\n"
    rstr+="状态:"
    rstr+=x['point']['warning_type']
    rstr+="\n"
    rstr+="\n\n"

    return rstr

def get_warning(result):
    rstr=""
    for x in result['response']:
        rstr+="位置:"
        rstr=rstr+x['Local_Network']+x['Area']+'-'+x['Station']+'-'+x['Device']
        rstr+='\n'
        rstr+="监控点:"
        rstr+=x['Point']
        rstr+='\n'
        rstr+="数值:"
        rstr=rstr+str(x['Value'])+x['Units']
        rstr+='\n'
        rstr+="开始时间:"
        rstr+=x['Start_Time']
        rstr+='\n'
        rstr+="类型:"
        rstr+=x['Warning_Type']
        rstr+='\n'
        rstr+="状态:"
        rstr+=x['Status']
        rstr+='\n\n'

    return rstr