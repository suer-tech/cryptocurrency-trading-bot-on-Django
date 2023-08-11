from django.shortcuts import render
from django.http import HttpResponse

from core.services.pnl_info import ProfitCalculator
from core.services.pos_info import create_array_pos_a, create_array_pos_b


def index_page(request):
    pos_a = create_array_pos_a()
    pos_b = create_array_pos_b()
    if request.method == 'POST':
        if 'pnl_a' in request.POST:
            # вызов функции для обработки нажатия на кнопку 1
            pnl_a_content = 'pnl_a'
            return render(request, 'index.html', {'pnl_a': pnl_a_content})

        elif 'pnl_b' in request.POST:
            # вызов функции для обработки нажатия на кнопку 2
            pnl_b_content = 'pnl_b'
            sublists = [pnl_b_content[x:x + 5] for x in range(0, len(pnl_b_content), 5)]
            sublists_str = ["".join(map(str, sublist)) for sublist in sublists]

            return render(request, 'index.html', {'pnl_b': sublists_str})
    else:
        return render(request, 'index.html')

calculator = ProfitCalculator()

def pnl(pair_ab, pos_ab, txt):
    pnlpair_ab = []
    for pair in pair_ab:
        for posas in pos_ab:
            if pair[0]['sym'] == posas['symbol']:
                pnlpair_ab.append(pair[0]['sym'][:-4])
                pnlpair_ab.append('-')
                pnlpair_ab.append(pair[1]['sym'][:-4])
                pnlpair_ab.append('= ')
                pnlpair_ab.append(f'{calculator.pnlPair(pair):.{2}}%')
                calculator.profitPair(pair)
    pnlpos = f"PNL = {calculator.pnlAB(pos_ab, txt):.{2}f}"
    pnlpair_ab.append(pnlpos)
    return pnlpair_ab







