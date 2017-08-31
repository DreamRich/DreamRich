class Profit:

    def annual(cdi, ipca):
        return (cdi + 1) / (ipca + 1) - 1

    def net_annual(net_profitability, ipca):
        return ((net_profitability + 1) / (ipca + 1)) - 1

    def net_annual_suggested(
            cdi, wallet_profitability_target, income_tax, ipca):
        return (((cdi * wallet_profitability_target) -
                ((cdi * wallet_profitability_target) * income_tax) + 1)) /\
                (ipca + 1) - 1
