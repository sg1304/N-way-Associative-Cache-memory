from random import randint
import filecmp
import os
import time


def read_file(filename):
    f1 = open(filename)
    my_line = f1.readline().rstrip()
    list1 = []
    while my_line:
        list1.append(my_line)
        my_line = f1.readline().rstrip()
    f1.close()
    return list1


cache_size = input("Enter the size of the cache in KB(only the number): ")
cache_size = int(cache_size)
cache_line_size = input("Enter the cache line size : ")
cache_line_size = int(cache_line_size)
way_associative = input("Enter the way associative : ")
way_associative = int(way_associative)
f3 = open("output.txt", "a+")
address_list = read_file('inst_addr_trace_hex_project_1.txt')
data_size_list = read_file('inst_data_size_project_1.txt')
cache_hit = False
cpu_clock = 0
main_size = 0
hit_count = 0
miss_count = 0


def my_reverse(s):
    if len(s) == 2:
        RAM_list.append(s)
    else:
        mm_byte = s[-2:]
        RAM_list.append(mm_byte)
        sample = s[0:len(s) - 2]
        my_reverse(sample)
    return


def power_of_two(x):
    if x == 1:
        pass
    else:
        power_of_two.power_count += 1
        q = x / 2
        power_of_two(q)
    return power_of_two.power_count


def build_cache(set1):
    sample_list = []
    for j in range(0, total_lines_in_each_set):
        sample_list.append({"valid": 0, "data": [], "tag": "0", "index": j, "set": set1})
    return sample_list


def cache_read(hex_address, data_size):
    global cpu_clock, cache_hit, hit_count, miss_count, total_access
    valid_flag = -1
    data_size = int(data_size)
    data_size = data_size // 2
    dec_address = int(hex_address, 16)
    bin_address = bin(dec_address)
    bit32_binary = bin_address[2:].zfill(32)
    tag = bit32_binary[0:tag_bits]
    print("Tag String = {0}".format(tag))
    index = bit32_binary[tag_bits:(tag_bits + index_bits)]
    print("Index String = {0}".format(index))
    index_int = int(index, 2)
    offset = bit32_binary[(tag_bits + index_bits):]
    print("Offset String = {0}".format(offset))
    offset_int = int(offset, 2)

    for set_number in range(way_associative):
        if cache_list[set_number][index_int]["valid"] == 0:
            cache_hit = False
            valid_flag = set_number

        elif cache_list[set_number][index_int]["valid"] == 1 and cache_list[set_number][index_int]["tag"] == tag:
            cache_hit = True
            break

        elif cache_list[set_number][index_int]["valid"] == 1 and cache_list[set_number][index_int]["tag"] != tag:
            cache_hit = False

        else:
            pass

    if cache_hit:
        cpu_clock = cpu_clock + 1
        hit_count = hit_count + 1
        final = list(cache_list[set_number][index_int]["data"][offset_int:(offset_int + data_size)])
        print("Cache hit")
        return final
    elif not cache_hit:
        if valid_flag != -1:
            valid_set_number = valid_flag
            cpu_clock = cpu_clock + 15
            miss_count = miss_count + 1
            mm_block_offset = (dec_address // cache_line_size) * cache_line_size
            cache_data = []
            for data in RAM_list[mm_block_offset:mm_block_offset + cache_line_size]:
                cache_data.append(data)
            cache_list[valid_set_number][index_int]["data"] = cache_data
            final = list(cache_list[valid_set_number][index_int]["data"][offset_int:(offset_int + data_size)])
            cache_list[valid_set_number][index_int]["valid"] = 1
            cache_list[valid_set_number][index_int]["tag"] = tag
            print("Cache Missed, Data pushed to the cache line having valid bit 0")
            return final

        elif valid_flag == -1:
            rand_set_number = randint(0, (way_associative - 1))
            cpu_clock = cpu_clock + 15
            miss_count = miss_count + 1
            mm_block_offset = (dec_address // cache_line_size) * cache_line_size
            cache_data = []
            for data in RAM_list[mm_block_offset:mm_block_offset + cache_line_size]:
                cache_data.append(data)
            cache_list[rand_set_number][index_int]["data"] = cache_data
            final = list(cache_list[rand_set_number][index_int]["data"][offset_int:(offset_int + data_size)])
            cache_list[rand_set_number][index_int]["valid"] = 1
            cache_list[rand_set_number][index_int]["tag"] = tag
            print("Cache Missed, Data pushed to the cache with valid bit 1 and tag mismatch.")
            return final

    else:
        pass


f = open('inst_mem_hex_16byte_wide.txt')
line = f.readline().rstrip()
line_length = len(line)
RAM_list = []

while line:
    my_reverse(line)
    line = f.readline().rstrip()
f.close()

power_of_two.power_count = 0
cache_line_power = power_of_two(cache_line_size)
print("Cache line size power 2 = {0}".format(cache_line_power))
power_of_two.power_count = 0
set_bits = power_of_two(way_associative)
print("Set bits size power 2 = {0}".format(set_bits))
power_of_two.power_count = 0
cache_size_power = (10 + power_of_two(cache_size)) - set_bits
print("Cache size power 2 = {0}".format(cache_size_power))
index_bits = cache_size_power - cache_line_power
print("Index bits = {0}".format(index_bits))
total_lines_in_each_set = 2 ** index_bits
print("total lines in caches = {0}".format(total_lines_in_each_set))
line_offset_bits = cache_line_power
print("Line offset bits = {0}".format(line_offset_bits))
tag_bits = 32 - (line_offset_bits + index_bits)
print("Tag bits = {0}".format(tag_bits))
print()

cache_list = [[]] * way_associative
for i in range(0, way_associative):
    cache_list[i] = build_cache(i)

for i in range(0, len(address_list)):
    main_size = int(data_size_list[i])
    main_size = main_size // 2
    final_data = []
    data_read = cache_read(address_list[i], data_size_list[i])
    final_data = data_read
    current_dec_address = int(address_list[i], 16)
    while len(final_data) < main_size:
        # logic to find new address
        new_address = current_dec_address + len(data_read)
        new_address = hex(new_address)
        new_address = str(new_address)
        # logic to find data_size
        new_data_size = main_size - (len(final_data))
        new_data_size = new_data_size * 2
        new_data_size = str(new_data_size)
        data_read = cache_read(new_address, new_data_size)
        current_dec_address = new_address
        current_dec_address = int(current_dec_address, 16)
        final_data = final_data + data_read

    final_data.reverse()
    print("{0} is the data fetched for the address {1}".format(final_data, address_list[i]))
    print()
    output = ''.join(str(e) for e in final_data)
    f3.write(output + '\n')
f3.close()
ipc = 57760 / cpu_clock
total_cache_access = hit_count + miss_count
hit_ratio = hit_count / total_cache_access
output_list = read_file("output.txt")
os.remove("output.txt")
output_list = [element.lower() for element in output_list]
time_str = time.strftime("%Y%m%d-%H%M%S")
file_name = "output_data_trace_" + time_str + ".txt"
f = open(file_name, 'w')
for items in output_list:
    f.write(items + '\n')
f.close()
print()
print("-------------------------------------------------------------------------------")
print()
print("Result of comparision with the data trace file is: {0}".format(
    filecmp.cmp(file_name, 'inst_data_trace_hex_project_1.txt')))
print("Total Hit count = {}".format(hit_count))
print("Total Miss count = {}".format(miss_count))
print("Hit ratio = {}".format(hit_ratio))
print("Total cycles = {}".format(cpu_clock))
print("Total cache access = {}".format(total_cache_access))
print("Instructions per clock cycle(IPC) = {}".format(ipc))
