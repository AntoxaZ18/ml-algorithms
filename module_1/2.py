from math import factorial


quality = 15    #количевто качественных деталей
defective = 5   #количество бракованных 
total = quality + defective #общее число деталей
samples = 2 #количество деталей в выборке


def k_combinations(total: int, samples: int) -> int:
    '''function return amount of combinations calc with formula total! / (samples! * (total - samples)!)
        total - total amount of samples
        samples - amount of samples
    '''

    return factorial(total) / (factorial(samples) * factorial(total - samples))


# общее число исходов
total_c = k_combinations(total, samples)


#Число исходов когда 2 хорошие
quality_2 = k_combinations(quality, samples)
print(f'Probability 2 quality: {(quality_2) / total_c:.2f}')


#Обе бракованные
defective_2 = k_combinations(defective, samples)
print(f'Probability 1 quality, 1 defective: {(defective_2) / total_c:.2f}')


#1 брак и 1 хорошая
quality = k_combinations(quality, 1)
defective = k_combinations(defective, 1)
print(f'Probability 1 quality, 1 defective: {(quality * defective) / total_c:.2f}')
