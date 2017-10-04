def actual_rate(first_rate, seccond_rate):
    return (first_rate + 1) / (seccond_rate + 1) - 1

def net_annual_suggested(
        cdi, wallet_profitability_target, income_tax, ipca):
    return (((cdi * wallet_profitability_target) -
             ((cdi * wallet_profitability_target) * income_tax) + 1)) /\
        (ipca + 1) - 1
