import xml.etree.ElementTree as ET
import SchedIO
import Task
import random

MAX_TIME_END = 100
MAX_PERIOD = 50
MAX_WCET = 40

if __name__ == "__main__":
    time_start = 0  # TODO random
    time_end = random.randint(0, MAX_TIME_END)
    simulation1 = ET.Element("simulation")
    time1 = ET.SubElement(simulation1, "time", start="0", end=str(time_end))
    time1.tail = "\n"
    software1 = ET.SubElement(simulation1, "software")
    tasks1 = ET.SubElement(software1, "tasks")
    tasks1.tail = "\n"
    simulation2 = ET.Element("simulation")
    time2 = ET.SubElement(simulation2, "time", start="0", end=str(time_end))
    time2.tail = "\n"
    software2 = ET.SubElement(simulation2, "software")
    tasks2 = ET.SubElement(software2, "tasks")
    tasks2.tail = "\n"
    new_tasks = []

    for task in range(1, 21):
        real_time = random.randint(0, 1)
        real_time_str = ''
        if real_time == 0:
            real_time = False
            real_time_str = 'false'
        else:
            real_time = True
            real_time_str = 'true'
        type = random.randint(0, 1)
        activation = None
        period = None
        deadline = None
        if type == 0:
            type = 'sporadic'
            activation = random.randint(0, time_end)
            deadline = random.randint(activation, MAX_TIME_END)
        else:
            type = 'periodic'
            period = random.randint(1, MAX_PERIOD)
            deadline = random.randint(0, MAX_TIME_END)
        wcet = random.randint(1, MAX_WCET)
        id = task
        if type == 'sporadic':
            if real_time:
                add_task1 = ET.SubElement(tasks1, "task", real_time=real_time_str, type="sporadic", id=str(id), activation=str(activation), deadline=str(deadline), wcet=str(wcet))
                add_task1.tail = "\n"
                if task <= 15:
                    add_task2 = ET.SubElement(tasks2, "task", real_time=real_time_str, type="sporadic", id=str(id), activation=str(activation), deadline=str(deadline), wcet=str(wcet))
                    add_task2.tail = "\n"
                    new_task = Task.Task(real_time, type, task, period, activation, deadline, wcet)
                    new_tasks.append(new_task)
            else:
                add_task1 = ET.SubElement(tasks1, "task", real_time=real_time_str, type="sporadic", id=str(id), activation=str(activation), wcet=str(wcet))
                add_task1.tail = "\n"
                if task <= 15:
                    add_task2 = ET.SubElement(tasks2, "task", real_time=real_time_str, type="sporadic", id=str(id), activation=str(activation), wcet=str(wcet))
                    add_task2.tail = "\n"
                else:
                    new_task = Task.Task(real_time, type, task, period, activation, deadline, wcet)
                    new_tasks.append(new_task)
        else:
            add_task1 = ET.SubElement(tasks1, "task", real_time=real_time_str, type="periodic", id=str(id), period=str(period), deadline=str(deadline), wcet=str(wcet))
            add_task1.tail = "\n"
            if task <= 15:
                add_task2 = ET.SubElement(tasks2, "task", real_time=real_time_str, type="periodic", id=str(id), period=str(period), deadline=str(deadline), wcet=str(wcet))
                add_task2.tail = "\n"
                new_task = Task.Task(real_time, type, task, period, activation, deadline, wcet)
                new_tasks.append(new_task)
    scheduler1 = ET.SubElement(software1, "scheduler", algorithm="FIFO")
    scheduler1.tail = "\n"
    scheduler2 = ET.SubElement(software2, "scheduler", algorithm="FIFO")
    scheduler2.tail = "\n"
    hardware1 = ET.SubElement(simulation1, "hardware")
    hardware2 = ET.SubElement(simulation2, "hardware")
    cpus1 = ET.SubElement(hardware1, "cpus")
    cpus1.tail = "\n"
    cpus2 = ET.SubElement(hardware2, "cpus")
    cpus2.tail = "\n"
    pe1 = ET.SubElement(cpus1, "pe", id="0", speed="1")
    pe1.tail = "\n"
    pe2 = ET.SubElement(cpus2, "pe", id="0", speed="1")
    pe2.tail = "\n"
    tree1 = ET.ElementTree(simulation1)
    tree1.write("examples/Inputs/test_input1.xml", encoding="UTF-8", xml_declaration=True)
    tree2 = ET.ElementTree(simulation2)
    tree2.write("examples/Inputs/test_input2.xml", encoding="UTF-8", xml_declaration=True)

    test_scheduler1 = SchedIO.import_file("examples/Inputs/test_input1.xml", "examples/Outputs/test_output1.txt")
    test_scheduler1.execute()
    test_scheduler2 = SchedIO.import_file("examples/Inputs/test_input2.xml", "examples/Outputs/test_output2.txt")
    test_scheduler2.execute()
    for new_task in new_tasks:
        test_scheduler2.new_task(new_task)
