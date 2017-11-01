class Rate:

    @staticmethod
    def difference(rate_a, rate_b):
        return (rate_a / rate_b) - 1

    @staticmethod
    def monthly_to_anual(rate):
        """Reference: http://www2.unemat.br/eugenio/files_financeira/\
           6_equivalencia_de_taxas.htm"""

        return ((rate + 1)**12) - 1

    @staticmethod
    def anual_to_monthly(rate):
        """Reference: http://www2.unemat.br/eugenio/files_financeira/\
           6_equivalencia_de_taxas.htm"""

        return ((1 + rate)**(1 / 12)) - 1

    @staticmethod
    def real_rate(rate, ipca):
        """Reference: http://mundoeducacao.bol.uol.com.br/\
           matematica/taxa-efetiva-taxa-real.htm"""

        return ((1 + rate) / (1 + ipca)) - 1
