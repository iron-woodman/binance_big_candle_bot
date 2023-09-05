import time

# last_signal_time = 1.0
#
# while True:
#     if time.time() - last_signal_time > 5:
#         print(last_signal_time)
#         last_signal_time = time.time()



def list_to_string(lst):
    mess = ''
    for item in lst:
        mess += item + '\n'
    return mess


print(list_to_string(['1', '2', '3']))