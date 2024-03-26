import xml.etree.ElementTree as ET
import Task
import Scheduler
import Cpu
import math


def import_file(file_path, output_file):
    scheduler = None
    root_node = ET.parse(file_path).getroot()

    # Parsing scheduler
    for node in root_node.findall('./software/scheduler'):
        if scheduler is not None:
            raise Exception('More than one scheduler is defined in the file')
        algorithm = node.attrib.get('algorithm')
        if algorithm == 'RR':
            quantum = node.attrib.get('quantum')
            if quantum is None:
                raise Exception('No "quantum" attribute defined in the file')
            scheduler = Scheduler.RoundRobin(output_file, quantum)
        elif algorithm == 'FIFO':
            scheduler = Scheduler.FIFO(output_file)
        elif algorithm == 'SJF':
            scheduler = Scheduler.SJF(output_file)
        elif algorithm == 'HRRN':
            scheduler = Scheduler.HRRN(output_file)
        elif algorithm == 'SRTF':
            scheduler = Scheduler.SRTF(output_file)
        else:
            raise Exception(f'Invalid scheduler algorithm: {algorithm}')

    if scheduler is None:
        raise Exception('No scheduler is defined in the file')
    
    
    # Parsing tasks
    for node in root_node.findall('./software/tasks/task'):
        _real_time = node.attrib.get('real-time', 'false') == 'true'
        _type = node.attrib['type']
        _id = int(node.attrib['id'])
        _period = int(node.attrib.get('period', -1))
        _activation = int(node.attrib.get('activation', -1))
        _deadline = int(node.attrib.get('deadline', -1))
        _wcet = int(node.attrib['wcet'])

        #print(_id, _wcet, _type, _period, _activation)
        if _id < 0 or _wcet <= 0 or (_type == 'periodic' and _period <= 0) or (_type == 'sporadic' and _activation < 0):
            print(_id, _wcet, _type, _period, _activation)
            raise Exception('Non-positive values are saved in the file')

        #if (_wcet > _period != -1) or (_deadline != -1 and _deadline < _wcet):
            #raise Exception('Inconsistent values are saved in the file')

        task = Task.Task(_real_time, _type, _id, _period, _activation, _deadline, _wcet)
        scheduler.tasks.append(task)


    if not scheduler.tasks:
        raise Exception('No tasks recognized in the file')

    # Parsing time
    time_node = root_node.find('./time')
    if time_node is not None:
        scheduler.start = int(time_node.attrib['start'])
        scheduler.end = int(time_node.attrib['end'])
        if scheduler.end < scheduler.start :
            raise Exception('Error in time definition')#chiedi se non deve fare nulla o lanciare eccezzione

    # Parsing hardware
    for node in root_node.findall('./hardware/cpus/pe'):
        _id = node.attrib['id']
        core = Cpu.Core(_id)
        core_speed = node.attrib.get('speed')
        if core_speed:
            core.speed = core_speed
        scheduler.cores.append(core)

    if not scheduler.cores:
        raise Exception('No cores recognized in the file')

    return scheduler


# This class was based on SchedSim v1:
# https://github.com/HEAPLab/schedsim/blob/master/SchedIo.py
class SchedulerEventWriter:
    def __init__(self, output_file):
        self.out = open(output_file, 'w')

    def add_scheduler_event(self, scheduler_event):
        self.out.write(
            str(scheduler_event.timestamp) + ',' + str(scheduler_event.task.id) + ',' +
            str(scheduler_event.job) + ',' + str(scheduler_event.processor) + ',' +
            str(scheduler_event.type) + ',' + str(scheduler_event.extra) + '\n')

    def terminate_write(self):
        self.out.close()
