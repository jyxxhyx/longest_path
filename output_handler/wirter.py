

def write_result(sols, file_name):
    with open(file_name, mode='w', encoding='utf-8-sig') as f:
        for i in range(len(sols[0])):
            f.write(f'{i},')
        f.write('\n')

        for sol in sols:
            for item in sol:
                f.write(f'{item},')
            f.write('\n')
    return
